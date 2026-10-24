from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class AuditEvent(BaseModel):
    id: str = Field(alias="_id")
    timestamp: str
    actor_id: str
    actor_name: str
    actor_role: str
    action: str  # e.g., APPLICATION_CREATED, DOCUMENT_UPLOADED, VERIFICATION_EXECUTED, STATUS_CHANGED, EVIDENCE_REQUESTED, REPORT_GENERATED
    entity_type: str  # application, document, rule, user, verification
    entity_id: str
    details: Dict[str, Any] = {}
    ip_address: Optional[str] = "127.0.0.1"

    class Config:
        populate_by_name = True

class ReviewDecisionRequest(BaseModel):
    action: str  # approve, reject, request_evidence, escalate
    reason: str  # Mandatory justification
    notes: Optional[str] = None
    requested_evidence_types: Optional[list[str]] = None
    target_stage: Optional[str] = None
