from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class ReviewPriorityLevel(str, Enum):
    LOW_CONCERN = "low_concern"
    MODERATE_CONCERN = "moderate_concern"
    HIGH_CONCERN = "high_concern"
    CRITICAL_REVIEW_REQUIRED = "critical_review_required"

class RiskSignal(BaseModel):
    category: str  # missing_mandatory, cross_doc_contradiction, metadata_anomaly, compression_tampering, expired_validity, low_ocr_quality, issuer_unverified
    title: str
    weight: float
    contribution_points: int
    evidence: str
    explanation: str

class ReviewPriorityAssessment(BaseModel):
    application_id: str
    priority_score: int  # 0 to 100
    priority_level: ReviewPriorityLevel
    recommended_queue: str  # Fast-Track Approval, Standard Queue, Senior Officer Review, Fraud Investigation Unit
    signals: List[RiskSignal] = []
    deterministic_violations_count: int = 0
    probabilistic_anomalies_count: int = 0
    model_version: str = "v1.2-weighted-hybrid"
    disclaimer: str = "This score indicates review urgency and routing priority. It is not an automated conclusion or legal probability of fraud."
