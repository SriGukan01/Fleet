import uuid
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher
from backend.app.models.cross_verification import (
    CrossDocumentComparison,
    MatchStatus,
    CrossVerificationSummary
)
from backend.app.models.document import DocumentInDB

def string_similarity(a: str, b: str) -> float:
    """Computes normalized string similarity ratio between 0.0 and 1.0"""
    if not a or not b:
        return 0.0
    s_a = " ".join(a.lower().strip().split())
    s_b = " ".join(b.lower().strip().split())
    if s_a == s_b:
        return 1.0
    return SequenceMatcher(None, s_a, s_b).ratio()

class CrossDocumentService:
    def __init__(self):
        pass

    def perform_cross_verification(
        self,
        application_id: str,
        declared_details: Dict[str, Any],
        documents: List[Dict[str, Any]]
    ) -> CrossVerificationSummary:
        comparisons: List[CrossDocumentComparison] = []
        total_checks = 0
        passed_checks = 0
        fuzzy_matches = 0
        mismatches = 0
        contradictions = 0

        # Build index of extracted fields per document
        # Map doc_id -> {field_key: field_dict}
        doc_fields_map: Dict[str, Dict[str, Any]] = {}
        doc_meta_map: Dict[str, Dict[str, Any]] = {}
        for d in documents:
            d_id = d.get("_id") or d.get("id")
            doc_fields_map[d_id] = d.get("extracted_fields", {})
            doc_meta_map[d_id] = {
                "name": d.get("metadata", {}).get("original_filename", "Document"),
                "type": d.get("document_type", "unknown")
            }

        doc_ids = list(doc_fields_map.keys())

        # 1. Compare Applicant Name across declared details vs each document
        declared_name = declared_details.get("applicant_name")
        if declared_name:
            for d_id in doc_ids:
                extracted = doc_fields_map[d_id].get("applicant_name")
                if extracted:
                    total_checks += 1
                    ext_val = extracted.get("value", "")
                    sim = string_similarity(declared_name, ext_val)
                    
                    if sim == 1.0:
                        passed_checks += 1
                        status = MatchStatus.EXACT_MATCH
                        contra = False
                        res = "Values match perfectly. No reviewer action required."
                    elif sim >= 0.80:
                        fuzzy_matches += 1
                        status = MatchStatus.FUZZY_MATCH
                        contra = False
                        res = "Minor spelling/initials variation detected. Verify name alias or initials."
                    else:
                        mismatches += 1
                        contradictions += 1
                        status = MatchStatus.MISMATCH
                        contra = True
                        res = "Significant name divergence detected. Check for identity impersonation or legal name change deed."

                    comparisons.append(CrossDocumentComparison(
                        id=str(uuid.uuid4()),
                        field_key="applicant_name",
                        display_name="Applicant Full Name",
                        doc1_id="declared_application",
                        doc1_name="Application Form (Declared)",
                        doc1_type="application_record",
                        doc1_value=declared_name,
                        doc2_id=d_id,
                        doc2_name=doc_meta_map[d_id]["name"],
                        doc2_type=doc_meta_map[d_id]["type"],
                        doc2_value=ext_val,
                        match_status=status,
                        similarity_score=round(sim, 2),
                        contradiction_flag=contra,
                        evidence_reference=f"Page {extracted.get('page_number', 1)} entity extraction",
                        suggested_resolution=res
                    ))

        # 2. Compare Pairwise across documents (e.g. Identity vs Degree Certificate)
        for i in range(len(doc_ids)):
            for j in range(i + 1, len(doc_ids)):
                id1, id2 = doc_ids[i], doc_ids[j]
                fields1 = doc_fields_map[id1]
                fields2 = doc_fields_map[id2]
                name1 = doc_meta_map[id1]["name"]
                name2 = doc_meta_map[id2]["name"]

                # A. Compare Name between Doc1 and Doc2
                if "applicant_name" in fields1 and "applicant_name" in fields2:
                    total_checks += 1
                    v1 = fields1["applicant_name"].get("value", "")
                    v2 = fields2["applicant_name"].get("value", "")
                    sim = string_similarity(v1, v2)
                    
                    if sim == 1.0:
                        passed_checks += 1
                        status = MatchStatus.EXACT_MATCH
                        contra = False
                        res = "Names agree between documents."
                    elif sim >= 0.82:
                        fuzzy_matches += 1
                        status = MatchStatus.FUZZY_MATCH
                        contra = False
                        res = "Spelling variation between documents (e.g., transliteration). Officer check recommended."
                    else:
                        mismatches += 1
                        contradictions += 1
                        status = MatchStatus.MISMATCH
                        contra = True
                        res = f"Mismatch: '{v1}' in {name1} vs '{v2}' in {name2}. Request clarifying identity affidavit."

                    comparisons.append(CrossDocumentComparison(
                        id=str(uuid.uuid4()),
                        field_key="applicant_name_interdoc",
                        display_name=f"Applicant Name ({name1} vs {name2})",
                        doc1_id=id1,
                        doc1_name=name1,
                        doc1_type=doc_meta_map[id1]["type"],
                        doc1_value=v1,
                        doc2_id=id2,
                        doc2_name=name2,
                        doc2_type=doc_meta_map[id2]["type"],
                        doc2_value=v2,
                        match_status=status,
                        similarity_score=round(sim, 2),
                        contradiction_flag=contra,
                        evidence_reference="Cross-document OCR entity matching",
                        suggested_resolution=res
                    ))

                # B. Compare Date of Birth
                if "dob" in fields1 and "dob" in fields2:
                    total_checks += 1
                    dob1 = fields1["dob"].get("normalized_value", fields1["dob"].get("value", ""))
                    dob2 = fields2["dob"].get("normalized_value", fields2["dob"].get("value", ""))
                    
                    if dob1 and dob2 and dob1 == dob2:
                        passed_checks += 1
                        comparisons.append(CrossDocumentComparison(
                            id=str(uuid.uuid4()),
                            field_key="dob_interdoc",
                            display_name="Date of Birth (DOB) Match",
                            doc1_id=id1,
                            doc1_name=name1,
                            doc1_type=doc_meta_map[id1]["type"],
                            doc1_value=dob1,
                            doc2_id=id2,
                            doc2_name=name2,
                            doc2_type=doc_meta_map[id2]["type"],
                            doc2_value=dob2,
                            match_status=MatchStatus.EXACT_MATCH,
                            similarity_score=1.0,
                            contradiction_flag=False,
                            evidence_reference="Normalized ISO date verification",
                            suggested_resolution="Dates of birth match exactly."
                        ))
                    elif dob1 and dob2:
                        mismatches += 1
                        contradictions += 1
                        comparisons.append(CrossDocumentComparison(
                            id=str(uuid.uuid4()),
                            field_key="dob_interdoc",
                            display_name="Date of Birth Contradiction",
                            doc1_id=id1,
                            doc1_name=name1,
                            doc1_type=doc_meta_map[id1]["type"],
                            doc1_value=dob1,
                            doc2_id=id2,
                            doc2_name=name2,
                            doc2_type=doc_meta_map[id2]["type"],
                            doc2_value=dob2,
                            match_status=MatchStatus.MISMATCH,
                            similarity_score=0.0,
                            contradiction_flag=True,
                            evidence_reference="Normalized ISO date verification",
                            suggested_resolution=f"DOB contradiction: '{dob1}' in {name1} vs '{dob2}' in {name2}. Request official birth certificate / matriculation record."
                        ))

        # Overall Status
        if contradictions > 0 or mismatches > 1:
            overall_status = "severe_mismatch"
        elif fuzzy_matches > 0:
            overall_status = "attention_required"
        else:
            overall_status = "passed"

        return CrossVerificationSummary(
            application_id=application_id,
            total_checks=total_checks,
            passed_checks=passed_checks,
            fuzzy_matches=fuzzy_matches,
            mismatches=mismatches,
            contradictions=contradictions,
            comparisons=comparisons,
            overall_status=overall_status
        )

cross_document_service = CrossDocumentService()
