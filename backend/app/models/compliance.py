from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class RuleStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    MISSING_EVIDENCE = "missing_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    NOT_APPLICABLE = "not_applicable"
    UNABLE_TO_DETERMINE = "unable_to_determine"
    REQUIRES_MANUAL_REVIEW = "requires_manual_review"

class RuleSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RegulatorySource(BaseModel):
    title: str
    authority: str  # e.g., AICTE, Ministry of Education, State Scholarship Portal
    section_or_clause: str
    effective_date: str
    source_url: Optional[str] = None
    excerpt: str

class ComplianceRule(BaseModel):
    id: str = Field(alias="_id")
    rule_id: str  # e.g. "RULE-AICTE-001"
    name: str
    jurisdiction: str  # AICTE / National / State
    application_type: str  # scholarship, admissions, recruitment, all
    policy_reference: RegulatorySource
    version: str = "1.0"
    severity: RuleSeverity = RuleSeverity.HIGH
    rule_type: str  # mandatory_documents, field_presence, expiry_check, threshold_constraint, cross_doc_consistency, digital_signature
    parameters: Dict[str, Any] = {}
    explanation: str
    remediation_instructions: str
    is_active: bool = True

    class Config:
        populate_by_name = True

class ComplianceEvaluationResult(BaseModel):
    rule_id: str
    rule_name: str
    status: RuleStatus
    severity: RuleSeverity
    policy_reference: RegulatorySource
    evidence_found: Optional[str] = None
    explanation: str
    remediation_instructions: Optional[str] = None
    reviewed: bool = False

class ComplianceSummary(BaseModel):
    application_id: str
    total_rules: int = 0
    compliant_count: int = 0
    non_compliant_count: int = 0
    missing_evidence_count: int = 0
    manual_review_count: int = 0
    overall_compliance_rate: float = 0.0  # percentage
    results: List[ComplianceEvaluationResult] = []
