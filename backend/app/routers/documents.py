import os
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from backend.app.database import get_db
from backend.app.models.document import DocumentType, DocumentStatus
from backend.app.services.storage_service import storage_service
from backend.app.services.file_validator import validate_uploaded_file
from backend.app.services.ocr_service import ocr_service
from backend.app.services.forensic_service import forensic_service
from backend.app.services.digital_signature import digital_signature_service
from backend.app.services.field_extractor import field_extractor_service
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api", tags=["Documents"])

@router.post("/applications/{id}/documents")
async def upload_document(
    id: str,
    file: UploadFile = File(...),
    document_type: str = Form(DocumentType.IDENTITY_DOCUMENT.value),
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")
    audit_col = db.get_collection("audit_events")

    app = await apps_col.find_one({"_id": id})
    if not app:
        app = await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Target application not found.")

    # Read bytes
    content = await file.read()
    
    # 1. Server-side validation (magic bytes, pdf/image integrity, size)
    val_res = validate_uploaded_file(file.filename, content)
    if not val_res.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File validation rejected: {val_res.error_message}"
        )

    # 2. Check for duplicate SHA-256 hash in system
    sha_hash = storage_service.calculate_sha256(content)
    existing_dup = await docs_col.find_one({"metadata.sha256_hash": sha_hash})
    is_duplicate = existing_dup is not None

    # 3. Save to storage abstraction
    stored_name, file_path, _ = storage_service.save_upload(file.filename, content)
    doc_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    # 4. Run AI Intelligence Pipeline
    # OCR & Layout preview
    ocr_res = ocr_service.process_document(file_path, val_res.mime_type, doc_id)
    
    # Authenticity & Forensics
    auth_rep = forensic_service.run_authenticity_pipeline(file_path, val_res.mime_type, doc_id)
    
    # Digital Signature Check
    dig_sig = digital_signature_service.inspect_digital_signature(file_path, val_res.mime_type)
    
    # Structured Field Extraction
    try:
        d_type_enum = DocumentType(document_type)
    except Exception:
        d_type_enum = DocumentType.OTHER
    extracted_fields = field_extractor_service.extract_fields(ocr_res.full_text, ocr_res.blocks, d_type_enum)

    # If duplicate detected, add an authenticity warning finding
    findings_list = [f.model_dump() for f in auth_rep.findings]
    if is_duplicate:
        findings_list.append({
            "id": f"{doc_id}_dup_hash",
            "title": "Exact SHA-256 Duplicate File Detected",
            "category": "duplicate_submission",
            "severity": "high",
            "evidence": f"File hash '{sha_hash}' matches existing record ID '{existing_dup.get('_id')}'.",
            "page_number": 1,
            "detection_method": "Cryptographic SHA-256 Hash Ingestion Table",
            "confidence_or_metric": "Exact 256-bit hash match",
            "explanation": "This exact file was already uploaded to another application. May indicate duplicate submission or shared documentation.",
            "recommended_action": "Verify if applicant holds multiple accounts or if document was re-used.",
            "human_review_required": True,
            "limitations": "Does not prove fraud if legitimate cross-application submission."
        })

    # 5. Persist Document Record
    doc_record = {
        "_id": doc_id,
        "application_id": app["_id"],
        "document_type": d_type_enum.value,
        "metadata": {
            "original_filename": file.filename,
            "stored_filename": stored_name,
            "file_path": file_path,
            "preview_path": storage_service.get_preview_path(doc_id, 1),
            "file_size_bytes": len(content),
            "mime_type": val_res.mime_type,
            "sha256_hash": sha_hash,
            "page_count": ocr_res.page_count,
            "upload_timestamp": now,
            "version": 1
        },
        "status": DocumentStatus.ANALYZED.value if not is_duplicate else DocumentStatus.FLAGGED.value,
        "ocr_confidence_score": ocr_res.avg_confidence,
        "quality_score": 95.0,
        "extracted_fields": {k: v.model_dump() for k, v in extracted_fields.items()},
        "authenticity_findings": findings_list,
        "digital_signature_info": dig_sig,
        "created_at": now,
        "updated_at": now
    }
    await docs_col.insert_one(doc_record)

    # Update Application doc list
    await apps_col.update_one(
        {"_id": app["_id"]},
        {"$set": {"document_ids": list(set(app.get("document_ids", []) + [doc_id])), "status": "under_review"}}
    )

    # Audit event
    await audit_col.insert_one({
        "_id": str(uuid.uuid4()),
        "timestamp": now,
        "actor_id": current_user.id,
        "actor_name": current_user.name,
        "actor_role": current_user.role.value,
        "action": "DOCUMENT_UPLOADED",
        "entity_type": "document",
        "entity_id": doc_id,
        "details": {"filename": file.filename, "sha256": sha_hash, "type": document_type}
    })

    return doc_record

@router.get("/documents/{id}")
async def get_document(id: str, current_user: UserResponse = Depends(get_current_user)):
    db = get_db()
    docs_col = db.get_collection("documents")
    doc = await docs_col.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return doc

@router.get("/documents/{id}/preview")
async def get_document_preview(id: str, page: int = 1):
    """Serves the rendered PNG preview of the document page for visual inspection."""
    preview_path = storage_service.get_preview_path(id, page)
    if not os.path.exists(preview_path):
        # Check if original file is an image
        db = get_db()
        docs_col = db.get_collection("documents")
        doc = await docs_col.find_one({"_id": id})
        if doc and os.path.exists(doc.get("metadata", {}).get("file_path", "")):
            return FileResponse(doc["metadata"]["file_path"], media_type="image/png")
        raise HTTPException(status_code=404, detail="Preview not available for this document.")
    return FileResponse(preview_path, media_type="image/png")

@router.get("/documents/{id}/file")
async def download_original_file(id: str, current_user: UserResponse = Depends(get_current_user)):
    db = get_db()
    docs_col = db.get_collection("documents")
    doc = await docs_col.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    
    file_path = doc.get("metadata", {}).get("file_path")
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File content unavailable on server.")
    
    filename = doc.get("metadata", {}).get("original_filename", "document.pdf")
    mime = doc.get("metadata", {}).get("mime_type", "application/octet-stream")
    return FileResponse(file_path, media_type=mime, filename=filename)

@router.post("/documents/{id}/analyze")
async def reanalyze_document(id: str, current_user: UserResponse = Depends(get_current_user)):
    db = get_db()
    docs_col = db.get_collection("documents")
    doc = await docs_col.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = doc["metadata"]["file_path"]
    mime = doc["metadata"]["mime_type"]
    d_type_enum = DocumentType(doc.get("document_type", "other"))

    ocr_res = ocr_service.process_document(file_path, mime, id)
    auth_rep = forensic_service.run_authenticity_pipeline(file_path, mime, id)
    dig_sig = digital_signature_service.inspect_digital_signature(file_path, mime)
    extracted = field_extractor_service.extract_fields(ocr_res.full_text, ocr_res.blocks, d_type_enum)

    update = {
        "ocr_confidence_score": ocr_res.avg_confidence,
        "extracted_fields": {k: v.model_dump() for k, v in extracted.items()},
        "authenticity_findings": [f.model_dump() for f in auth_rep.findings],
        "digital_signature_info": dig_sig,
        "status": DocumentStatus.ANALYZED.value,
        "updated_at": datetime.utcnow().isoformat()
    }
    await docs_col.update_one({"_id": id}, {"$set": update})
    doc.update(update)
    return doc
