from fastapi import APIRouter
from backend.app.database import get_db
from backend.app.seed.seed_data import seed_database

router = APIRouter(prefix="/api/scenarios", tags=["Demo Scenarios"])

SCENARIO_METADATA = [
    {
        "id": "scenario_clean",
        "title": "Scenario 1: Clean Application",
        "reference_id": "APP-2026-CLEAN-01",
        "applicant": "Aarav Sharma",
        "category": "Scholarship",
        "expected_score": 0,
        "expected_level": "Low Concern (Fast-Track)",
        "expected_status": "Approved",
        "description": "Complete, valid identity and degree credentials. All mandatory documents present, cross-document fields agree 100%, and regulatory income ceiling is satisfied.",
        "key_checks": ["Aadhaar Match: Passed", "Degree Ingestion: 84.5%", "Income Ceiling (<= 8L): ₹3.4L Passed"]
    },
    {
        "id": "scenario_missing_doc",
        "title": "Scenario 2: Missing Mandatory Document",
        "reference_id": "APP-2026-MISSING-02",
        "applicant": "Rohan Deshmukh",
        "category": "Scholarship",
        "expected_score": 25,
        "expected_level": "Moderate Concern",
        "expected_status": "Needs Evidence",
        "description": "Mandatory academic certificate was not uploaded during intake submission, triggering Rule AICTE-MANDATORY-DOCS breach.",
        "key_checks": ["Rule Breach: AICTE-MANDATORY-DOCS", "Missing: academic_certificate", "Action: Request Evidence"]
    },
    {
        "id": "scenario_cross_mismatch",
        "title": "Scenario 3: Cross-Document Discrepancy",
        "reference_id": "APP-2026-MISMATCH-03",
        "applicant": "Vikramaditya Roy",
        "category": "Admissions",
        "expected_score": 65,
        "expected_level": "High Concern",
        "expected_status": "Under Review",
        "description": "Applicant Name and Date of Birth conflict between official Aadhaar and Degree record (Vikramaditya Roy vs Bikram Roy Chowdhury).",
        "key_checks": ["Name Contradiction: Flagged", "DOB Mismatch: 18/05/2002 vs 12/09/2000", "Resolution: Identity Affidavit Required"]
    },
    {
        "id": "scenario_expired_doc",
        "title": "Scenario 4: Expired Validity Certificate",
        "reference_id": "APP-2026-EXPIRED-04",
        "applicant": "Ananya Sen",
        "category": "Scholarship",
        "expected_score": 50,
        "expected_level": "High Concern",
        "expected_status": "Under Review",
        "description": "Income certificate has validity period ending 2023-03-31, failing current financial year regulatory requirement.",
        "key_checks": ["Rule Breach: INCOME-VALIDITY-PERIOD", "Expired On: 2023-03-31", "Action: Submit Renewed Certificate"]
    },
    {
        "id": "scenario_suspicious_tampered",
        "title": "Scenario 5: Suspicious Document / Forensics",
        "reference_id": "APP-2026-SUSPICIOUS-05",
        "applicant": "Kabir Mehta",
        "category": "Recruitment",
        "expected_score": 85,
        "expected_level": "Critical Review Required",
        "expected_status": "Under Review",
        "description": "Altered Master's transcript with embedded editing tool metadata (Canva Studio Pro), ELA compression divergence, and inflated marks.",
        "key_checks": ["Forensic Alert: Graphic Editor Metadata", "ELA Divergence: Anomaly Detected", "Priority: Senior Scrutiny Queue"]
    },
    {
        "id": "scenario_unavailable_issuer",
        "title": "Scenario 6: External Issuer API Unavailable",
        "reference_id": "APP-2026-UNAVAILABLE-06",
        "applicant": "Fatima Zahra",
        "category": "Regulatory Licensing",
        "expected_score": 20,
        "expected_level": "Moderate Concern",
        "expected_status": "Under Review",
        "description": "External licensing authority server timed out. System gracefully marks check as 'Unavailable' rather than failing the applicant.",
        "key_checks": ["Issuer Call: HTTP 504 Timeout", "Status: Graceful Fallback", "No False Fraud Claim"]
    }
]

@router.get("")
async def list_demo_scenarios():
    return SCENARIO_METADATA

@router.post("/reload")
async def reload_demo_data():
    db = get_db()
    # Re-seed if needed
    await seed_database()
    return {"message": "Demonstration dataset refreshed successfully with 6 synthetic scenarios."}
