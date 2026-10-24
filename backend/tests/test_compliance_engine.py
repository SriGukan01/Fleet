import pytest
from backend.app.services.compliance_engine import compliance_engine, DEFAULT_RULES
from backend.app.models.compliance import RuleStatus

def test_mandatory_documents_rule_success():
    declared = {"applicant_name": "Aarav Sharma"}
    docs = [
        {"document_type": "identity_document", "extracted_fields": {}},
        {"document_type": "academic_certificate", "extracted_fields": {}}
    ]
    summary = compliance_engine.evaluate("test_app", "scholarship", declared, docs, None, DEFAULT_RULES)
    rule_res = next((r for r in summary.results if r.rule_id == "AICTE-MANDATORY-DOCS"), None)
    assert rule_res is not None
    assert rule_res.status == RuleStatus.COMPLIANT

def test_mandatory_documents_missing():
    declared = {"applicant_name": "Rohan Deshmukh"}
    # Only identity submitted, academic missing
    docs = [{"document_type": "identity_document", "extracted_fields": {}}]
    summary = compliance_engine.evaluate("test_app", "scholarship", declared, docs, None, DEFAULT_RULES)
    rule_res = next((r for r in summary.results if r.rule_id == "AICTE-MANDATORY-DOCS"), None)
    assert rule_res is not None
    assert rule_res.status == RuleStatus.MISSING_EVIDENCE

def test_income_ceiling_compliance():
    declared = {"applicant_name": "Test"}
    docs = [
        {
            "document_type": "income_certificate",
            "extracted_fields": {
                "annual_income": {"value": "₹3,40,000", "normalized_value": "340000"}
            }
        }
    ]
    summary = compliance_engine.evaluate("test_app", "scholarship", declared, docs, None, DEFAULT_RULES)
    inc_rule = next((r for r in summary.results if r.rule_id == "INCOME-THRESHOLD-CEILING"), None)
    assert inc_rule is not None
    assert inc_rule.status == RuleStatus.COMPLIANT
