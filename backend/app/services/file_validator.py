import io
import os
from typing import Tuple, Optional
from pypdf import PdfReader
from PIL import Image
from backend.app.config import settings

# Magic byte signatures
MAGIC_SIGNATURES = {
    b"%PDF": "application/pdf",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"\xff\xd8\xff": "image/jpeg",
    b"RIFF": "image/webp",  # WebP begins with RIFF....WEBP
}

class ValidationResult:
    def __init__(self, is_valid: bool, mime_type: str, page_count: int, error_message: Optional[str] = None):
        self.is_valid = is_valid
        self.mime_type = mime_type
        self.page_count = page_count
        self.error_message = error_message

def detect_mime_type_by_bytes(content: bytes) -> Optional[str]:
    if len(content) < 12:
        return None
    if content.startswith(b"%PDF"):
        return "application/pdf"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if content.startswith(b"RIFF") and b"WEBP" in content[8:12]:
        return "image/webp"
    return None

def validate_uploaded_file(filename: str, content: bytes) -> ValidationResult:
    # 1. Size check
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) == 0:
        return ValidationResult(False, "unknown", 0, "Uploaded file is empty (0 bytes).")
    if len(content) > max_bytes:
        return ValidationResult(False, "unknown", 0, f"File size exceeds maximum allowed limit of {settings.MAX_FILE_SIZE_MB}MB.")

    # 2. Magic byte inspection
    detected_mime = detect_mime_type_by_bytes(content)
    if not detected_mime:
        return ValidationResult(False, "unknown", 0, "Invalid file signature. File header does not match any accepted format (PDF, PNG, JPEG, WebP).")

    if detected_mime not in settings.ALLOWED_MIME_TYPES:
        return ValidationResult(False, detected_mime, 0, f"File type {detected_mime} is not permitted. Only PDF, PNG, JPEG, and WebP are allowed.")

    # 3. Format integrity & structural parsing
    if detected_mime == "application/pdf":
        try:
            stream = io.BytesIO(content)
            reader = PdfReader(stream)
            if reader.is_encrypted:
                return ValidationResult(False, detected_mime, 0, "Encrypted or password-protected PDFs are not supported. Please upload an unlocked document.")
            
            page_count = len(reader.pages)
            if page_count == 0:
                return ValidationResult(False, detected_mime, 0, "PDF contains no readable pages.")
            if page_count > settings.MAX_PAGE_COUNT:
                return ValidationResult(False, detected_mime, page_count, f"PDF page count ({page_count}) exceeds limit of {settings.MAX_PAGE_COUNT} pages.")
            
            # Verify first page can be read
            _ = reader.pages[0].extract_text()
            return ValidationResult(True, detected_mime, page_count, None)
        except Exception as e:
            return ValidationResult(False, detected_mime, 0, f"Malformed or corrupted PDF structure: {str(e)}")

    else:
        # Image integrity check
        try:
            # Protect against decompression bombs
            Image.MAX_IMAGE_PIXELS = 50_000_000  # 50 MP limit
            stream = io.BytesIO(content)
            with Image.open(stream) as img:
                img.verify()
            
            # Reopen to check dimensions and load
            stream.seek(0)
            with Image.open(stream) as img:
                width, height = img.size
                if width < 50 or height < 50:
                    return ValidationResult(False, detected_mime, 1, "Image dimensions are too small to be a legible document.")
            return ValidationResult(True, detected_mime, 1, None)
        except Exception as e:
            return ValidationResult(False, detected_mime, 0, f"Corrupted or invalid image file: {str(e)}")
