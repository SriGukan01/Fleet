# VERITRUST AI — REST API Technical Reference
## OpenAPI / Swagger Documented Endpoints
### Base URL: `http://127.0.0.1:8000`

---

## Authentication Endpoints (`/api/auth`)

### 1. Register User
- **Method**: `POST /api/auth/register`
- **Request Body**:
  ```json
  {
    "email": "user@example.edu",
    "name": "Full Name",
    "password": "Password123!",
    "role": "applicant",
    "organization": "Institution Name"
  }
  ```
- **Response**: `200 OK` with JWT bearer token and user object.

### 2. Standard Login
- **Method**: `POST /api/auth/login`
- **Request Body**: `{"email": "...", "password": "..."}`
- **Response**: `200 OK` with JWT token.

### 3. Demo 1-Click Role Login
- **Method**: `POST /api/auth/demo-login`
- **Request Body**: `{"role": "applicant" | "officer" | "admin"}`
- **Response**: `200 OK` with authorized demonstration JWT token.

### 4. Current Session Profile
- **Method**: `GET /api/auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Current authenticated user profile.

---

## Applications Endpoints (`/api/applications`)

### 5. Create Application
- **Method**: `POST /api/applications`
- **Request Body**:
  ```json
  {
    "applicant_name": "Aarav Sharma",
    "applicant_email": "aarav.sharma@example.edu",
    "category": "scholarship",
    "organization_or_institution": "Delhi Technological University",
    "declared_details": {
      "applicant_name": "Aarav Sharma",
      "annual_income": "₹3,40,000"
    }
  }
  ```
- **Response**: Created application with unique reference ID (e.g. `APP-2026-SCH-A93F2B`).

### 6. List Applications
- **Method**: `GET /api/applications`
- **Query Params**: `category`, `status`, `priority_level`, `search`
- **Response**: Array of application summaries.

### 7. Get Application Detail
- **Method**: `GET /api/applications/{id}`
- **Response**: Complete application entity with embedded document catalog, cross-document comparison, compliance summary, and review decisions.

---

## Documents & Pipeline (`/api`)

### 8. Upload & Ingest Document
- **Method**: `POST /api/applications/{id}/documents`
- **Content-Type**: `multipart/form-data`
- **Fields**: `file` (binary), `document_type` (string)
- **Response**: Parsed document record with SHA-256 hash, extracted fields, bounding boxes, and forensic findings.

### 9. View Rendered Page Preview
- **Method**: `GET /api/documents/{id}/preview?page=1`
- **Response**: `image/png` high-resolution rendered page.

### 10. Trigger Full Verification Pipeline
- **Method**: `POST /api/applications/{id}/verify`
- **Response**: Verification summary, cross-document matrix, compliance results, and Review Priority Score (0-100).

---

## Review & Reports

### 11. Record Adjudication Decision
- **Method**: `POST /api/applications/{id}/review`
- **Request Body**:
  ```json
  {
    "action": "approved",
    "reason": "All credentials verified against statutory guidelines.",
    "notes": "Verified by officer sign-off"
  }
  ```
- **Response**: Updated application status with immutable audit record.

### 12. Download PDF Verification Report
- **Method**: `GET /api/applications/{id}/reports/pdf`
- **Response**: `application/pdf` binary download with legal disclaimers.

### 13. Download JSON Verification Report
- **Method**: `GET /api/applications/{id}/reports/json`
- **Response**: Machine-readable JSON summary.
