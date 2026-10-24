from fastapi import APIRouter, Depends
from backend.app.database import get_db
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview")
async def get_analytics_overview(current_user: UserResponse = Depends(get_current_user)):
    db = get_db()
    apps_col = db.get_collection("applications")
    docs_col = db.get_collection("documents")

    all_apps = await apps_col.find().to_list(500)
    all_docs = await docs_col.find().to_list(1000)

    total_applications = len(all_apps)
    total_documents = len(all_docs)

    approved_count = sum(1 for a in all_apps if a.get("status") == "approved")
    rejected_count = sum(1 for a in all_apps if a.get("status") == "rejected")
    needs_evidence_count = sum(1 for a in all_apps if a.get("status") == "needs_evidence")
    under_review_count = sum(1 for a in all_apps if a.get("status") in ["under_review", "submitted", "processing"])

    # Review Priority distribution
    priority_dist = {
        "low_concern": sum(1 for a in all_apps if a.get("review_priority_level") == "low_concern"),
        "moderate_concern": sum(1 for a in all_apps if a.get("review_priority_level") == "moderate_concern"),
        "high_concern": sum(1 for a in all_apps if a.get("review_priority_level") == "high_concern"),
        "critical_review_required": sum(1 for a in all_apps if a.get("review_priority_level") == "critical_review_required"),
    }

    # Category breakdown
    category_counts = {}
    for a in all_apps:
        cat = a.get("category", "other")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # Cross-document mismatch count & contradictions across records
    total_contradictions = 0
    total_cross_checks = 0
    rule_failures = {}

    for a in all_apps:
        v_sum = a.get("verification_summary") or {}
        cross = v_sum.get("cross_document") or {}
        total_contradictions += cross.get("contradictions", 0)
        total_cross_checks += cross.get("total_checks", 0)

        comp = v_sum.get("compliance") or {}
        for r in comp.get("results", []):
            if r.get("status") in ["non_compliant", "missing_evidence"]:
                r_name = r.get("rule_name", "Rule")
                rule_failures[r_name] = rule_failures.get(r_name, 0) + 1

    # Digital signature status count
    sig_status_counts = {"has_signature": 0, "no_signature": 0}
    for d in all_docs:
        sig_info = d.get("digital_signature_info") or {}
        if sig_info.get("has_digital_signature"):
            sig_status_counts["has_signature"] += 1
        else:
            sig_status_counts["no_signature"] += 1

    # Average OCR confidence
    ocr_scores = [d.get("ocr_confidence_score", 0.9) for d in all_docs if d.get("ocr_confidence_score")]
    avg_ocr_confidence = round(sum(ocr_scores) / max(1, len(ocr_scores)) * 100, 1)

    # Funnel format for charts
    funnel_data = [
        {"stage": "Intake Submitted", "count": total_applications, "fill": "#0B192C"},
        {"stage": "AI Ingestion & OCR", "count": total_applications, "fill": "#1E3E62"},
        {"stage": "Cross-Verified", "count": sum(1 for a in all_apps if a.get("verification_summary")), "fill": "#0D9488"},
        {"stage": "Officer Adjudicated", "count": approved_count + rejected_count, "fill": "#14B8A6"},
        {"stage": "Cleared & Approved", "count": approved_count, "fill": "#10B981"},
    ]

    # Category distribution for bar/pie charts
    category_chart_data = [
        {"name": k.replace("_", " ").title(), "value": v}
        for k, v in category_counts.items()
    ]

    # Review priority chart data
    priority_chart_data = [
        {"name": "Low Concern (0-24)", "count": priority_dist["low_concern"], "color": "#10B981"},
        {"name": "Moderate (25-49)", "count": priority_dist["moderate_concern"], "color": "#F59E0B"},
        {"name": "High Concern (50-74)", "count": priority_dist["high_concern"], "color": "#F97316"},
        {"name": "Critical (75-100)", "count": priority_dist["critical_review_required"], "color": "#EF4444"},
    ]

    # Rule failure chart data
    rule_failure_chart_data = [
        {"rule": k[:25] + "...", "failures": v}
        for k, v in sorted(rule_failures.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    return {
        "kpis": {
            "total_applications": total_applications,
            "total_documents": total_documents,
            "under_review_count": under_review_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "needs_evidence_count": needs_evidence_count,
            "avg_ocr_confidence": avg_ocr_confidence,
            "total_contradictions_detected": total_contradictions,
            "cross_checks_performed": total_cross_checks,
            "digital_signatures_detected": sig_status_counts["has_signature"]
        },
        "funnel_data": funnel_data,
        "category_data": category_chart_data,
        "priority_data": priority_chart_data,
        "rule_failure_data": rule_failure_chart_data
    }
