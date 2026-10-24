from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.database import get_db
from backend.app.services.issuer_service import issuer_service
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api/issuers", tags=["Issuer Integrations"])

class VerifyIssuerRequest(BaseModel):
    application_id: str
    document_id: str
    issuer_code: str

@router.get("")
async def list_registered_issuers():
    db = get_db()
    issuers_col = db.get_collection("issuer_registry")
    issuers = await issuers_col.find().to_list(100)
    if not issuers:
        return [i.model_dump(by_alias=True) for i in issuer_service.get_registered_issuers()]
    return issuers

@router.post("/verify")
async def verify_against_issuer(
    req: VerifyIssuerRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    docs_col = db.get_collection("documents")
    doc = await docs_col.find_one({"_id": req.document_id})
    extracted = doc.get("extracted_fields", {}) if doc else {}

    result = issuer_service.verify_against_issuer(
        req.application_id, req.document_id, req.issuer_code, extracted
    )
    return result.model_dump(by_alias=True)
