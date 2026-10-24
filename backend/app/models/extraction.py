from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class BoundingBox(BaseModel):
    x: float  # percentage or pixels
    y: float
    width: float
    height: float

class ExtractedField(BaseModel):
    field_key: str
    display_name: str
    value: Any
    normalized_value: Optional[str] = None
    confidence: float = 1.0  # 0.0 to 1.0
    page_number: int = 1
    bounding_box: Optional[BoundingBox] = None
    extraction_method: str = "ocr_layout"  # ocr_layout, pdf_metadata, vision_ai, rule_regex
    raw_snippet: Optional[str] = None
    is_verified: bool = False
    validation_status: str = "valid"  # valid, warning, invalid, unverified

class DocumentExtractionResult(BaseModel):
    document_id: str
    fields: Dict[str, ExtractedField] = {}
    ocr_full_text: str = ""
    tables: List[Dict[str, Any]] = []
    average_confidence: float = 0.0
    detected_language: str = "en"
    page_count: int = 1
