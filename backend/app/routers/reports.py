import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from backend.app.database import get_db
from backend.app.services.report_service import report_service
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api/applications", tags=["Reports"])

@router.post("/{id}/reports")
async def generate_reports(
    id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    db = get_db()
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")

    app = await apps_col.find_one({"_id": id}) or await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    # Fetch documents
    doc_ids = app.get("document_ids", [])
    documents = []
    for d_id in doc_ids:
        d = await docs_col.find_one({"_id": d_id})
        if d:
            documents.append(d)

    app_data = dict(app)
    app_data["documents"] = documents

    # Generate PDF
    pdf_path = report_service.generate_pdf_report(app_data)
    json_data = report_service.generate_json_report(app_data)

    return {
        "message": "Verification reports generated successfully.",
        "application_reference": app.get("reference_id"),
        "pdf_download_url": f"/api/applications/{app['_id']}/reports/pdf",
        "json_download_url": f"/api/applications/{app['_id']}/reports/json",
        "pdf_path": pdf_path
    }

@router.get("/{id}/reports/pdf")
async def download_pdf_report(id: str):
    db = get_db()
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")

    app = await apps_col.find_one({"_id": id}) or await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    doc_ids = app.get("document_ids", [])
    documents = []
    for d_id in doc_ids:
        d = await docs_col.find_one({"_id": d_id})
        if d:
            documents.append(d)

    app_data = dict(app)
    app_data["documents"] = documents

    # Generate or retrieve PDF
    pdf_path = report_service.generate_pdf_report(app_data)
    filename = f"Verification_Report_{app.get('reference_id', 'APP')}.pdf"
    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)

@router.get("/{id}/reports/json")
async def download_json_report(id: str):
    db = get_db()
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")

    app = await apps_col.find_one({"_id": id}) or await apps_col.find_one({"reference_id": id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    doc_ids = app.get("document_ids", [])
    documents = []
    for d_id in doc_ids:
        d = await docs_col.find_one({"_id": d_id})
        if d:
            documents.append(d)

    app_data = dict(app)
    app_data["documents"] = documents

    json_data = report_service.generate_json_report(app_data)
    return JSONResponse(json_data)
