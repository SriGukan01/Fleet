import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from backend.app.database import get_db
from backend.app.models.application import (
    CreateApplicationRequest,
    ApplicationResponse,
    ApplicationStatus,
    ApplicationCategory
)
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api/applications", tags=["Applications"])

def generate_reference_id(category: str) -> str:
    cat_code = category[:3].upper()
    hex_suffix = uuid.uuid4().hex[:6].upper()
    year = datetime.utcnow().year
    return f"APP-{year}-{cat_code}-{hex_suffix}"

@router.post("", response_model=ApplicationResponse)
async def create_application(
    req: CreateApplicationRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")
    audit_col = db.get_collection("audit_events")

    app_id = str(uuid.uuid4())
    ref_id = generate_reference_id(req.category.value)
    now = datetime.utcnow().isoformat()

    doc = {
        "_id": app_id,
        "reference_id": ref_id,
        "applicant_name": req.applicant_name.strip(),
        "applicant_email": req.applicant_email.strip().lower(),
        "applicant_phone": req.applicant_phone,
        "category": req.category.value,
        "organization_or_institution": req.organization_or_institution,
        "declared_details": req.declared_details or {"applicant_name": req.applicant_name},
        "notes": req.notes,
        "status": ApplicationStatus.SUBMITTED.value,
        "created_by": current_user.id,
        "document_ids": [],
        "review_priority_score": 0,
        "review_priority_level": "low_concern",
        "verification_summary": None,
        "review_decision": None,
        "created_at": now,
        "updated_at": now
    }
    await apps_col.insert_one(doc)

    # Log audit event
    await audit_col.insert_one({
        "_id": str(uuid.uuid4()),
        "timestamp": now,
        "actor_id": current_user.id,
        "actor_name": current_user.name,
        "actor_role": current_user.role.value,
        "action": "APPLICATION_CREATED",
        "entity_type": "application",
        "entity_id": app_id,
        "details": {"reference_id": ref_id, "category": req.category.value}
    })

    return ApplicationResponse(
        id=app_id,
        reference_id=ref_id,
        applicant_name=doc["applicant_name"],
        applicant_email=doc["applicant_email"],
        applicant_phone=doc["applicant_phone"],
        category=req.category,
        organization_or_institution=doc["organization_or_institution"],
        declared_details=doc["declared_details"],
        notes=doc["notes"],
        status=ApplicationStatus.SUBMITTED,
        created_by=current_user.id,
        document_ids=[],
        review_priority_score=0,
        review_priority_level="low_concern",
        created_at=now,
        updated_at=now
    )

@router.get("", response_model=List[ApplicationResponse])
async def list_applications(
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    priority_level: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")

    query = {}
    # If applicant, only view own applications
    if current_user.role.value == "applicant":
        query["created_by"] = current_user.id

    if category:
        query["category"] = category
    if status:
        query["status"] = status
    if priority_level:
        query["review_priority_level"] = priority_level

    cursor = apps_col.find(query).sort("created_at", -1)
    results = await cursor.to_list(100)

    # Filter search in memory if provided
    if search:
        s_term = search.lower().strip()
        results = [
            r for r in results
            if s_term in r.get("applicant_name", "").lower()
            or s_term in r.get("reference_id", "").lower()
            or s_term in r.get("applicant_email", "").lower()
        ]

    output = []
    for r in results:
        output.append(ApplicationResponse(
            id=r["_id"],
            reference_id=r["reference_id"],
            applicant_name=r["applicant_name"],
            applicant_email=r["applicant_email"],
            applicant_phone=r.get("applicant_phone"),
            category=ApplicationCategory(r["category"]),
            organization_or_institution=r.get("organization_or_institution"),
            declared_details=r.get("declared_details", {}),
            notes=r.get("notes"),
            status=ApplicationStatus(r.get("status", "submitted")),
            created_by=r.get("created_by", ""),
            document_ids=r.get("document_ids", []),
            review_priority_score=r.get("review_priority_score", 0),
            review_priority_level=r.get("review_priority_level", "low_concern"),
            verification_summary=r.get("verification_summary"),
            review_decision=r.get("review_decision"),
            created_at=r.get("created_at", ""),
            updated_at=r.get("updated_at", "")
        ))
    return output

@router.get("/{id}")
async def get_application_detail(
    id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")

    app = await apps_col.find_one({"_id": id})
    if not app:
        # Check by reference_id
        app = await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    # Fetch associated documents
    doc_ids = app.get("document_ids", [])
    documents = []
    if doc_ids:
        for d_id in doc_ids:
            d = await docs_col.find_one({"_id": d_id})
            if d:
                documents.append(d)

    app_data = dict(app)
    app_data["id"] = app["_id"]
    app_data["documents"] = documents
    return app_data

@router.delete("/{id}")
async def delete_application(
    id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can delete applications.")

    db = get_db()
    apps_col = db.get_collection("applications")
    await apps_col.delete_one({"_id": id})
    return {"message": "Application deleted successfully."}
