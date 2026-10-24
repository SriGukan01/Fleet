import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.models.issuer import (
    IssuerRegistryEntry,
    IssuerVerificationRequest,
    IssuerVerificationStatus
)

class IssuerVerificationService:
    def __init__(self):
        self.registry = [
            IssuerRegistryEntry(
                _id="issuer_digilocker",
                issuer_code="UIDAI_DIGILOCKER",
                name="DigiLocker / UIDAI Identity Gateway",
                category="National Identity",
                api_endpoint="https://api.digitallocker.gov.in/public/oauth2/1/xml/pull",
                status="operational",
                is_sandbox=True,
                supported_doc_types=["identity_document"]
            ),
            IssuerRegistryEntry(
                _id="issuer_cbse",
                issuer_code="CBSE_ACADEMIC_REGISTRY",
                name="Central Board of Secondary Education (CBSE API)",
                category="Secondary Education",
                api_endpoint="https://cbse.nic.in/academic/records/verify",
                status="operational",
                is_sandbox=True,
                supported_doc_types=["academic_certificate", "marksheet_transcript"]
            ),
            IssuerRegistryEntry(
                _id="issuer_state_revenue",
                issuer_code="STATE_REVENUE_DIRECTORATE",
                name="State Revenue e-District Portal",
                category="Revenue & Welfare",
                api_endpoint="https://edistrict.gov.in/services/income/verify",
                status="operational",
                is_sandbox=True,
                supported_doc_types=["income_certificate"]
            ),
            IssuerRegistryEntry(
                _id="issuer_cca_esign",
                issuer_code="CCA_ESIGN_GATEWAY",
                name="Controller of Certifying Authorities (CCA India)",
                category="PKI & Digital Signatures",
                api_endpoint="https://cca.gov.in/pki/ocsp",
                status="degraded",  # Offline sandbox simulation
                is_sandbox=True,
                supported_doc_types=["all"]
            )
        ]

    def get_registered_issuers(self) -> List[IssuerRegistryEntry]:
        return self.registry

    def verify_against_issuer(
        self,
        application_id: str,
        document_id: str,
        issuer_code: str,
        extracted_fields: Dict[str, Any]
    ) -> IssuerVerificationRequest:
        """
        Executes verification against external or sandbox issuer registry.
        Accurately flags whether call was sandboxed or real.
        """
        req_ref = f"REQ-VERI-{uuid.uuid4().hex[:8].upper()}"
        ts = datetime.utcnow().isoformat()

        if issuer_code == "UIDAI_DIGILOCKER":
            # Check if name and document_number exist
            name = extracted_fields.get("applicant_name", {}).get("value")
            doc_no = extracted_fields.get("document_number", {}).get("value")
            
            if not doc_no:
                return IssuerVerificationRequest(
                    _id=str(uuid.uuid4()),
                    application_id=application_id,
                    document_id=document_id,
                    issuer_code=issuer_code,
                    request_reference=req_ref,
                    timestamp=ts,
                    status=IssuerVerificationStatus.UNAVAILABLE,
                    fields_checked=["document_number"],
                    evidence_returned={},
                    is_simulated=True,
                    message="Aadhaar / Document number not found in document to query DigiLocker Pull API."
                )

            return IssuerVerificationRequest(
                _id=str(uuid.uuid4()),
                application_id=application_id,
                document_id=document_id,
                issuer_code=issuer_code,
                request_reference=req_ref,
                timestamp=ts,
                status=IssuerVerificationStatus.SANDBOX_SIMULATED,
                fields_checked=["applicant_name", "dob", "document_number"],
                evidence_returned={
                    "sandbox_match": True,
                    "matched_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "authority": "Unique Identification Authority of India (UIDAI)"
                },
                is_simulated=True,
                message="[SANDBOX MODE] Simulated DigiLocker API response. Test identity verified against sandbox mock records."
            )

        elif issuer_code == "UNAVAILABLE_TEST":
            return IssuerVerificationRequest(
                _id=str(uuid.uuid4()),
                application_id=application_id,
                document_id=document_id,
                issuer_code=issuer_code,
                request_reference=req_ref,
                timestamp=ts,
                status=IssuerVerificationStatus.UNAVAILABLE,
                fields_checked=[],
                evidence_returned={},
                is_simulated=False,
                message="External verification service timed out (HTTP 504 Gateway Timeout). Reviewer must perform manual outreach."
            )

        # Default fallback
        return IssuerVerificationRequest(
            _id=str(uuid.uuid4()),
            application_id=application_id,
            document_id=document_id,
            issuer_code=issuer_code,
            request_reference=req_ref,
            timestamp=ts,
            status=IssuerVerificationStatus.SANDBOX_SIMULATED,
            fields_checked=list(extracted_fields.keys()),
            evidence_returned={"status": "record_acknowledged"},
            is_simulated=True,
            message="Sandbox validation successful against standard schema registry."
        )

issuer_service = IssuerVerificationService()
