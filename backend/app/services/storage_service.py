import os
import hashlib
import uuid
from typing import Tuple
from backend.app.config import settings

class StorageService:
    def __init__(self):
        self.upload_dir = os.path.join(settings.STORAGE_LOCAL_DIR, "uploads")
        self.preview_dir = os.path.join(settings.STORAGE_LOCAL_DIR, "previews")
        self.report_dir = os.path.join(settings.STORAGE_LOCAL_DIR, "reports")
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.preview_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    @staticmethod
    def calculate_sha256(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def save_upload(self, original_filename: str, content: bytes) -> Tuple[str, str, str]:
        """
        Saves uploaded file safely.
        Returns: (stored_filename, absolute_file_path, sha256_hash)
        """
        sha256_hash = self.calculate_sha256(content)
        # Extract extension safely
        _, ext = os.path.splitext(original_filename)
        ext = ext.lower()
        if not ext:
            ext = ".bin"
        
        unique_id = str(uuid.uuid4())
        stored_filename = f"{unique_id}{ext}"
        absolute_path = os.path.join(self.upload_dir, stored_filename)
        
        with open(absolute_path, "wb") as f:
            f.write(content)
            
        return stored_filename, absolute_path, sha256_hash

    def get_file_bytes(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()

    def get_preview_path(self, document_id: str, page_num: int = 1) -> str:
        return os.path.join(self.preview_dir, f"{document_id}_page_{page_num}.png")

    def save_preview(self, document_id: str, image_bytes: bytes, page_num: int = 1) -> str:
        preview_path = self.get_preview_path(document_id, page_num)
        with open(preview_path, "wb") as f:
            f.write(image_bytes)
        return preview_path

    def get_report_path(self, application_id: str, report_type: str = "pdf") -> str:
        return os.path.join(self.report_dir, f"verification_report_{application_id}.{report_type}")

storage_service = StorageService()
