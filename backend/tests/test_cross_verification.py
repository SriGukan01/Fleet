import pytest
from backend.app.services.cross_doc_service import cross_document_service, string_similarity
from backend.app.models.cross_verification import MatchStatus

def test_string_similarity():
    assert string_similarity("Aarav Sharma", "Aarav Sharma") == 1.0
    assert string_similarity("Aarav Sharma", "Aarav K Sharma") > 0.8
    assert string_similarity("Aarav Sharma", "Vikramaditya Roy") < 0.4

def test_cross_verification_detection():
    declared = {"applicant_name": "Aarav Sharma"}
    docs = [
        {
            "_id": "doc_1",
            "document_type": "identity_document",
            "metadata": {"original_filename": "aadhaar.pdf"},
            "extracted_fields": {
                "applicant_name": {"value": "Aarav Sharma", "page_number": 1},
                "dob": {"value": "14/08/2003", "normalized_value": "2003-08-14"}
            }
        },
        {
            "_id": "doc_2",
            "document_type": "academic_certificate",
            "metadata": {"original_filename": "degree.pdf"},
            "extracted_fields": {
                "applicant_name": {"value": "Aarav Sharma", "page_number": 1},
                "dob": {"value": "14/08/2003", "normalized_value": "2003-08-14"}
            }
        }
    ]

    summary = cross_document_service.perform_cross_verification("app_test_1", declared, docs)
    assert summary.contradictions == 0
    assert summary.overall_status == "passed"

def test_contradiction_detected():
    declared = {"applicant_name": "Vikramaditya Roy"}
    docs = [
        {
            "_id": "doc_1",
            "document_type": "identity_document",
            "metadata": {"original_filename": "aadhaar.pdf"},
            "extracted_fields": {
                "applicant_name": {"value": "Vikramaditya Roy", "page_number": 1},
                "dob": {"value": "18/05/2002", "normalized_value": "2002-05-18"}
            }
        },
        {
            "_id": "doc_2",
            "document_type": "academic_certificate",
            "metadata": {"original_filename": "degree.pdf"},
            "extracted_fields": {
                "applicant_name": {"value": "Bikram Roy Chowdhury", "page_number": 1},
                "dob": {"value": "12/09/2000", "normalized_value": "2000-09-12"}
            }
        }
    ]

    summary = cross_document_service.perform_cross_verification("app_test_2", declared, docs)
    assert summary.contradictions > 0
    assert summary.overall_status == "severe_mismatch"
