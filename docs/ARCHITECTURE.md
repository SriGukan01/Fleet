# VERITRUST AI — Architectural Technical Specification
## AI-Powered Application Validation, Document Authentication & Regulatory Compliance Verification
### SIH26261 | AICTE | Smart Automation

---

## 1. System Overview

VERITRUST AI is an enterprise-grade scrutiny intelligence platform designed for universities, scholarship administrators, government-facing service providers, and recruitment cells. It solves the critical problem of automated credential ingestion and multi-layer validation without relying on black-box predictions or ungrounded generative hallucinations.

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
|  |  [Stage A] File Validation & Magic Signature Parsing                        |  |
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
|  |  • Resilient In-Memory / JSON Document Store Fallback                       |  |
|  |  • Cryptographic File Storage with SHA-256 Digest Indexing                  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Subsystems

### A. Document Forensics Engine
- **PDF Metadata & Catalog Inspection**: Scans `/Producer`, `/Creator`, `/CreationDate`, and `/ModDate`. Flags usage of graphical editing software (e.g. Photoshop, Canva, GIMP, Sejda) on institutional documents.
- **Error Level Analysis (ELA)**: Resaves image tiles at 90% JPEG quality to determine compression gradient variance. Divergent error rates identify spliced text and inserted marks.
- **Laplacian Edge Sharpness**: Computes edge variance across the grayscale pixel matrix. Scores under 50.0 flag defocus blur or sensor smear.
- **Stamp & Seal Candidate Locator**: Uses adaptive Gaussian thresholding and contour aspect ratio analysis (0.7 - 1.4) to locate institutional rubber stamps.
- **Digital Signature Parsing**: Inspects PDF `/Sig` dictionaries and ByteRanges, verifying cryptographic integrity while explicitly distinguishing local sandbox limitations from Root CA certificate chain validation.

### B. Cross-Document Correlation Matrix
- Computes pairwise similarity between all credentials uploaded under an application.
- Uses normalized Levenshtein ratios for names (e.g., handles initials, prefixes, transliteration).
- Normalizes disparate date formats (`DD/MM/YYYY`, `YYYY-MM-DD`, `DD Mon YYYY`) into ISO standard and identifies conflicting dates of birth across records.

### C. Grounded Compliance Engine
- Contains deterministic rules referencing authoritative sources:
  1. `AICTE-MANDATORY-DOCS`: AICTE Approval Process Handbook Clause 2.4.1.
  2. `INCOME-VALIDITY-PERIOD`: National Scholarship Portal (NSP) Section 4(b).
  3. `INCOME-THRESHOLD-CEILING`: AICTE Pragati/Saksham Scheme Clause 3.1 (₹8,00,000 ceiling).
  4. `NAME-CONSISTENCY-CHECK`: UGC & AICTE Academic Cell Section 5.
  5. `MINIMUM-QUALIFYING-PERCENTAGE`: AICTE Technical Entry Norms Appendix 1.
- Provides direct source URLs, clause citations, and exact policy excerpts with zero legal fabrication.

### D. Human-in-the-Loop Adjudication
- Enforces mandatory justification reasons (minimum 8 characters) for consequential actions (`approve`, `reject`, `request_evidence`, `escalate`).
- Logs every action into an immutable audit event trail with timestamp, officer identity, role, and client IP.
