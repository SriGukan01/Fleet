export type UserRole = 'applicant' | 'officer' | 'admin';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  organization?: string;
  is_active: boolean;
  is_demo: boolean;
  created_at: string;
}

export type ApplicationCategory = 'scholarship' | 'admissions' | 'recruitment' | 'regulatory_licensing';
export type ApplicationStatus = 'draft' | 'submitted' | 'processing' | 'under_review' | 'needs_evidence' | 'approved' | 'rejected';
export type ReviewPriorityLevel = 'low_concern' | 'moderate_concern' | 'high_concern' | 'critical_review_required';

export type DocumentType =
  | 'identity_document'
  | 'academic_certificate'
  | 'marksheet_transcript'
  | 'income_certificate'
  | 'address_proof'
  | 'registration_certificate'
  | 'supporting_declaration'
  | 'other';

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface ExtractedField {
  field_key: string;
  display_name: string;
  value: any;
  normalized_value?: string;
  confidence: number;
  page_number: number;
  bounding_box?: BoundingBox;
  extraction_method: string;
  raw_snippet?: string;
  is_verified: boolean;
  validation_status: string;
}

export interface AuthenticityFinding {
  id: string;
  title: string;
  category: string;
  severity: 'info' | 'low' | 'medium' | 'high' | 'critical';
  evidence: string;
  page_number: number;
  region?: BoundingBox;
  detection_method: string;
  confidence_or_metric?: string;
  explanation: string;
  recommended_action: string;
  human_review_required: boolean;
  limitations?: string;
}

export interface DocumentRecord {
  _id: string;
  id?: string;
  application_id: string;
  document_type: DocumentType;
  metadata: {
    original_filename: string;
    stored_filename: string;
    file_path: string;
    preview_path?: string;
    file_size_bytes: number;
    mime_type: string;
    sha256_hash: string;
    page_count: number;
    upload_timestamp: string;
    version: number;
  };
  status: string;
  ocr_confidence_score: number;
  quality_score: number;
  extracted_fields: Record<string, ExtractedField>;
  authenticity_findings: AuthenticityFinding[];
  digital_signature_info?: {
    has_digital_signature: boolean;
    status: string;
    message: string;
    signer_identity?: string;
    byte_range_integrity?: string;
    trust_chain_status?: string;
  };
  created_at: string;
  updated_at: string;
}

export interface CrossDocumentComparison {
  id: string;
  field_key: string;
  display_name: string;
  doc1_id: string;
  doc1_name: string;
  doc1_type: string;
  doc1_value?: string;
  doc2_id: string;
  doc2_name: string;
  doc2_type: string;
  doc2_value?: string;
  match_status: 'exact_match' | 'fuzzy_match' | 'mismatch' | 'missing_in_one' | 'not_applicable';
  similarity_score: number;
  contradiction_flag: boolean;
  evidence_reference: string;
  suggested_resolution: string;
  reviewed: boolean;
}

export interface CrossVerificationSummary {
  application_id: string;
  total_checks: number;
  passed_checks: number;
  fuzzy_matches: number;
  mismatches: number;
  contradictions: number;
  comparisons: CrossDocumentComparison[];
  overall_status: string;
}

export interface RegulatorySource {
  title: string;
  authority: string;
  section_or_clause: string;
  effective_date: string;
  source_url?: string;
  excerpt: string;
}

export interface ComplianceEvaluationResult {
  rule_id: string;
  rule_name: string;
  status: 'compliant' | 'non_compliant' | 'missing_evidence' | 'conflicting_evidence' | 'not_applicable' | 'requires_manual_review';
  severity: 'low' | 'medium' | 'high' | 'critical';
  policy_reference: RegulatorySource;
  evidence_found?: string;
  explanation: string;
  remediation_instructions?: string;
  reviewed: boolean;
}

export interface ComplianceSummary {
  application_id: string;
  total_rules: number;
  compliant_count: number;
  non_compliant_count: number;
  missing_evidence_count: number;
  manual_review_count: number;
  overall_compliance_rate: number;
  results: ComplianceEvaluationResult[];
}

export interface RiskSignal {
  category: string;
  title: string;
  weight: number;
  contribution_points: number;
  evidence: string;
  explanation: string;
}

export interface ReviewPriorityAssessment {
  application_id: string;
  priority_score: number;
  priority_level: ReviewPriorityLevel;
  recommended_queue: string;
  signals: RiskSignal[];
  deterministic_violations_count: number;
  probabilistic_anomalies_count: number;
  model_version: string;
  disclaimer: string;
}

export interface ReviewDecision {
  action: 'approved' | 'rejected' | 'needs_evidence' | 'under_review';
  reason: string;
  notes?: string;
  reviewed_by_name: string;
  reviewed_by_role: string;
  decided_at: string;
}

export interface Application {
  id: string;
  _id?: string;
  reference_id: string;
  applicant_name: string;
  applicant_email: string;
  applicant_phone?: string;
  category: ApplicationCategory;
  organization_or_institution?: string;
  declared_details: Record<string, any>;
  notes?: string;
  status: ApplicationStatus;
  created_by: string;
  document_ids: string[];
  documents?: DocumentRecord[];
  review_priority_score: number;
  review_priority_level: ReviewPriorityLevel;
  verification_summary?: {
    cross_document?: CrossVerificationSummary;
    compliance?: ComplianceSummary;
    risk_assessment?: ReviewPriorityAssessment;
  };
  review_decision?: ReviewDecision;
  created_at: string;
  updated_at: string;
}

export interface DemoScenario {
  id: string;
  title: string;
  reference_id: string;
  applicant: string;
  category: string;
  expected_score: number;
  expected_level: string;
  expected_status: string;
  description: string;
  key_checks: string[];
}
