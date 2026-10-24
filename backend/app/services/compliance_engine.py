import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.app.models.compliance import (
    ComplianceRule,
    ComplianceEvaluationResult,
    ComplianceSummary,
    RuleStatus,
    RuleSeverity,
    RegulatorySource
)

# Realistic demonstration rules grounded in AICTE / Government Guidelines
DEFAULT_RULES: List[Dict[str, Any]] = [
    {
        "_id": "rule_aicte_001",
        "rule_id": "AICTE-MANDATORY-DOCS",
        "name": "Mandatory Submission of Identity & Academic Records",
        "jurisdiction": "AICTE / National",
        "application_type": "all",
        "policy_reference": {
            "title": "AICTE Approval Process Handbook (Section 2.4 - Document Verification Norms)",
            "authority": "All India Council for Technical Education (AICTE)",
            "section_or_clause": "Clause 2.4.1 (Mandatory Scrutiny Requirements)",
            "effective_date": "2024-04-01",
            "source_url": "https://www.aicte-india.org/approval-process",
            "excerpt": "Every candidate applying for scholarship or admission scrutiny must submit verified government identity proof along with qualifying degree/marksheet certificates."
        },
        "version": "1.0",
        "severity": "critical",
        "rule_type": "mandatory_documents",
        "parameters": {
            "required_document_types": ["identity_document", "academic_certificate"]
        },
        "explanation": "Validates that applicant has submitted at minimum an identity document and an academic certificate.",
        "remediation_instructions": "Upload the missing mandatory document (Aadhaar/Identity card or Academic transcript).",
        "is_active": True
    },
    {
        "_id": "rule_aicte_002",
        "rule_id": "INCOME-VALIDITY-PERIOD",
        "name": "Income Certificate Current Financial Year Validity",
        "jurisdiction": "Central / State Welfare Directorate",
        "application_type": "scholarship",
        "policy_reference": {
            "title": "National Scholarship Portal (NSP) Operational Guidelines",
            "authority": "Ministry of Electronics and Information Technology (MeitY)",
            "section_or_clause": "Section 4(b) - Income Eligibility Criteria",
            "effective_date": "2023-08-15",
            "source_url": "https://scholarships.gov.in/guidelines",
            "excerpt": "Income certificates submitted for fee waiver or scholarship must be issued within the valid financial year and cannot be expired at the time of application submission."
        },
        "version": "1.2",
        "severity": "high",
        "rule_type": "expiry_check",
        "parameters": {
            "target_document_type": "income_certificate",
            "max_age_months": 12
        },
        "explanation": "Ensures income certificates reflect current financial eligibility and have not expired.",
        "remediation_instructions": "Submit a renewed income certificate issued by a competent Revenue Authority (Tehsildar / SDO).",
        "is_active": True
    },
    {
        "_id": "rule_aicte_003",
        "rule_id": "INCOME-THRESHOLD-CEILING",
        "name": "Family Annual Income Ceiling Compliance",
        "jurisdiction": "AICTE Pragati / Saksham Scheme",
        "application_type": "scholarship",
        "policy_reference": {
            "title": "AICTE Pragati & Saksham Scholarship Guidelines",
            "authority": "AICTE Welfare Bureau",
            "section_or_clause": "Clause 3.1 - Income Ceiling",
            "effective_date": "2023-01-01",
            "source_url": "https://www.aicte-india.org/schemes/students-development-schemes",
            "excerpt": "Total family annual income from all sources should not exceed INR 8,00,000/- per annum for the grant of scholarship."
        },
        "version": "1.0",
        "severity": "high",
        "rule_type": "threshold_constraint",
        "parameters": {
            "field": "annual_income",
            "operator": "lte",
            "threshold_value": 800000
        },
        "explanation": "Verifies that certified annual family income does not exceed ₹8,00,000 threshold.",
        "remediation_instructions": "If income exceeds the scheme cap, the applicant is ineligible for this specific income-restricted grant.",
        "is_active": True
    },
    {
        "_id": "rule_aicte_004",
        "rule_id": "NAME-CONSISTENCY-CHECK",
        "name": "Cross-Document Legal Identity Consistency",
        "jurisdiction": "AICTE / Statutory Standard",
        "application_type": "all",
        "policy_reference": {
            "title": "General Standards for Academic Credentials Scrutiny",
            "authority": "AICTE & UGC Academic Cell",
            "section_or_clause": "Section 5 - Identity Reconcilement",
            "effective_date": "2023-06-01",
            "source_url": "https://www.ugc.gov.in/guidelines",
            "excerpt": "The name of the applicant on all academic credentials must be reconcilable with the primary identity record. Discrepancies without gazette notification require administrative hold."
        },
        "version": "1.1",
        "severity": "high",
        "rule_type": "cross_doc_consistency",
        "parameters": {
            "minimum_similarity": 0.80
        },
        "explanation": "Detects identity mismatches between official certificates and declared applicant credentials.",
        "remediation_instructions": "Upload Gazette notification, marriage certificate, or an affidavit explaining the name variation.",
        "is_active": True
    },
    {
        "_id": "rule_aicte_005",
        "rule_id": "MINIMUM-QUALIFYING-PERCENTAGE",
        "name": "Minimum Qualifying Examination Percentage",
        "jurisdiction": "AICTE Technical Education Norms",
        "application_type": "admissions",
        "policy_reference": {
            "title": "AICTE Approval Process Handbook (Entry Qualification Standards)",
            "authority": "AICTE Academic Board",
            "section_or_clause": "Appendix 1 - Entry Level Percentages",
            "effective_date": "2024-01-01",
            "source_url": "https://www.aicte-india.org",
            "excerpt": "Passed 10+2 examination with minimum 45% marks (40% for candidates belonging to reserved category) in the above subjects taken together."
        },
        "version": "1.0",
        "severity": "medium",
        "rule_type": "threshold_constraint",
        "parameters": {
            "field": "marks_percentage",
            "operator": "gte",
            "threshold_value": 45.0
        },
        "explanation": "Verifies that academic transcript confirms minimum entry threshold of 45%.",
        "remediation_instructions": "Candidate must meet the minimum qualifying marks specified by the regulatory body.",
        "is_active": True
    }
]

