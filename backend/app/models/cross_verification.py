from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class MatchStatus(str, Enum):
    EXACT_MATCH = "exact_match"
    FUZZY_MATCH = "fuzzy_match"
    MISMATCH = "mismatch"
    MISSING_IN_ONE = "missing_in_one"
    NOT_APPLICABLE = "not_applicable"

class CrossDocumentComparison(BaseModel):
    id: str
    field_key: str
    display_name: str
    doc1_id: str
    doc1_name: str
    doc1_type: str
    doc1_value: Optional[str] = None
    doc2_id: str
    doc2_name: str
    doc2_type: str
    doc2_value: Optional[str] = None
    match_status: MatchStatus
    similarity_score: float = 1.0  # 0.0 to 1.0
    contradiction_flag: bool = False
    evidence_reference: str
    suggested_resolution: str
    reviewed: bool = False

class CrossVerificationSummary(BaseModel):
    application_id: str
    total_checks: int = 0
    passed_checks: int = 0
    fuzzy_matches: int = 0
    mismatches: int = 0
    contradictions: int = 0
    comparisons: List[CrossDocumentComparison] = []
    overall_status: str = "passed"  # passed, attention_required, severe_mismatch
