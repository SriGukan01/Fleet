import pytest
from backend.app.services.file_validator import validate_uploaded_file

def test_empty_file_rejected():
    res = validate_uploaded_file("empty.pdf", b"")
    assert not res.is_valid
    assert "empty" in res.error_message.lower()

def test_invalid_magic_bytes():
    res = validate_uploaded_file("fake.pdf", b"NOT_A_REAL_PDF_HEADER_123456789")
    assert not res.is_valid
    assert "signature" in res.error_message.lower() or "header" in res.error_message.lower()

def test_valid_pdf_structure():
    # Minimal valid PDF header and trailer
    valid_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 12 >>\nstream\nBT /F1 12 Tf ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000216 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n278\n%%EOF"
    res = validate_uploaded_file("test.pdf", valid_pdf_bytes)
    assert res.is_valid
    assert res.mime_type == "application/pdf"
    assert res.page_count == 1
