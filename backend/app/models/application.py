from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class ApplicationCategory(str, Enum):
    SCHOLARSHIP = "scholarship"
    ADMISSIONS = "admissions"
    RECRUITMENT = "recruitment"
    REGULATORY_LICENSING = "regulatory_licensing"

class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    UNDER_REVIEW = "under_review"
    NEEDS_EVIDENCE = "needs_evidence"
    APPROVED = "approved"
    REJECTED = "rejected"

class ApplicationBase(BaseModel):
    reference_id: str
    applicant_name: str
    applicant_email: str
    applicant_phone: Optional[str] = None
    category: ApplicationCategory = ApplicationCategory.SCHOLARSHIP
    organization_or_institution: Optional[str] = None
    declared_details: Dict[str, Any] = {}
    notes: Optional[str] = None

class CreateApplicationRequest(BaseModel):
    applicant_name: str
    applicant_email: str
    applicant_phone: Optional[str] = None
    category: ApplicationCategory
    organization_or_institution: Optional[str] = None
    declared_details: Dict[str, Any] = {}
    notes: Optional[str] = None

class ApplicationInDB(ApplicationBase):
    id: str = Field(alias="_id")
    status: ApplicationStatus = ApplicationStatus.SUBMITTED
    created_by: str  # user_id
    document_ids: List[str] = []
    review_priority_score: int = 0
    review_priority_level: str = "low_concern"  # low_concern, moderate_concern, high_concern, critical_review_required
    verification_summary: Optional[Dict[str, Any]] = None
    review_decision: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str

    class Config:
        populate_by_name = True

class ApplicationResponse(ApplicationBase):
    id: str
    status: ApplicationStatus
    created_by: str
    document_ids: List[str] = []
    review_priority_score: int = 0
    review_priority_level: str = "low_concern"
    verification_summary: Optional[Dict[str, Any]] = None
    review_decision: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str
