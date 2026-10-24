from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class DocumentType(str, Enum):
    IDENTITY_DOCUMENT = "identity_document"
    ACADEMIC_CERTIFICATE = "academic_certificate"
    MARKSHEET_TRANSCRIPT = "marksheet_transcript"
    INCOME_CERTIFICATE = "income_certificate"
    ADDRESS_PROOF = "address_proof"
    REGISTRATION_CERTIFICATE = "registration_certificate"
    SUPPORTING_DECLARATION = "supporting_declaration"
    OTHER = "other"

class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    FLAGGED = "flagged"
    VERIFIED = "verified"
    REJECTED = "rejected"

class DocumentMetadata(BaseModel):
    original_filename: str
    stored_filename: str
    file_path: str
    preview_path: Optional[str] = None
    file_size_bytes: int
    mime_type: str
    sha256_hash: str
    page_count: int = 1
    upload_timestamp: str
    version: int = 1

class DocumentInDB(BaseModel):
    id: str = Field(alias="_id")
    application_id: str
    document_type: DocumentType
    metadata: DocumentMetadata
    status: DocumentStatus = DocumentStatus.UPLOADED
    ocr_confidence_score: float = 0.0
    quality_score: float = 100.0
    extracted_fields: Dict[str, Any] = {}
    authenticity_findings: List[Dict[str, Any]] = []
    digital_signature_info: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str

    class Config:
        populate_by_name = True

class DocumentResponse(BaseModel):
    id: str
    application_id: str
    document_type: DocumentType
    metadata: DocumentMetadata
    status: DocumentStatus
    ocr_confidence_score: float
    quality_score: float
    extracted_fields: Dict[str, Any]
    authenticity_findings: List[Dict[str, Any]]
    digital_signature_info: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str
