# VERITRUST AI
## AI-Powered Application Validation, Document Authentication & Regulatory Compliance Verification
### Smart India Hackathon (SIH26261) | AICTE | Smart Automation

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18_TypeScript-2563EB?logo=react&logoColor=white)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Styling-TailwindCSS_Navy_&_Teal-0D9488?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Pytest](https://img.shields.io/badge/Tests-14_Passed_100%25-16A34A?logo=pytest&logoColor=white)](https://pytest.org)
[![License](https://img.shields.io/badge/Hackathon-SIH26261_Prototype-blueviolet)]()

---

## 1. Executive Summary & Problem Statement

In academic admissions, national scholarships (e.g. AICTE Pragati, Saksham), recruitment, and statutory licensing, organizations process tens of thousands of complex credential submissions. Traditional verification relies either on error-prone manual scrutiny or naive OCR systems that claim authenticity merely because text was extracted.

**VERITRUST AI** is a complete, explainable verification platform that answers five foundational questions:
1. **Is the uploaded document readable and structurally valid?** (Magic signature validation, PDF structure, Laplacian sharpness).
2. **Does the document contain inconsistencies or manipulation indicators?** (Error Level Analysis - ELA, PDF producer metadata scanning, font diversity, stamp candidate locator).
3. **Do extracted details agree across the applicant's credentials?** (Pairwise normalized Levenshtein fuzzy matching and DOB contradiction detection).
4. **Which configured regulatory compliance requirements are satisfied or violated?** (Deterministic rule engine citing actual AICTE Handbook clauses).
5. **What evidence supports each finding, and what should the reviewer do next?** (Evidence references, spatial coordinate box overlays, and mandatory justification enforcement for consequential human decisions).

---

## 2. System Architecture

```
+-----------------------------------------------------------------------------------+
|                                CLIENT FRONTEND                                    |
|   React 18 + TypeScript + Vite + Tailwind CSS (Navy & Teal Design System)         |
|   • Landing Page • Review Workbench • Visual Evidence Explorer • Scenarios Demo   |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST (JWT Bearer)
+------------------------------------------v----------------------------------------+
|                               FASTAPI BACKEND                                     |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Routers: /auth  /applications  /documents  /verification  /compliance  ...   |  |
|  +-----------------------------------------------------------------------------+  |
|                                          |                                        |
|  +---------------------------------------v-------------------------------------+  |
|  |                     DOCUMENT INTELLIGENCE PIPELINE                          |  |
|  |                                                                             |  |
|  |  [Stage A] File Validation & Magic Signature Parsing (PDF, PNG, JPEG, WebP) |  |
|  |  [Stage B] Document Classification (Identity / Degree / Marksheet / Income) |  |
|  |  [Stage C] Image Preprocessing & High-Res Page Rendering (150 DPI)         |  |
|  |  [Stage D] Layout-Aware OCR & Coordinate Box Attribution (PyMuPDF)          |  |
|  |  [Stage E] Structured Field Extraction & ISO Date Normalization            |  |
|  |  [Stage F] Forensic Analysis: ELA, Laplacian Blur, PDF Metadata Producer    |  |
|  |  [Stage G] Digital Signature Inspection (ByteRange Integrity & CA Trust)   |  |
|  |  [Stage H] Cross-Document Pairwise Fuzzy Correlation (Levenshtein)          |  |
|  |  [Stage I] Grounded Regulatory Compliance Engine (AICTE Handbook Norms)     |  |
|  |  [Stage J] Weighted Review Priority Engine (0-100 Score & Routing Queue)    |  |
|  +-----------------------------------------------------------------------------+  |
|                                          |                                        |
|  +---------------------------------------v-------------------------------------+  |
|  |                     DATA PERSISTENCE & STORAGE LAYER                        |  |
|  |  • MongoDB Atlas Async Driver (Motor)                                       |  |
|  |  • Resilient In-Memory / JSON Document Store Fallback (Zero Setup)          |  |
|  |  • Cryptographic File Storage with SHA-256 Digest Indexing                  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 3. The 6 Synthetic Demonstration Scenarios

VERITRUST AI includes **6 pre-seeded synthetic test cases** that can be evaluated with 1-click in the UI at `/scenarios`:

1. **Scenario 1 — Clean Application (`APP-2026-CLEAN-01`)**:
   - Complete valid Aadhaar, Engineering Degree, and Income Certificate.
   - All fields agree 100%, income is within AICTE cap (₹3.4L <= ₹8L).
   - Review Priority Score: `0/100` (Low Concern / Fast-Track Cleared).
2. **Scenario 2 — Missing Mandatory Document (`APP-2026-MISSING-02`)**:
   - Identity record uploaded, but mandatory academic transcript is absent.
   - Fails `AICTE-MANDATORY-DOCS` rule. Status: `needs_evidence`.
3. **Scenario 3 — Cross-Document Mismatch (`APP-2026-MISMATCH-03`)**:
   - Name and Date of Birth conflict between Aadhaar and Degree record (`Vikramaditya Roy` vs `Bikram Roy Chowdhury`, DOB: `18/05/2002` vs `12/09/2000`).
   - Review Priority Score: `65/100` (High Concern).
4. **Scenario 4 — Expired Validity Document (`APP-2026-EXPIRED-04`)**:
   - Income certificate validity expired on `2023-03-31`.
   - Fails `INCOME-VALIDITY-PERIOD` rule. Status: `under_review`.
5. **Scenario 5 — Suspicious Document / Forensics (`APP-2026-SUSPICIOUS-05`)**:
   - Master's transcript modified with `Canva Creative Studio Pro` metadata.
   - High Error Level Analysis (ELA) standard deviation across spliced marks tiles.
   - Review Priority Score: `85/100` (Critical Review Required).
6. **Scenario 6 — External Issuer Unavailable (`APP-2026-UNAVAILABLE-06`)**:
   - External licensing gateway returns timeout (HTTP 504).
   - System gracefully marks check as `Verification Unavailable` without falsely accusing the applicant.

---

## 4. Quickstart Guide (Local Setup)

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Node.js 18+ & npm

### Step 1: Clone & Configure
```bash
git clone <repo-url>
cd SIH
copy .env.example .env
```
*(Note: If you leave `MONGODB_URL=""` in `.env`, the system runs smoothly out of the box using the built-in Local Document Store!)*

### Step 2: Run the Backend
```bash
# Windows
backend\venv\Scripts\python backend\run.py

# Linux / macOS
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
python backend/run.py
```
*Backend starts on `http://127.0.0.1:8000` with Swagger docs at `http://127.0.0.1:8000/docs`.*

### Step 3: Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
*Frontend starts on `http://localhost:5173/`.*

### Step 4: Run Automated Tests
```bash
backend\venv\Scripts\python -m pytest backend/tests -v
```
*Executes all 14 unit and integration test suites.*

---

## 5. Demonstration Accounts

The platform includes a **1-Click Role Switcher** at the top right of the application:

| Role | Demo Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Verification Officer** | `officer@veritrust.ai` | `Demo@123` | Scrutiny workbench, visual evidence viewer, adjudication decisions |
| **Applicant** | `applicant@veritrust.ai` | `Demo@123` | New application intake wizard, drag-and-drop document upload |
| **Administrator** | `admin@veritrust.ai` | `Demo@123` | Compliance rule editor, registry management, full audit trail |

---

## 6. Project Directory Structure

```
d:/Hackathon/SIH/
├── backend/
│   ├── app/
│   │   ├── config.py             # App settings & limits
│   │   ├── database.py           # MongoDB Atlas & Local Store fallback
│   │   ├── main.py               # FastAPI application, CORS, routers
│   │   ├── models/               # Pydantic schemas (User, App, Doc, Compliance, Risk, etc.)
│   │   ├── routers/              # Documented REST API endpoints
│   │   ├── seed/                 # Synthetic generator for 6 evaluation scenarios
│   │   └── services/             # OCR, Forensics (ELA), Cross-doc, Compliance, Reports
│   ├── requirements.txt          # Python dependencies
│   ├── run.py                    # Backend server runner
│   └── tests/                    # Pytest test suite (14 test cases)
├── frontend/
│   ├── src/
│   │   ├── api/client.ts         # Fetch client with JWT handling
│   │   ├── components/           # Visual Evidence Explorer, CrossDocMatrix, DecisionDialog
│   │   ├── context/AuthContext.tsx # Authentication & 1-Click Role Switcher
│   │   ├── pages/                # Landing, Dashboard, Review Workbench, Scenarios, etc.
│   │   └── types/                # TypeScript interface definitions
│   ├── package.json
│   ├── tailwind.config.js        # Navy & Teal color system
│   └── vite.config.ts
├── docs/
│   ├── ARCHITECTURE.md           # Technical deep-dive
│   ├── API_DOCUMENTATION.md      # REST endpoints reference
│   ├── DATABASE_SCHEMA.md        # Data models & collections
│   ├── MODEL_EVALUATION.md       # Precision, recall, and benchmark methodology
│   └── DEMO_SCRIPT.md            # 5-minute judge demonstration script
├── README.md
└── .env.example
```

---

## 7. Known Limitations & Statutory Safeguards

1. **Decision-Support Guarantee**: VERITRUST AI is architected as an institutional decision-support system. It **never makes irreversible autonomous rejections**. Consequential adjudications require affirmative officer sign-off with mandatory recorded justification.
2. **Heuristic Nature of Forensics**: ELA and metadata checks identify digital manipulation indicators in synthetic and electronic PDFs; analog photocopies or re-photographed physical prints require manual institutional verification or authorized DigiLocker Pull API verification.
3. **Statutory Non-Certification**: Verification reports clearly state that they do not constitute a government-certified forensic certificate or legal ruling.
