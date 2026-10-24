import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from backend.app.database import get_db
from backend.app.models.audit import ReviewDecisionRequest
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api/applications", tags=["Human Review"])

@router.post("/{id}/review")
async def record_review_decision(
    id: str,
    req: ReviewDecisionRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.role.value not in ["officer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized. Only authorized Verification Officers and Administrators can record consequential decisions."
        )

    # Mandatory reason enforcement
    if not req.reason or len(req.reason.strip()) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A substantive mandatory reason (minimum 8 characters) is required for consequential adjudication."
        )

    db = get_db()
    apps_col = db.get_collection("applications")
    audit_col = db.get_collection("audit_events")

    app = await apps_col.find_one({"_id": id}) or await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    valid_actions = {
        "approve": "approved",
        "reject": "rejected",
        "request_evidence": "needs_evidence",
        "escalate": "under_review"
    }

    if req.action.lower() not in valid_actions:
        raise HTTPException(status_code=400, detail=f"Invalid review action '{req.action}'. Allowed: {list(valid_actions.keys())}")

    new_status = valid_actions[req.action.lower()]
    now = datetime.utcnow().isoformat()

    decision_record = {
        "action": req.action.lower(),
        "status_applied": new_status,
        "reason": req.reason.strip(),
        "notes": req.notes,
        "reviewed_by_id": current_user.id,
        "reviewed_by_name": current_user.name,
        "reviewed_by_role": current_user.role.value,
        "decided_at": now
    }

    await apps_col.update_one(
        {"_id": app["_id"]},
        {
            "$set": {
                "status": new_status,
                "review_decision": decision_record,
                "updated_at": now
            }
        }
    )

    # Immutable Audit Log
    await audit_col.insert_one({
        "_id": str(uuid.uuid4()),
        "timestamp": now,
        "actor_id": current_user.id,
        "actor_name": current_user.name,
        "actor_role": current_user.role.value,
        "action": f"APPLICATION_{req.action.upper()}",
        "entity_type": "application",
        "entity_id": app["_id"],
        "details": decision_record
    })

    return {
        "message": f"Application adjudication recorded as '{new_status}'.",
        "decision": decision_record
    }
