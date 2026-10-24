from typing import List, Dict, Any, Optional
from backend.app.models.risk import (
    ReviewPriorityAssessment,
    ReviewPriorityLevel,
    RiskSignal
)
from backend.app.models.compliance import ComplianceSummary, RuleStatus
from backend.app.models.cross_verification import CrossVerificationSummary
from backend.app.models.authenticity import AuthenticityReport

class RiskEngine:
    def __init__(self):
        # Configurable signal point weights (capped total)
        self.weights = {
            "cross_doc_contradiction": 35,
            "tampering_ela_or_editor": 30,
            "expired_mandatory_doc": 25,
            "missing_mandatory_doc": 20,
            "unusual_metadata_divergence": 10,
            "low_ocr_quality_blur": 15,
            "issuer_unverified": 10,
            "minor_fuzzy_name_variation": 10
        }

    def assess(
        self,
        application_id: str,
        documents: List[Dict[str, Any]],
        cross_doc: Optional[CrossVerificationSummary],
        compliance: Optional[ComplianceSummary],
        authenticity_reports: List[AuthenticityReport]
    ) -> ReviewPriorityAssessment:
        signals: List[RiskSignal] = []
        det_violations = 0
        prob_anomalies = 0

        # 1. Evaluate Cross-Document Contradictions
        if cross_doc:
            if cross_doc.contradictions > 0:
                det_violations += cross_doc.contradictions
                pts = min(40, cross_doc.contradictions * self.weights["cross_doc_contradiction"])
                signals.append(RiskSignal(
                    category="cross_doc_contradiction",
                    title="Cross-Document Discrepancy Detected",
                    weight=self.weights["cross_doc_contradiction"],
                    contribution_points=pts,
                    evidence=f"{cross_doc.contradictions} critical field contradiction(s) between uploaded records.",
                    explanation="Information declared by applicant or extracted from primary ID differs significantly from supporting academic certificates."
                ))
            elif cross_doc.fuzzy_matches > 0:
                signals.append(RiskSignal(
                    category="minor_fuzzy_name_variation",
                    title="Minor Name Spelling / Initials Variation",
                    weight=self.weights["minor_fuzzy_name_variation"],
                    contribution_points=10,
                    evidence=f"{cross_doc.fuzzy_matches} fuzzy matching field(s) require human eyes.",
                    explanation="Slight variation in name spelling or initials between records."
                ))

        # 2. Evaluate Compliance Violations
        if compliance:
            for r in compliance.results:
                if r.status == RuleStatus.NON_COMPLIANT:
                    det_violations += 1
                    signals.append(RiskSignal(
                        category="regulatory_rule_violation",
                        title=f"Breach of Rule: {r.rule_name}",
                        weight=25,
                        contribution_points=25,
                        evidence=r.evidence_found or "Rule condition unmet.",
                        explanation=r.explanation
                    ))
                elif r.status == RuleStatus.MISSING_EVIDENCE:
                    det_violations += 1
                    signals.append(RiskSignal(
                        category="missing_mandatory_doc",
                        title=f"Mandatory Evidence Absent: {r.rule_name}",
                        weight=self.weights["missing_mandatory_doc"],
                        contribution_points=20,
                        evidence=r.evidence_found or "Required evidence document missing.",
                        explanation=r.explanation
                    ))

        # 3. Evaluate Forensics & Tampering Anomaly Reports
        for auth in authenticity_reports:
            for finding in auth.findings:
                if finding.severity.value in ["critical", "high"]:
                    prob_anomalies += 1
                    # Avoid double counting if already added
                    if not any(s.title == finding.title for s in signals):
                        signals.append(RiskSignal(
                            category=finding.category,
                            title=finding.title,
                            weight=self.weights.get("tampering_ela_or_editor", 25),
                            contribution_points=25,
                            evidence=finding.evidence,
                            explanation=finding.explanation
                        ))
                elif finding.severity.value == "medium":
                    if not any(s.title == finding.title for s in signals):
                        signals.append(RiskSignal(
                            category=finding.category,
                            title=finding.title,
                            weight=10,
                            contribution_points=10,
                            evidence=finding.evidence,
                            explanation=finding.explanation
                        ))

        # Sum total points (bounded 0 to 100)
        total_points = sum(s.contribution_points for s in signals)
        priority_score = min(100, max(0, total_points))

        # Tier assignment
        if priority_score >= 70:
            level = ReviewPriorityLevel.CRITICAL_REVIEW_REQUIRED
            queue = "Senior Officer & Forensic Scrutiny Queue"
        elif priority_score >= 45:
            level = ReviewPriorityLevel.HIGH_CONCERN
            queue = "Standard Verification Officer Queue (Elevated Priority)"
        elif priority_score >= 20:
            level = ReviewPriorityLevel.MODERATE_CONCERN
            queue = "Standard Verification Officer Queue"
        else:
            level = ReviewPriorityLevel.LOW_CONCERN
            queue = "Fast-Track Automated Clearance Queue"

        return ReviewPriorityAssessment(
            application_id=application_id,
            priority_score=priority_score,
            priority_level=level,
            recommended_queue=queue,
            signals=signals,
            deterministic_violations_count=det_violations,
            probabilistic_anomalies_count=prob_anomalies,
            model_version="v2.1-hybrid-explainable-weights"
        )

risk_engine = RiskEngine()
