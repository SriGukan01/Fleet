from fastapi import APIRouter, Depends
from backend.app.database import get_db
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api/audit", tags=["Audit Trail"])

@router.get("")
async def get_audit_trail(limit: int = 50, current_user: UserResponse = Depends(get_current_user)):
    db = get_db()
    audit_col = db.get_collection("audit_events")
    cursor = audit_col.find().sort("timestamp", -1)
    logs = await cursor.to_list(limit)
    return logs
