from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

class FindingSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuthenticityFinding(BaseModel):
    id: str
    title: str
    category: str  # pdf_metadata, image_consistency, compression_ela, signature_seal, digital_signature, text_ocr_mismatch, template_comparison
    severity: FindingSeverity
    evidence: str
    page_number: int = 1
    region: Optional[Dict[str, float]] = None  # {x, y, width, height}
    detection_method: str
    confidence_or_metric: Optional[str] = None  # e.g., "Sharpness variance: 42.1 (Blur threshold: 100)" or "ELA divergence: 28%"
    explanation: str
    recommended_action: str
    human_review_required: bool = True
    limitations: Optional[str] = "Automated heuristic indicator. Does not constitute conclusive proof of fraud."

class AuthenticityReport(BaseModel):
    document_id: str
    overall_status: str  # no_suspicious_indicators, review_required, anomalies_detected
    findings: List[AuthenticityFinding] = []
    checks_performed: List[str] = []
    checks_unavailable: List[str] = []
    tampering_risk_score: int = 0  # 0 to 100
    digital_signature_verified: Optional[bool] = None
