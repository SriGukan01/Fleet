from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class IssuerVerificationStatus(str, Enum):
    VERIFIED = "verified"
    MISMATCH = "mismatch"
    UNAVAILABLE = "unavailable"
    SANDBOX_SIMULATED = "sandbox_simulated"

class IssuerRegistryEntry(BaseModel):
    id: str = Field(alias="_id")
    issuer_code: str  # e.g., "UIDAI_DIGILOCKER", "CBSE_REGISTRY", "AICTE_INST_DIR"
    name: str
    category: str  # Identity, Education, Taxation, Licensing
    api_endpoint: Optional[str] = None
    status: str = "operational"  # operational, degraded, offline
    is_sandbox: bool = True
    supported_doc_types: List[str] = []

    class Config:
        populate_by_name = True

class IssuerVerificationRequest(BaseModel):
    id: str = Field(alias="_id")
    application_id: str
    document_id: str
    issuer_code: str
    request_reference: str
    timestamp: str
    status: IssuerVerificationStatus
    fields_checked: List[str] = []
    evidence_returned: Dict[str, Any] = {}
    is_simulated: bool = False
    message: str

    class Config:
        populate_by_name = True
