import uuid
from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from backend.app.database import get_db
from backend.app.services.cross_doc_service import cross_document_service
from backend.app.services.compliance_engine import compliance_engine
from backend.app.services.risk_engine import risk_engine
from backend.app.services.forensic_service import forensic_service
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api/applications", tags=["Verification"])

class RequestEvidencePayload(BaseModel):
    requested_documents: List[str]
    message: str
    deadline_days: int = 7

@router.post("/{id}/verify")
async def trigger_application_verification(
    id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")
    rules_col = db.get_collection("compliance_rules")
    audit_col = db.get_collection("audit_events")

    app = await apps_col.find_one({"_id": id})
    if not app:
        app = await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    # Fetch all documents
    doc_ids = app.get("document_ids", [])
    documents = []
    for d_id in doc_ids:
        d = await docs_col.find_one({"_id": d_id})
        if d:
            documents.append(d)

    # 1. Cross-Document Verification
    declared = app.get("declared_details", {})
    if "applicant_name" not in declared and "applicant_name" in app:
        declared["applicant_name"] = app["applicant_name"]
    
    cross_doc_summary = cross_document_service.perform_cross_verification(
        app["_id"], declared, documents
    )

    # 2. Compliance Evaluation against active rules
    rules_cursor = rules_col.find({"is_active": True})
    active_rules = await rules_cursor.to_list(100)
    
    comp_summary = compliance_engine.evaluate(
        app["_id"], app.get("category", "scholarship"), declared, documents, cross_doc_summary, active_rules
    )

    # 3. Authenticity Analysis Syntheses
    auth_reports = []
    for d in documents:
        auth_rep = forensic_service.run_authenticity_pipeline(
            d["metadata"]["file_path"], d["metadata"]["mime_type"], d["_id"]
        )
        auth_reports.append(auth_rep)

    # 4. Explainable Risk & Review Priority Assessment
    risk_assessment = risk_engine.assess(
        app["_id"], documents, cross_doc_summary, comp_summary, auth_reports
    )

    # Save to application
    verification_summary = {
        "cross_document": cross_doc_summary.model_dump(),
        "compliance": comp_summary.model_dump(),
        "risk_assessment": risk_assessment.model_dump(),
        "verified_at": datetime.utcnow().isoformat()
    }

    await apps_col.update_one(
        {"_id": app["_id"]},
        {
            "$set": {
                "review_priority_score": risk_assessment.priority_score,
                "review_priority_level": risk_assessment.priority_level.value,
                "verification_summary": verification_summary,
                "status": "under_review" if app.get("status") in ["submitted", "processing"] else app.get("status"),
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    )

    # Record Audit event
    await audit_col.insert_one({
        "_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "actor_id": current_user.id,
        "actor_name": current_user.name,
        "actor_role": current_user.role.value,
        "action": "VERIFICATION_PIPELINE_EXECUTED",
        "entity_type": "application",
        "entity_id": app["_id"],
        "details": {
            "priority_score": risk_assessment.priority_score,
            "priority_level": risk_assessment.priority_level.value,
            "contradictions": cross_doc_summary.contradictions,
            "non_compliant_rules": comp_summary.non_compliant_count
        }
    })

    return {
        "application_id": app["_id"],
        "reference_id": app["reference_id"],
        "review_priority_score": risk_assessment.priority_score,
        "review_priority_level": risk_assessment.priority_level.value,
        "verification_summary": verification_summary
    }

@router.get("/{id}/verification")
async def get_verification_summary(
    id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")
    app = await apps_col.find_one({"_id": id}) or await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")
    
    return {
        "application_id": app["_id"],
        "reference_id": app["reference_id"],
        "status": app.get("status"),
        "review_priority_score": app.get("review_priority_score", 0),
        "review_priority_level": app.get("review_priority_level", "low_concern"),
        "verification_summary": app.get("verification_summary")
    }

@router.post("/{id}/request-evidence")
async def request_additional_evidence(
    id: str,
    payload: RequestEvidencePayload,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")
    audit_col = db.get_collection("audit_events")

    app = await apps_col.find_one({"_id": id}) or await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    now = datetime.utcnow().isoformat()
    evidence_req_obj = {
        "requested_by": current_user.name,
        "requested_at": now,
        "documents": payload.requested_documents,
        "message": payload.message,
        "deadline_days": payload.deadline_days
    }

    await apps_col.update_one(
        {"_id": app["_id"]},
        {
            "$set": {
                "status": "needs_evidence",
                "evidence_request": evidence_req_obj,
                "updated_at": now
            }
        }
    )

    await audit_col.insert_one({
        "_id": str(uuid.uuid4()),
        "timestamp": now,
        "actor_id": current_user.id,
        "actor_name": current_user.name,
        "actor_role": current_user.role.value,
        "action": "EVIDENCE_REQUESTED",
        "entity_type": "application",
        "entity_id": app["_id"],
        "details": evidence_req_obj
    })

    return {"message": "Evidence request registered and notification queued.", "request": evidence_req_obj}
