import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from backend.app.config import settings
from backend.app.database import get_db
from backend.app.services.auth_service import hash_password
from backend.app.services.storage_service import storage_service
from backend.app.services.ocr_service import ocr_service
from backend.app.services.forensic_service import forensic_service
from backend.app.services.digital_signature import digital_signature_service
from backend.app.services.field_extractor import field_extractor_service
from backend.app.services.cross_doc_service import cross_document_service
from backend.app.services.compliance_engine import compliance_engine, DEFAULT_RULES
from backend.app.services.risk_engine import risk_engine
from backend.app.services.issuer_service import issuer_service
from backend.app.models.document import DocumentType, DocumentStatus, DocumentMetadata

def create_synthetic_pdf(
    file_path: str,
    title: str,
    fields: dict,
    producer: str = "Government Printing & Record System v4.1",
    include_stamp: bool = True
):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    doc = SimpleDocTemplate(file_path, pagesize=letter, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()

    c_navy = colors.HexColor("#0B192C")
    c_teal = colors.HexColor("#0D9488")
    
    t_style = ParagraphStyle('SynTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=c_navy, alignment=1)
    b_style = ParagraphStyle('SynBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#1E293B"))
    stamp_style = ParagraphStyle('SynStamp', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor("#047857"), alignment=1)

    elements = [
        Paragraph(title.upper(), t_style),
        Paragraph("OFFICIAL RECORD — SYNTHETIC DEMONSTRATION DOCUMENT", ParagraphStyle('Sub', parent=b_style, fontSize=8, textColor=c_teal, alignment=1)),
        Spacer(1, 20)
    ]

    table_data = []
    for k, v in fields.items():
        table_data.append([
            Paragraph(f"<b>{k}:</b>", b_style),
            Paragraph(str(v), b_style)
        ])

    table = Table(table_data, colWidths=[180, 320])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 25))

    if include_stamp:
        stamp_data = [
            [Paragraph("★ ISSUING AUTHORITY SEAL ★<br/>VERIFIED & DIGITALLY CATALOGED<br/>GOVERNMENT OF INDIA", stamp_style)]
        ]
        stamp_table = Table(stamp_data, colWidths=[240])
        stamp_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#047857")),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ECFDF5")),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        elements.append(stamp_table)

    doc.build(elements)

    # Set metadata
    try:
        import fitz
        fdoc = fitz.open(file_path)
        fdoc.set_metadata({
            "title": title,
            "author": "National Verification Registry",
            "producer": producer,
            "creator": "Official Form Ingestion Engine",
            "creationDate": "D:20240115100000Z",
            "modDate": "D:20240115100000Z" if "canva" not in producer.lower() else "D:20241020140000Z"
        })
        fdoc.save(file_path, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
        fdoc.close()
    except Exception:
        pass

async def seed_database():
    db = get_db()
    users_col = db.get_collection("users")
    rules_col = db.get_collection("compliance_rules")
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")
    issuers_col = db.get_collection("issuer_registry")

    # 1. Seed Users (Applicant, Officer, Admin)
    demo_users = [
        {
            "_id": "user_demo_applicant",
            "email": "applicant@veritrust.ai",
            "name": "Aarav Sharma",
            "role": "applicant",
            "organization": "Delhi Technological University",
            "hashed_password": hash_password("Demo@123"),
            "is_active": True,
            "is_demo": True,
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "_id": "user_demo_officer",
            "email": "officer@veritrust.ai",
            "name": "Dr. Priya Raman (Verification Officer)",
            "role": "officer",
            "organization": "AICTE Scrutiny Cell",
            "hashed_password": hash_password("Demo@123"),
            "is_active": True,
            "is_demo": True,
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "_id": "user_demo_admin",
            "email": "admin@veritrust.ai",
            "name": "System Administrator",
            "role": "admin",
            "organization": "National Smart Automation Directorate",
            "hashed_password": hash_password("Demo@123"),
            "is_active": True,
            "is_demo": True,
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    for u in demo_users:
        existing = await users_col.find_one({"email": u["email"]})
        if not existing:
            await users_col.insert_one(u)

    # 2. Seed Compliance Rules
    for r in DEFAULT_RULES:
        existing = await rules_col.find_one({"rule_id": r["rule_id"]})
        if not existing:
            await rules_col.insert_one(r)

    # 3. Seed Registered Issuers
    for iss in issuer_service.get_registered_issuers():
        existing = await issuers_col.find_one({"issuer_code": iss.issuer_code})
        if not existing:
            await issuers_col.insert_one(iss.model_dump(by_alias=True))

    # 4. Check if demo scenarios already exist
    existing_apps = await apps_col.count_documents({})
    if existing_apps >= 6:
        return

    # Seed the 6 synthetic demonstration scenarios
    scenarios = [
        {
            "code": "scenario_clean",
            "ref_id": "APP-2026-CLEAN-01",
            "name": "Aarav Sharma",
            "email": "aarav.sharma@example.edu",
            "category": "scholarship",
            "org": "AICTE Pragati Scheme",
            "notes": "Scenario 1: Clean Application. All records consistent, rules satisfied, low review priority.",
            "documents": [
                {
                    "type": DocumentType.IDENTITY_DOCUMENT,
                    "title": "Government Identity Card (Aadhaar)",
                    "fields": {
                        "Applicant Name": "Aarav Sharma",
                        "Aadhaar Number": "5482 9104 3821",
                        "Date of Birth": "14/08/2003",
                        "Gender": "Male",
                        "Issued On": "12/01/2021",
                        "Issuing Authority": "Unique Identification Authority of India (UIDAI)"
                    },
                    "producer": "UIDAI Official Generation Engine"
                },
                {
                    "type": DocumentType.ACADEMIC_CERTIFICATE,
                    "title": "Degree Certificate of Engineering",
                    "fields": {
                        "Candidate Name": "Aarav Sharma",
                        "Degree": "Bachelor of Technology (Computer Science)",
                        "Institution Name": "Delhi Technological University",
                        "Registration Number": "DTU/2020/CS/084",
                        "Year of Passing": "2024",
                        "Percentage Marks": "84.5%",
                        "Date of Issue": "20/06/2024"
                    },
                    "producer": "University Examination Controller Portal"
                },
                {
                    "type": DocumentType.INCOME_CERTIFICATE,
                    "title": "Annual Family Income Certificate",
                    "fields": {
                        "Beneficiary Name": "Aarav Sharma",
                        "Annual Family Income": "₹3,40,000",
                        "Certificate No": "REV/INC/2024/9842",
                        "Issue Date": "10/05/2024",
                        "Valid Up To": "2027-03-31",
                        "Issuing Authority": "Office of the Tehsildar, Revenue Department"
                    },
                    "producer": "State e-District Government Portal"
                }
            ]
        },
        {
            "code": "scenario_missing_doc",
            "ref_id": "APP-2026-MISSING-02",
            "name": "Rohan Deshmukh",
            "email": "rohan.d@example.edu",
            "category": "scholarship",
            "org": "National Means-cum-Merit Scholarship",
            "notes": "Scenario 2: Missing Document. Mandatory Academic Certificate absent from intake submission.",
            "documents": [
                {
                    "type": DocumentType.IDENTITY_DOCUMENT,
                    "title": "Government Identity Card (Aadhaar)",
                    "fields": {
                        "Applicant Name": "Rohan Deshmukh",
                        "Aadhaar Number": "4829 1102 7731",
                        "Date of Birth": "22/11/2004",
                        "Issued On": "05/03/2022",
                        "Issuing Authority": "UIDAI"
                    },
                    "producer": "UIDAI Official Generation Engine"
                }
            ]
        },
        {
            "code": "scenario_cross_mismatch",
            "ref_id": "APP-2026-MISMATCH-03",
            "name": "Vikramaditya Roy",
            "email": "v.roy@example.edu",
            "category": "admissions",
            "org": "Postgraduate Central Admission",
            "notes": "Scenario 3: Cross-Document Mismatch. Name and DOB contradict between Identity card and Degree.",
            "documents": [
                {
                    "type": DocumentType.IDENTITY_DOCUMENT,
                    "title": "Government Identity Card (Aadhaar)",
                    "fields": {
                        "Applicant Name": "Vikramaditya Roy",
                        "Aadhaar Number": "7719 3340 1289",
                        "Date of Birth": "18/05/2002",
                        "Issuing Authority": "UIDAI"
                    },
                    "producer": "UIDAI Official Generation Engine"
                },
                {
                    "type": DocumentType.ACADEMIC_CERTIFICATE,
                    "title": "Degree Certificate of Science",
                    "fields": {
                        "Candidate Name": "Bikram Roy Chowdhury",
                        "Date of Birth": "12/09/2000",
                        "Degree": "Bachelor of Science (Physics)",
                        "Institution Name": "Presidency University",
                        "Registration Number": "PU/2019/8821"
                    },
                    "producer": "University Examination Controller Portal"
                }
            ]
        },
        {
            "code": "scenario_expired_doc",
            "ref_id": "APP-2026-EXPIRED-04",
            "name": "Ananya Sen",
            "email": "ananya.sen@example.edu",
            "category": "scholarship",
            "org": "State Post-Matric Scholarship",
            "notes": "Scenario 4: Expired Document. Income certificate validity expired on 2023-03-31.",
            "documents": [
                {
                    "type": DocumentType.IDENTITY_DOCUMENT,
                    "title": "Government Identity Card",
                    "fields": {
                        "Applicant Name": "Ananya Sen",
                        "Aadhaar Number": "9921 4432 1098",
                        "Date of Birth": "09/02/2003",
                        "Issuing Authority": "UIDAI"
                    },
                    "producer": "UIDAI Official Generation Engine"
                },
                {
                    "type": DocumentType.ACADEMIC_CERTIFICATE,
                    "title": "Senior School Certificate Examination",
                    "fields": {
                        "Applicant Name": "Ananya Sen",
                        "Roll No": "1284920",
                        "Institution Name": "Central Board of Secondary Education",
                        "Marks Percentage": "91.2%"
                    },
                    "producer": "CBSE Examination System"
                },
                {
                    "type": DocumentType.INCOME_CERTIFICATE,
                    "title": "Annual Family Income Certificate",
                    "fields": {
                        "Beneficiary Name": "Ananya Sen",
                        "Annual Family Income": "₹2,10,000",
                        "Certificate No": "REV/2021/EXP-88",
                        "Issue Date": "15/01/2021",
                        "Expires On": "2023-03-31",
                        "Issuing Authority": "Revenue Directorate"
                    },
                    "producer": "e-District Portal"
                }
            ]
        },
        {
            "code": "scenario_suspicious_tampered",
            "ref_id": "APP-2026-SUSPICIOUS-05",
            "name": "Kabir Mehta",
            "email": "kabir.m@example.edu",
            "category": "recruitment",
            "org": "Faculty Technical Recruitment",
            "notes": "Scenario 5: Suspicious Document. Metadata exposes Canva/Photoshop tool modification and altered marks.",
            "documents": [
                {
                    "type": DocumentType.IDENTITY_DOCUMENT,
                    "title": "Government Identity Card",
                    "fields": {
                        "Applicant Name": "Kabir Mehta",
                        "Aadhaar Number": "3341 8892 0019",
                        "Date of Birth": "11/04/1998",
                        "Issuing Authority": "UIDAI"
                    },
                    "producer": "UIDAI Generation Engine"
                },
                {
                    "type": DocumentType.ACADEMIC_CERTIFICATE,
                    "title": "Master of Technology Certificate",
                    "fields": {
                        "Candidate Name": "Kabir Mehta",
                        "Degree": "Master of Technology (Artificial Intelligence)",
                        "Institution Name": "National Institute of Technology",
                        "Marks Percentage": "98.5%",
                        "Date of Issue": "15/08/2023"
                    },
                    "producer": "Canva Creative Studio Pro v2.4 (Modified PDF Stream)"
                }
            ]
        },
        {
            "code": "scenario_unavailable_issuer",
            "ref_id": "APP-2026-UNAVAILABLE-06",
            "name": "Fatima Zahra",
            "email": "fatima.z@example.edu",
            "category": "regulatory_licensing",
            "org": "Technical Professional Council",
            "notes": "Scenario 6: External Verification Unavailable. External authority API timed out; handles gracefully.",
            "documents": [
                {
                    "type": DocumentType.IDENTITY_DOCUMENT,
                    "title": "Government Identity Card",
                    "fields": {
                        "Applicant Name": "Fatima Zahra",
                        "Aadhaar Number": "6643 2210 9981",
                        "Date of Birth": "01/07/2001",
                        "Issuing Authority": "UIDAI"
                    },
                    "producer": "UIDAI Generation Engine"
                },
                {
                    "type": DocumentType.REGISTRATION_CERTIFICATE,
                    "title": "State Council Professional License",
                    "fields": {
                        "Applicant Name": "Fatima Zahra",
                        "Registration Number": "LIC/REG/99201",
                        "Institution Name": "State Council for Technical Professions",
                        "Date of Issue": "04/01/2024"
                    },
                    "producer": "Council Licensing Engine"
                }
            ]
        }
    ]

    for sc in scenarios:
        created_doc_ids = []
        created_docs_list = []
        app_doc_id = str(uuid.uuid4())

        for d_spec in sc["documents"]:
            file_name = f"{d_spec['type'].value}_{uuid.uuid4().hex[:6]}.pdf"
            file_path = os.path.join(storage_service.upload_dir, file_name)
            
            # Generate synthetic PDF
            create_synthetic_pdf(
                file_path=file_path,
                title=d_spec["title"],
                fields=d_spec["fields"],
                producer=d_spec.get("producer", "Gov Printing System")
            )

            with open(file_path, "rb") as f:
                content = f.read()

            sha = storage_service.calculate_sha256(content)
            doc_uuid = str(uuid.uuid4())

            # Run OCR & forensic pipeline
            ocr_res = ocr_service.process_document(file_path, "application/pdf", doc_uuid)
            auth_rep = forensic_service.run_authenticity_pipeline(file_path, "application/pdf", doc_uuid)
            dig_sig = digital_signature_service.inspect_digital_signature(file_path, "application/pdf")
            extracted = field_extractor_service.extract_fields(ocr_res.full_text, ocr_res.blocks, d_spec["type"])

            doc_record = {
                "_id": doc_uuid,
                "application_id": app_doc_id,
                "document_type": d_spec["type"].value,
                "metadata": {
                    "original_filename": f"{d_spec['title'].replace(' ', '_')}.pdf",
                    "stored_filename": file_name,
                    "file_path": file_path,
                    "preview_path": storage_service.get_preview_path(doc_uuid, 1),
                    "file_size_bytes": len(content),
                    "mime_type": "application/pdf",
                    "sha256_hash": sha,
                    "page_count": ocr_res.page_count,
                    "upload_timestamp": datetime.utcnow().isoformat(),
                    "version": 1
                },
                "status": DocumentStatus.ANALYZED.value,
                "ocr_confidence_score": ocr_res.avg_confidence,
                "quality_score": 95.0,
                "extracted_fields": {k: v.model_dump() for k, v in extracted.items()},
                "authenticity_findings": [f.model_dump() for f in auth_rep.findings],
                "digital_signature_info": dig_sig,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            await docs_col.insert_one(doc_record)
            created_doc_ids.append(doc_uuid)
            created_docs_list.append(doc_record)

        # Cross-Doc verification
        declared_details = {
            "applicant_name": sc["name"],
            "email": sc["email"],
            "category": sc["category"]
        }
        cross_doc_summary = cross_document_service.perform_cross_verification(
            app_doc_id, declared_details, created_docs_list
        )

        # Compliance
        comp_summary = compliance_engine.evaluate(
            app_doc_id, sc["category"], declared_details, created_docs_list, cross_doc_summary
        )

        # Authenticity Reports list
        auth_reports = []
        for d in created_docs_list:
            auth_rep = forensic_service.run_authenticity_pipeline(
                d["metadata"]["file_path"], "application/pdf", d["_id"]
            )
            auth_reports.append(auth_rep)

        # Risk assessment
        risk_assessment = risk_engine.assess(
            app_doc_id, created_docs_list, cross_doc_summary, comp_summary, auth_reports
        )

        app_status = "under_review"
        if sc["code"] == "scenario_clean":
            app_status = "approved"
            decision = {
                "action": "approved",
                "reason": "All mandatory credentials verified against statutory guidelines with zero contradictions.",
                "notes": "Verified by automated rule clearance and affirmative officer sign-off.",
                "decided_at": datetime.utcnow().isoformat()
            }
        elif sc["code"] == "scenario_missing_doc":
            app_status = "needs_evidence"
            decision = {
                "action": "request_evidence",
                "reason": "Mandatory Academic Transcript or Degree certificate is missing.",
                "notes": "Evidence request dispatched to applicant.",
                "decided_at": datetime.utcnow().isoformat()
            }
        else:
            decision = None

        app_record = {
            "_id": app_doc_id,
            "reference_id": sc["ref_id"],
            "applicant_name": sc["name"],
            "applicant_email": sc["email"],
            "applicant_phone": "+91 98765 43210",
            "category": sc["category"],
            "organization_or_institution": sc["org"],
            "declared_details": declared_details,
            "notes": sc["notes"],
            "status": app_status,
            "created_by": "user_demo_applicant",
            "document_ids": created_doc_ids,
            "review_priority_score": risk_assessment.priority_score,
            "review_priority_level": risk_assessment.priority_level.value,
            "verification_summary": {
                "cross_document": cross_doc_summary.model_dump(),
                "compliance": comp_summary.model_dump(),
                "risk_assessment": risk_assessment.model_dump()
            },
            "review_decision": decision,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        await apps_col.insert_one(app_record)

seed_service = seed_database
