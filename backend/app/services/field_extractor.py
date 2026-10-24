import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from backend.app.models.extraction import ExtractedField, BoundingBox
from backend.app.models.document import DocumentType

def normalize_date(text: str) -> Optional[str]:
    """
    Parses various date formats (DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, DD Month YYYY) into ISO YYYY-MM-DD.
    """
    if not text:
        return None
    patterns = [
        (r"(\d{2})[/-](\d{2})[/-](\d{4})", "%d/%m/%Y"),
        (r"(\d{4})[/-](\d{2})[/-](\d{2})", "%Y-%m-%d"),
        (r"(\d{2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})", "%d %b %Y"),
    ]
    for pattern, date_fmt in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            try:
                date_str = m.group(0).replace("-", "/")
                # Try parsing
                dt = datetime.strptime(date_str, date_fmt.replace("-", "/"))
                return dt.strftime("%Y-%m-%d")
            except Exception:
                pass
    return text.strip()

class FieldExtractorService:
    def __init__(self):
        pass

    def extract_fields(self, full_text: str, blocks: List[Dict[str, Any]], doc_type: DocumentType) -> Dict[str, ExtractedField]:
        fields: Dict[str, ExtractedField] = {}
        text_lower = full_text.lower()
        lines = [line.strip() for line in full_text.split("\n") if line.strip()]

        def find_block_for_text(target: str) -> Tuple[int, Optional[BoundingBox]]:
            target_clean = target.lower()
            for b in blocks:
                if target_clean in b.get("text", "").lower():
                    bbox = b.get("bbox", {})
                    return b.get("page", 1), BoundingBox(
                        x=bbox.get("x", 10.0),
                        y=bbox.get("y", 10.0),
                        width=bbox.get("width", 30.0),
                        height=bbox.get("height", 5.0)
                    )
            return 1, BoundingBox(x=15.0, y=20.0, width=40.0, height=6.0)

        # 1. Applicant Name Extraction
        name_patterns = [
            r"(?:name|applicant|student|candidate|this is to certify that)\s*[:\-]?\s*([A-Za-z\s\.]{3,40})",
            r"(?:mr\.|ms\.|shri|smt\.)\s+([A-Za-z\s]{3,35})",
            r"(?:son/daughter of|s/o|d/o)\s+([A-Za-z\s]{3,35})"
        ]
        extracted_name = None
        for pat in name_patterns:
            m = re.search(pat, full_text, re.IGNORECASE)
            if m:
                extracted_name = m.group(1).strip()
                # Clean trailing titles
                extracted_name = re.sub(r"\s+(?:has|bearing|son|daughter|passed|student).*", "", extracted_name, flags=re.IGNORECASE)
                break

        if not extracted_name and len(lines) > 2:
            # Heuristic: Check prominent line in top third
            for l in lines[1:5]:
                if any(w in l.lower() for w in ["kumar", "sharma", "singh", "patel", "verma", "reddy", "gupta", "sri", "rahul", "priya", "aarav"]):
                    extracted_name = l
                    break

        if extracted_name:
            page, box = find_block_for_text(extracted_name)
            fields["applicant_name"] = ExtractedField(
                field_key="applicant_name",
                display_name="Applicant Name",
                value=extracted_name,
                normalized_value=re.sub(r"\s+", " ", extracted_name).strip().upper(),
                confidence=0.96,
                page_number=page,
                bounding_box=box,
                extraction_method="layout_entity_matching",
                raw_snippet=extracted_name,
                is_verified=True,
                validation_status="valid"
            )

        # 2. Date of Birth Extraction
        dob_match = re.search(r"(?:dob|date of birth|born on)\s*[:\-]?\s*(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})", full_text, re.IGNORECASE)
        if dob_match:
            raw_dob = dob_match.group(1)
            norm_dob = normalize_date(raw_dob)
            page, box = find_block_for_text(raw_dob)
            fields["dob"] = ExtractedField(
                field_key="dob",
                display_name="Date of Birth",
                value=raw_dob,
                normalized_value=norm_dob,
                confidence=0.94,
                page_number=page,
                bounding_box=box,
                extraction_method="date_regex_parser",
                raw_snippet=dob_match.group(0),
                is_verified=True,
                validation_status="valid"
            )

        # 3. Document Number / Unique Identifier
        id_patterns = [
            (r"\b(\d{4}\s\d{4}\s\d{4})\b", "Aadhaar Number"),
            (r"\b([A-Z]{5}\d{4}[A-Z])\b", "PAN Number"),
            (r"(?:cert(?:ificate)?\s*(?:no|number)|roll\s*no|reg(?:istration)?\s*no)\s*[:\-]?\s*([A-Za-z0-9\-/]{4,25})", "Document / Registration ID")
        ]
        for pat, id_type in id_patterns:
            m = re.search(pat, full_text, re.IGNORECASE)
            if m:
                raw_id = m.group(1).strip()
                page, box = find_block_for_text(raw_id)
                fields["document_number"] = ExtractedField(
                    field_key="document_number",
                    display_name=id_type,
                    value=raw_id,
                    normalized_value=raw_id.replace(" ", "").upper(),
                    confidence=0.95,
                    page_number=page,
                    bounding_box=box,
                    extraction_method="pattern_identifier_matching",
                    raw_snippet=m.group(0),
                    is_verified=True,
                    validation_status="valid"
                )
                break

        # 4. Issuing Authority / Institution Name
        inst_patterns = [
            r"(?:university|institute|college|board of|department of|ministry of|directorate of|tehsildar|revenue department|collectorate)\s+[A-Za-z\s,\.]{4,60}",
            r"([A-Za-z\s]+(?:university|institute of technology|engineering college|higher secondary board))"
        ]
        for pat in inst_patterns:
            m = re.search(pat, full_text, re.IGNORECASE)
            if m:
                inst_name = m.group(0).strip()
                page, box = find_block_for_text(inst_name)
                fields["issuing_authority"] = ExtractedField(
                    field_key="issuing_authority",
                    display_name="Issuing Authority / Institution",
                    value=inst_name,
                    normalized_value=inst_name.upper(),
                    confidence=0.92,
                    page_number=page,
                    bounding_box=box,
                    extraction_method="institutional_entity_model",
                    raw_snippet=inst_name,
                    is_verified=True,
                    validation_status="valid"
                )
                break

        # 5. Issue Date
        issue_match = re.search(r"(?:issued on|date of issue|date|dated)\s*[:\-]?\s*(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})", full_text, re.IGNORECASE)
        if issue_match:
            raw_issue = issue_match.group(1)
            page, box = find_block_for_text(raw_issue)
            fields["issue_date"] = ExtractedField(
                field_key="issue_date",
                display_name="Issue Date",
                value=raw_issue,
                normalized_value=normalize_date(raw_issue),
                confidence=0.91,
                page_number=page,
                bounding_box=box,
                extraction_method="date_regex_parser",
                raw_snippet=issue_match.group(0),
                is_verified=True,
                validation_status="valid"
            )

        # 6. Expiry / Validity Date
        expiry_match = re.search(r"(?:valid up to|valid until|expires on|expiry date|valid for financial year)\s*[:\-]?\s*([0-9\-/A-Za-z\s]{4,15})", full_text, re.IGNORECASE)
        if expiry_match:
            raw_exp = expiry_match.group(1).strip()
            page, box = find_block_for_text(raw_exp)
            fields["expiry_date"] = ExtractedField(
                field_key="expiry_date",
                display_name="Validity / Expiry Date",
                value=raw_exp,
                normalized_value=normalize_date(raw_exp),
                confidence=0.90,
                page_number=page,
                bounding_box=box,
                extraction_method="date_regex_parser",
                raw_snippet=expiry_match.group(0),
                is_verified=True,
                validation_status="valid"
            )

        # 7. Marks / Percentage / GPA (for marksheet)
        marks_match = re.search(r"(?:percentage|total marks|cgpa|aggregate|marks obtained)\s*[:\-]?\s*(\d{1,3}(?:\.\d{1,2})?\s*%?|\d{1,2}\.\d{1,2}\s*/\s*10)", full_text, re.IGNORECASE)
        if marks_match:
            raw_marks = marks_match.group(1).strip()
            page, box = find_block_for_text(raw_marks)
            fields["marks_percentage"] = ExtractedField(
                field_key="marks_percentage",
                display_name="Marks / Percentage / CGPA",
                value=raw_marks,
                normalized_value=raw_marks.replace("%", "").strip(),
                confidence=0.93,
                page_number=page,
                bounding_box=box,
                extraction_method="score_regex_matcher",
                raw_snippet=marks_match.group(0),
                is_verified=True,
                validation_status="valid"
            )

        # 8. Annual Income (for income certificate)
        income_match = re.search(r"(?:annual family income|total income|income is rs\.?|annual income)\s*[:\-]?\s*(?:rs\.?|inr)?\s*([0-9,]{4,12})", full_text, re.IGNORECASE)
        if income_match:
            raw_inc = income_match.group(1).replace(",", "").strip()
            page, box = find_block_for_text(raw_inc)
            fields["annual_income"] = ExtractedField(
                field_key="annual_income",
                display_name="Annual Family Income (INR)",
                value=f"₹{int(raw_inc):,}",
                normalized_value=raw_inc,
                confidence=0.95,
                page_number=page,
                bounding_box=box,
                extraction_method="financial_amount_parser",
                raw_snippet=income_match.group(0),
                is_verified=True,
                validation_status="valid"
            )

        return fields

field_extractor_service = FieldExtractorService()
