import os
import json
from datetime import datetime
from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.app.services.storage_service import storage_service

class ReportService:
    def __init__(self):
        pass

    def generate_json_report(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates full machine-readable JSON verification report.
        """
        return {
            "meta": {
                "report_id": f"REP-{application_data.get('reference_id', 'VERI')}",
                "generated_at": datetime.utcnow().isoformat(),
                "platform": "VERITRUST AI (SIH26261)",
                "schema_version": "1.0",
                "disclaimer": "This report is an automated AI-assisted scrutiny summary and does not constitute a government-certified document or legally conclusive forensic certificate."
            },
            "application": {
                "reference_id": application_data.get("reference_id"),
                "applicant_name": application_data.get("applicant_name"),
                "category": application_data.get("category"),
                "status": application_data.get("status"),
                "declared_details": application_data.get("declared_details", {})
            },
            "review_priority": {
                "score": application_data.get("review_priority_score", 0),
                "level": application_data.get("review_priority_level", "low_concern"),
                "assessment": application_data.get("verification_summary", {}).get("risk_assessment", {})
            },
            "documents": application_data.get("documents", []),
            "cross_document_verification": application_data.get("verification_summary", {}).get("cross_document", {}),
            "compliance_evaluation": application_data.get("verification_summary", {}).get("compliance", {}),
            "reviewer_decision": application_data.get("review_decision")
        }

    def generate_pdf_report(self, application_data: Dict[str, Any]) -> str:
        """
        Generates enterprise-grade PDF verification report and writes to storage.
        Returns the absolute file path of the generated PDF.
        """
        app_id = application_data.get("reference_id", "DOC")
        output_path = storage_service.get_report_path(app_id, "pdf")
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        
        # Custom palette
        c_navy = colors.HexColor("#0B192C")
        c_teal = colors.HexColor("#0D9488")
        c_dark = colors.HexColor("#1E293B")
        c_light = colors.HexColor("#F8FAFC")
        c_gray = colors.HexColor("#64748B")
        c_red = colors.HexColor("#DC2626")
        c_green = colors.HexColor("#16A34A")

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=c_navy
        )
        sub_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=c_teal
        )
        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=c_navy,
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'DocBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=c_dark
        )
        alert_style = ParagraphStyle(
            'AlertText',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#991B1B")
        )

        elements = []

        # Header Banner
        header_data = [
            [Paragraph("<b>VERITRUST AI</b>", title_style), 
             Paragraph(f"<b>REPORT ID:</b> REP-{app_id}<br/><b>DATE:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", body_style)],
            [Paragraph("AI-Powered Application Validation & Compliance Verification Platform", sub_style),
             Paragraph("<b>STATUS:</b> " + application_data.get("status", "SUBMITTED").upper(), body_style)]
        ]
        header_table = Table(header_data, colWidths=[350, 180])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(header_table)
        elements.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=15, spaceBefore=8))

        # Executive Summary Box
        score = application_data.get("review_priority_score", 0)
        level = application_data.get("review_priority_level", "low_concern").replace("_", " ").title()
        
        score_color = c_green if score < 30 else (colors.HexColor("#D97706") if score < 60 else c_red)
        
        summary_data = [
            [Paragraph("<b>Applicant Name</b>", body_style), Paragraph(str(application_data.get("applicant_name", "N/A")), body_style),
             Paragraph("<b>Application Category</b>", body_style), Paragraph(str(application_data.get("category", "N/A")).title(), body_style)],
            [Paragraph("<b>Reference ID</b>", body_style), Paragraph(str(application_data.get("reference_id", "N/A")), body_style),
             Paragraph("<b>Review Priority Score</b>", body_style), Paragraph(f"<b><font color='{score_color}'>{score}/100 ({level})</font></b>", body_style)],
        ]
        sum_table = Table(summary_data, colWidths=[130, 135, 130, 135])
        sum_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(sum_table)
        elements.append(Spacer(1, 12))

        # Processed Documents Table
        elements.append(Paragraph("1. Processed Document Catalog & Integrity Hashes", h2_style))
        docs = application_data.get("documents", [])
        doc_rows = [["Document Type", "File Name", "Pages", "SHA-256 Digest", "OCR Conf."]]
        
        for d in docs:
            m = d.get("metadata", {})
            sha = m.get("sha256_hash", "")[:12] + "..."
            doc_rows.append([
                d.get("document_type", "").replace("_", " ").title(),
                m.get("original_filename", "N/A"),
                str(m.get("page_count", 1)),
                sha,
                f"{int(d.get('ocr_confidence_score', 0.9) * 100)}%"
            ])
            
        if len(doc_rows) == 1:
            doc_rows.append(["No documents uploaded", "-", "-", "-", "-"])

        doc_table = Table(doc_rows, colWidths=[120, 150, 40, 140, 80])
        doc_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), c_navy),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(doc_table)
        elements.append(Spacer(1, 12))

        # Cross Document Verification Section
        elements.append(Paragraph("2. Cross-Document Intelligence & Consistency Checks", h2_style))
        cross_doc = application_data.get("verification_summary", {}).get("cross_document", {})
        comparisons = cross_doc.get("comparisons", [])
        
        cross_rows = [["Field", "Source 1", "Source 2", "Status", "Resolution Suggestion"]]
        for c in comparisons[:6]:
            cross_rows.append([
                c.get("display_name", "")[:20],
                f"{c.get('doc1_value', '')[:16]} ({c.get('doc1_name', '')[:10]})",
                f"{c.get('doc2_value', '')[:16]} ({c.get('doc2_name', '')[:10]})",
                c.get("match_status", "").upper(),
                Paragraph(c.get("suggested_resolution", "")[:80], body_style)
            ])
        if len(cross_rows) == 1:
            cross_rows.append(["Single document submitted", "-", "-", "BASELINE", "Pairwise cross-check skipped."])

        cross_table = Table(cross_rows, colWidths=[90, 110, 110, 70, 150])
        cross_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), c_teal),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7.5),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(cross_table)
        elements.append(Spacer(1, 12))

        # Compliance Findings
        elements.append(Paragraph("3. Regulatory Compliance Rule Evaluation", h2_style))
        compliance = application_data.get("verification_summary", {}).get("compliance", {})
        c_results = compliance.get("results", [])
        comp_rows = [["Rule ID", "Rule Name", "Status", "Evidence / Findings"]]
        
        for r in c_results:
            st = r.get("status", "").upper()
            comp_rows.append([
                r.get("rule_id", ""),
                r.get("rule_name", "")[:30],
                st,
                Paragraph(r.get("evidence_found", "No breach")[:100], body_style)
            ])
            
        if len(comp_rows) == 1:
            comp_rows.append(["-", "No compliance rules evaluated", "-", "-"])

        comp_table = Table(comp_rows, colWidths=[90, 150, 90, 200])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334E68")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(comp_table)
        elements.append(Spacer(1, 12))

        # Reviewer Decision & Notes
        decision = application_data.get("review_decision") or {}
        elements.append(Paragraph("4. Verification Officer Adjudication", h2_style))
        dec_status = decision.get("action", "PENDING_REVIEW").upper()
        dec_reason = decision.get("reason", "Awaiting human verification officer determination.")
        
        dec_data = [
            [Paragraph("<b>Adjudication Action</b>", body_style), Paragraph(f"<b>{dec_status}</b>", body_style)],
            [Paragraph("<b>Justification / Mandatory Reason</b>", body_style), Paragraph(dec_reason, body_style)],
            [Paragraph("<b>Reviewer Notes</b>", body_style), Paragraph(decision.get("notes", "None recorded."), body_style)],
            [Paragraph("<b>Decided At</b>", body_style), Paragraph(decision.get("decided_at", "N/A"), body_style)]
        ]
        dec_table = Table(dec_data, colWidths=[150, 380])
        dec_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(dec_table)
        elements.append(Spacer(1, 14))

        # Mandatory Disclaimers
        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94A3B8"), spaceAfter=8, spaceBefore=4))
        disclaimer_text = (
            "<b>STATUTORY NOTICE & LIMITATIONS:</b> This automated verification report was compiled by VERITRUST AI "
            "as an institutional decision-support system. Automated authenticity scores, ELA checks, and OCR match rates "
            "are heuristic indicators and DO NOT constitute a government-certified forensic certificate or legal determination of fraud. "
            "All consequential determinations must be executed by an authorized institutional verification officer."
        )
        elements.append(Paragraph(disclaimer_text, alert_style))

        doc.build(elements)
        return output_path

report_service = ReportService()
