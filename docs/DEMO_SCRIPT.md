# VERITRUST AI — 5-Minute Hackathon Demonstration Script
## SIH26261 | AICTE | Smart Automation

---

## 1. Introduction (0:00 - 1:00)
- **Presenter**: "Good afternoon, esteemed jury. For Problem Statement SIH26261, we present **VERITRUST AI** — an AI-powered application validation, document authentication, and regulatory compliance verification platform."
- **Key Message**: "Most verification tools either do naive OCR or hallucinate fraud scores with ungrounded AI models. VERITRUST AI solves this with a **three-tier explainable framework**:
  1. Deep document forensics (ELA, metadata inspection, digital signatures).
  2. Multi-document cross-correlation (fuzzy matching and contradiction detection).
  3. Grounded regulatory compliance (rule-based evaluation citing real AICTE clauses)."

---

## 2. Live Platform Tour (1:00 - 2:30)
- Open `http://localhost:5173/` on the projector.
- Show the Landing Page: point out the 3-step workflow and click **"Launch Officer Demo"**.
- On the Dashboard:
  - Highlight the **Live Application Funnel** and **Review Priority Distribution** calculated directly from actual database records.
  - Explain the **Review Priority Score**: "Notice we don't claim '99% fraud certainty'. We provide a calibrated 0-100 review priority score to route high-risk files to senior officers."

---

## 3. The 6 Synthetic Scenarios Walkthrough (2:30 - 4:30)
- Click **"Demo Scenarios"** in the sidebar.
- Showcase the pre-seeded scenarios:
  1. **Scenario 1 (Clean Application)**:
     - Open `APP-2026-CLEAN-01`.
     - Show 100% compliance: Aadhaar, Degree, and Income Certificate all agree. Review priority score is 0. Show the celebratory approval.
  2. **Scenario 3 (Cross-Document Discrepancy)**:
     - Open `APP-2026-MISMATCH-03`.
     - Click **Cross-Document Intelligence** tab: show the contradiction table flagging 'Vikramaditya Roy' on Aadhaar vs 'Bikram Roy Chowdhury' on Degree with conflicting DOB (2002 vs 2000).
  3. **Scenario 5 (Suspicious Document Forensics)**:
     - Open `APP-2026-SUSPICIOUS-05`.
     - Click **Visual Evidence Explorer** tab: show the **Deep Forensics** panel exposing that the PDF Producer metadata contains `Canva Creative Studio Pro` and ELA compression divergence across marks tiles!
  4. **Scenario 6 (Graceful External Timeout)**:
     - Show how when an external registry is unreachable, the system returns **"Verification Unavailable"** instead of falsely penalizing the applicant.

---

## 4. Human-in-the-Loop Adjudication & Reports (4:30 - 5:30)
- Demonstrate the **Adjudicate Decision** dialog:
  - Try submitting without a reason: point out the **mandatory justification enforcement**.
  - Provide a substantive reason and commit approval/rejection.
- Click **"Report"**:
  - Show the downloadable **PDF Verification Report** generated dynamically by the backend, complete with SHA-256 hashes, evidence appendix, and statutory limitations disclaimers.

---

## 5. Conclusion & Q&A (5:30 - 6:00)
- Conclude: "VERITRUST AI is production-ready, modular, respects DPDP privacy norms, and provides transparent, evidence-backed assistance for national institutions."
