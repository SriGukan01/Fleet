# VERITRUST AI — Database Schema & Data Models
## Persistence Specifications (MongoDB Atlas / Local Document Store)
### AICTE SIH26261 | Smart Automation

---

## 1. Overview & Dual-Persistence Architecture

VERITRUST AI supports two persistence backends:
1. **MongoDB Atlas (Production & Cloud Mode)**: Configured via `MONGODB_URL` in `.env`. Uses the async `motor` driver.
2. **Local Document Store (Resilient Fallback Mode)**: Activated automatically if `MONGODB_URL` is omitted or network access is offline. Persists document collections into `backend/data/db.json` with zero data loss across restarts.

---

## 2. Collection Schemas

### `users`
```json
{
  "_id": "user_demo_officer",
  "email": "officer@veritrust.ai",
  "name": "Dr. Priya Raman (Verification Officer)",
  "role": "officer", // "applicant" | "officer" | "admin"
  "organization": "AICTE Scrutiny Cell",
  "hashed_password": "$2b$12$...",
  "is_active": true,
  "is_demo": true,
  "created_at": "2026-10-20T10:00:00.000Z"
}
```

### `applications`
```json
{
  "_id": "uuid-string",
  "reference_id": "APP-2026-SCH-A93F2B",
  "applicant_name": "Aarav Sharma",
  "applicant_email": "aarav.sharma@example.edu",
  "applicant_phone": "+91 98765 43210",
  "category": "scholarship", // "scholarship" | "admissions" | "recruitment" | "regulatory_licensing"
  "organization_or_institution": "Delhi Technological University",
  "declared_details": {
    "applicant_name": "Aarav Sharma",
    "annual_income": "₹3,40,000"
  },
  "notes": "Intake notes",
  "status": "approved", // "submitted" | "under_review" | "needs_evidence" | "approved" | "rejected"
  "created_by": "user_demo_applicant",
  "document_ids": ["doc_uuid_1", "doc_uuid_2"],
  "review_priority_score": 0, // 0 to 100
  "review_priority_level": "low_concern", // "low_concern" | "moderate_concern" | "high_concern" | "critical_review_required"
  "verification_summary": {
    "cross_document": {},
    "compliance": {},
    "risk_assessment": {}
  },
  "review_decision": {
    "action": "approved",
    "reason": "All mandatory documents verified against AICTE guidelines.",
    "reviewed_by_name": "Dr. Priya Raman",
    "decided_at": "2026-10-20T10:30:00.000Z"
  },
  "created_at": "2026-10-20T10:00:00.000Z",
  "updated_at": "2026-10-20T10:30:00.000Z"
}
```

### `documents`
```json
{
  "_id": "doc_uuid",
  "application_id": "app_uuid",
  "document_type": "identity_document",
  "metadata": {
    "original_filename": "Aadhaar_Card.pdf",
    "stored_filename": "unique_stored_file.pdf",
    "file_path": "/storage/uploads/unique_stored_file.pdf",
    "preview_path": "/storage/previews/doc_uuid_page_1.png",
    "file_size_bytes": 1048576,
    "mime_type": "application/pdf",
    "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "page_count": 1,
    "upload_timestamp": "2026-10-20T10:00:00.000Z",
    "version": 1
  },
  "status": "analyzed",
  "ocr_confidence_score": 0.96,
  "quality_score": 95.0,
  "extracted_fields": {
    "applicant_name": {
      "field_key": "applicant_name",
      "display_name": "Applicant Name",
      "value": "Aarav Sharma",
      "normalized_value": "AARAV SHARMA",
      "confidence": 0.96,
      "page_number": 1,
      "bounding_box": { "x": 15.2, "y": 24.5, "width": 38.0, "height": 4.5 }
    }
  },
  "authenticity_findings": [],
  "digital_signature_info": {
    "has_digital_signature": false,
    "status": "no_signature_present"
  }
}
```

### `compliance_rules`
```json
{
  "_id": "rule_aicte_001",
  "rule_id": "AICTE-MANDATORY-DOCS",
  "name": "Mandatory Submission of Identity & Academic Records",
  "jurisdiction": "AICTE / National",
  "application_type": "all",
  "policy_reference": {
    "title": "AICTE Approval Process Handbook (Section 2.4)",
    "authority": "All India Council for Technical Education",
    "section_or_clause": "Clause 2.4.1",
    "effective_date": "2024-04-01",
    "source_url": "https://www.aicte-india.org/approval-process",
    "excerpt": "Mandatory verification norms requiring primary government identity and qualifying transcript."
  },
  "version": "1.0",
  "severity": "critical",
  "rule_type": "mandatory_documents",
  "parameters": {
    "required_document_types": ["identity_document", "academic_certificate"]
  },
  "explanation": "Validates minimum mandatory credential presence.",
  "is_active": true
}
```

### `audit_events`
```json
{
  "_id": "audit_uuid",
  "timestamp": "2026-10-20T10:30:00.000Z",
  "actor_id": "user_demo_officer",
  "actor_name": "Dr. Priya Raman",
  "actor_role": "officer",
  "action": "APPLICATION_APPROVED",
  "entity_type": "application",
  "entity_id": "app_uuid",
  "details": {
    "action": "approved",
    "reason": "All documents verified against AICTE guidelines."
  },
  "ip_address": "127.0.0.1"
}
```