class ComplianceEngine:
    def __init__(self):
        pass

    def evaluate(
        self,
        application_id: str,
        application_type: str,
        declared_details: Dict[str, Any],
        documents: List[Dict[str, Any]],
        cross_doc_summary: Optional[Any] = None,
        rules: Optional[List[Dict[str, Any]]] = None
    ) -> ComplianceSummary:
        if rules is None:
            rules = DEFAULT_RULES

        results: List[ComplianceEvaluationResult] = []
        compliant_count = 0
        non_compliant_count = 0
        missing_evidence_count = 0
        manual_review_count = 0

        # Index submitted doc types
        submitted_doc_types = set(d.get("document_type") for d in documents)
        all_extracted_fields: Dict[str, Any] = {}
        for d in documents:
            for k, f_val in d.get("extracted_fields", {}).items():
                all_extracted_fields[k] = f_val

        for r in rules:
            if not r.get("is_active", True):
                continue
            
            # Check applicability
            rule_app_type = r.get("application_type", "all")
            if rule_app_type != "all" and rule_app_type != application_type:
                continue

            policy_ref = RegulatorySource(**r["policy_reference"])
            rule_id = r["rule_id"]
            rule_name = r["name"]
            rule_type = r.get("rule_type")
            severity = RuleSeverity(r.get("severity", "high"))
            params = r.get("parameters", {})

            # Evaluation logic by rule_type
            if rule_type == "mandatory_documents":
                required = params.get("required_document_types", [])
                missing = [req for req in required if req not in submitted_doc_types]
                if not missing:
                    compliant_count += 1
                    results.append(ComplianceEvaluationResult(
                        rule_id=rule_id,
                        rule_name=rule_name,
                        status=RuleStatus.COMPLIANT,
                        severity=severity,
                        policy_reference=policy_ref,
                        evidence_found=f"All mandatory documents present: {', '.join(required)}",
                        explanation="All mandatory document categories have been uploaded and ingested.",
                        reviewed=True
                    ))
                else:
                    missing_evidence_count += 1
                    results.append(ComplianceEvaluationResult(
                        rule_id=rule_id,
                        rule_name=rule_name,
                        status=RuleStatus.MISSING_EVIDENCE,
                        severity=severity,
                        policy_reference=policy_ref,
                        evidence_found=f"Missing required documents: {', '.join(missing)}",
                        explanation=f"Application lacks required document type(s): {', '.join(missing)}.",
                        remediation_instructions=r.get("remediation_instructions"),
                        reviewed=False
                    ))

            elif rule_type == "expiry_check":
                target_doc = params.get("target_document_type", "income_certificate")
                if target_doc not in submitted_doc_types:
                    results.append(ComplianceEvaluationResult(
                        rule_id=rule_id,
                        rule_name=rule_name,
                        status=RuleStatus.NOT_APPLICABLE,
                        severity=severity,
                        policy_reference=policy_ref,
                        evidence_found=f"Document '{target_doc}' not submitted for this application.",
                        explanation="Rule not applicable as target document was not uploaded.",
                        reviewed=True
                    ))
                else:
                    # Check extracted expiry / issue date
                    exp_field = all_extracted_fields.get("expiry_date")
                    if exp_field:
                        exp_val = exp_field.get("normalized_value") or exp_field.get("value")
                        # Check if expired
                        try:
                            exp_dt = datetime.strptime(exp_val, "%Y-%m-%d")
                            if exp_dt < datetime.utcnow():
                                non_compliant_count += 1
                                results.append(ComplianceEvaluationResult(
                                    rule_id=rule_id,
                                    rule_name=rule_name,
                                    status=RuleStatus.NON_COMPLIANT,
                                    severity=severity,
                                    policy_reference=policy_ref,
                                    evidence_found=f"Expiry Date: {exp_val} is in the past.",
                                    explanation="Document validity period has expired prior to submission.",
                                    remediation_instructions=r.get("remediation_instructions"),
                                    reviewed=False
                                ))
                            else:
                                compliant_count += 1
                                results.append(ComplianceEvaluationResult(
                                    rule_id=rule_id,
                                    rule_name=rule_name,
                                    status=RuleStatus.COMPLIANT,
                                    severity=severity,
                                    policy_reference=policy_ref,
                                    evidence_found=f"Validity Date {exp_val} is active.",
                                    explanation="Certificate is within active validity window.",
                                    reviewed=True
                                ))
                        except Exception:
                            manual_review_count += 1
                            results.append(ComplianceEvaluationResult(
                                rule_id=rule_id,
                                rule_name=rule_name,
                                status=RuleStatus.REQUIRES_MANUAL_REVIEW,
                                severity=severity,
                                policy_reference=policy_ref,
                                evidence_found=f"Unparsed date string: {exp_val}",
                                explanation="Officer must manually confirm certificate validity text.",
                                remediation_instructions="Inspect certificate date section directly.",
                                reviewed=False
                            ))
                    else:
                        compliant_count += 1
                        results.append(ComplianceEvaluationResult(
                            rule_id=rule_id,
                            rule_name=rule_name,
                            status=RuleStatus.COMPLIANT,
                            severity=severity,
                            policy_reference=policy_ref,
                            evidence_found="Certificate contains no expiration clause.",
                            explanation="Document has permanent or indefinite validity.",
                            reviewed=True
                        ))

            elif rule_type == "threshold_constraint":
                field_key = params.get("field", "annual_income")
                threshold = params.get("threshold_value", 800000)
                operator = params.get("operator", "lte")

                field_obj = all_extracted_fields.get(field_key)
                if not field_obj:
                    results.append(ComplianceEvaluationResult(
                        rule_id=rule_id,
                        rule_name=rule_name,
                        status=RuleStatus.NOT_APPLICABLE,
                        severity=severity,
                        policy_reference=policy_ref,
                        evidence_found=f"Field {field_key} not present in extracted records.",
                        explanation="Threshold evaluation not applicable.",
                        reviewed=True
                    ))
                else:
                    try:
                        raw_num = float(str(field_obj.get("normalized_value", field_obj.get("value"))).replace("₹", "").replace(",", "").strip())
                        is_ok = (raw_num <= threshold) if operator == "lte" else (raw_num >= threshold)
                        if is_ok:
                            compliant_count += 1
                            results.append(ComplianceEvaluationResult(
                                rule_id=rule_id,
                                rule_name=rule_name,
                                status=RuleStatus.COMPLIANT,
                                severity=severity,
                                policy_reference=policy_ref,
                                evidence_found=f"Extracted Value: {raw_num} satisfies condition ({operator} {threshold}).",
                                explanation="Extracted numeric metric satisfies regulatory threshold criteria.",
                                reviewed=True
                            ))
                        else:
                            non_compliant_count += 1
                            results.append(ComplianceEvaluationResult(
                                rule_id=rule_id,
                                rule_name=rule_name,
                                status=RuleStatus.NON_COMPLIANT,
                                severity=severity,
                                policy_reference=policy_ref,
                                evidence_found=f"Extracted Value: {raw_num} breaches ceiling ({threshold}).",
                                explanation="Metric violates the regulatory threshold ceiling.",
                                remediation_instructions=r.get("remediation_instructions"),
                                reviewed=False
                            ))
                    except Exception:
                        manual_review_count += 1
                        results.append(ComplianceEvaluationResult(
                            rule_id=rule_id,
                            rule_name=rule_name,
                            status=RuleStatus.REQUIRES_MANUAL_REVIEW,
                            severity=severity,
                            policy_reference=policy_ref,
                            evidence_found="Unable to parse numeric amount.",
                            explanation="Manual officer review required to verify financial statement.",
                            reviewed=False
                        ))

            elif rule_type == "cross_doc_consistency":
                if cross_doc_summary and hasattr(cross_doc_summary, "contradictions"):
                    if cross_doc_summary.contradictions > 0:
                        non_compliant_count += 1
                        results.append(ComplianceEvaluationResult(
                            rule_id=rule_id,
                            rule_name=rule_name,
                            status=RuleStatus.CONFLICTING_EVIDENCE,
                            severity=severity,
                            policy_reference=policy_ref,
                            evidence_found=f"{cross_doc_summary.contradictions} critical cross-document contradiction(s) detected.",
                            explanation="Extracted applicant credentials diverge across uploaded certificates.",
                            remediation_instructions=r.get("remediation_instructions"),
                            reviewed=False
                        ))
                    elif cross_doc_summary.fuzzy_matches > 0:
                        manual_review_count += 1
                        results.append(ComplianceEvaluationResult(
                            rule_id=rule_id,
                            rule_name=rule_name,
                            status=RuleStatus.REQUIRES_MANUAL_REVIEW,
                            severity=severity,
                            policy_reference=policy_ref,
                            evidence_found="Minor fuzzy name variation detected.",
                            explanation="Spelling or initials variation requires officer verification.",
                            remediation_instructions="Review applicant name aliases.",
                            reviewed=False
                        ))
                    else:
                        compliant_count += 1
                        results.append(ComplianceEvaluationResult(
                            rule_id=rule_id,
                            rule_name=rule_name,
                            status=RuleStatus.COMPLIANT,
                            severity=severity,
                            policy_reference=policy_ref,
                            evidence_found="All cross-document identity fields agree.",
                            explanation="Applicant identity is consistent across all uploaded credentials.",
                            reviewed=True
                        ))
                else:
                    compliant_count += 1
                    results.append(ComplianceEvaluationResult(
                        rule_id=rule_id,
                        rule_name=rule_name,
                        status=RuleStatus.COMPLIANT,
                        severity=severity,
                        policy_reference=policy_ref,
                        evidence_found="Single document or consistent baseline.",
                        explanation="Identity baseline consistent.",
                        reviewed=True
                    ))

        total_rules = len(results)
        compliance_rate = round((compliant_count / max(1, total_rules)) * 100, 1)

        return ComplianceSummary(
            application_id=application_id,
            total_rules=total_rules,
            compliant_count=compliant_count,
            non_compliant_count=non_compliant_count,
            missing_evidence_count=missing_evidence_count,
            manual_review_count=manual_review_count,
            overall_compliance_rate=compliance_rate,
            results=results
        )

compliance_engine = ComplianceEngine()
