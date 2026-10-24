import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, NavLink } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { Application, DocumentRecord } from '../types';
import { VisualEvidenceExplorer } from '../components/document/VisualEvidenceExplorer';
import { CrossDocMatrix } from '../components/cross_doc/CrossDocMatrix';
import { DecisionDialog } from '../components/review/DecisionDialog';
import { PriorityBadge } from '../components/common/PriorityBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import {
  ShieldCheck,
  Cpu,
  Layers,
  Scale,
  GitCompare,
  Download,
  AlertTriangle,
  CheckCircle2,
  FileText,
  UserCheck2,
  Sparkles,
  ArrowRight,
  ExternalLink,
} from 'lucide-react';

export const HumanReviewPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [app, setApp] = useState<Application | null>(null);
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'evidence' | 'cross_doc' | 'compliance' | 'risk'>('evidence');
  const [isDecisionOpen, setIsDecisionOpen] = useState<boolean>(false);
  const [isVerifying, setIsVerifying] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const loadApplication = async () => {
    if (!id) return;
    setIsLoading(true);
    try {
      const data = await apiRequest<Application>(`/api/applications/${id}`);
      setApp(data);
      if (data.documents && data.documents.length > 0 && !selectedDocId) {
        setSelectedDocId(data.documents[0]._id || data.documents[0].id || null);
      }
    } catch (err) {
      console.error('Failed to load application:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadApplication();
  }, [id]);

  const handleRunVerify = async () => {
    if (!id) return;
    setIsVerifying(true);
    try {
      await apiRequest(`/api/applications/${id}/verify`, { method: 'POST' });
      await loadApplication();
    } catch (err) {
      console.error('Verification failed:', err);
    } finally {
      setIsVerifying(false);
    }
  };

  const handleCommitDecision = async (action: string, reason: string, notes?: string) => {
    if (!id) return;
    await apiRequest(`/api/applications/${id}/review`, {
      method: 'POST',
      body: JSON.stringify({ action, reason, notes }),
    });
    await loadApplication();
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-teal-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!app) {
    return (
      <div className="p-8 text-center space-y-3">
        <p className="text-sm font-semibold text-slate-700">Application not found.</p>
        <button
          onClick={() => navigate('/applications')}
          className="text-xs text-teal-600 font-bold hover:underline"
        >
          &larr; Return to Applications Registry
        </button>
      </div>
    );
  }

  const documents = app.documents || [];
  const selectedDoc = documents.find((d) => (d._id || d.id) === selectedDocId) || documents[0];
  const vSum = app.verification_summary;
  const crossDoc = vSum?.cross_document;
  const compliance = vSum?.compliance;
  const risk = vSum?.risk_assessment;

  return (
    <div className="space-y-6 font-sans">
      {/* Top Header Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              <span className="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                {app.reference_id}
              </span>
              <PriorityBadge score={app.review_priority_score} level={app.review_priority_level} />
              <StatusBadge status={app.status} />
            </div>
            <h1 className="text-xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
              {app.applicant_name}{' '}
              <span className="text-xs font-medium text-slate-400">({app.applicant_email})</span>
            </h1>
            <p className="text-xs text-slate-500">
              Category: <b className="capitalize text-slate-700">{app.category.replace('_', ' ')}</b> • Organization:{' '}
              <b>{app.organization_or_institution || 'N/A'}</b>
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={handleRunVerify}
              disabled={isVerifying}
              className="px-4 py-2.5 rounded-xl text-xs font-bold bg-navy-900 hover:bg-navy-800 text-teal-300 border border-teal-800/60 shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-50"
            >
              <Cpu className="w-4 h-4 text-teal-400" />
              <span>{isVerifying ? 'Verifying Pipeline...' : 'Re-run Scrutiny Engine'}</span>
            </button>

            <button
              onClick={() => navigate(`/applications/${app.id || app._id}/report`)}
              className="px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 flex items-center gap-1.5 transition-all"
            >
              <Download className="w-4 h-4" />
              <span>Report</span>
            </button>

            <button
              onClick={() => setIsDecisionOpen(true)}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-600/25 flex items-center gap-1.5 transition-all hover:scale-[1.02]"
            >
              <UserCheck2 className="w-4 h-4" />
              <span>Adjudicate Decision</span>
            </button>
          </div>
        </div>

        {/* Existing Decision Alert if already decided */}
        {app.review_decision && (
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs flex items-start gap-2.5">
            <CheckCircle2 className="w-4 h-4 text-teal-600 mt-0.5 shrink-0" />
            <div>
              <p className="font-bold text-navy-950">
                Official Determination Recorded: <span className="uppercase text-teal-700">{app.review_decision.action}</span>
              </p>
              <p className="text-slate-600 mt-0.5">
                <b>Mandatory Reason:</b> {app.review_decision.reason}
              </p>
              <p className="text-[10px] text-slate-400 mt-1">
                Decided by {app.review_decision.reviewed_by_name} ({app.review_decision.reviewed_by_role}) at{' '}
                {new Date(app.review_decision.decided_at).toLocaleString()}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Document Selector Badges */}
      {documents.length > 0 && (
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider shrink-0 pr-2">
            Uploaded Credentials:
          </span>
          {documents.map((doc) => {
            const docId = doc._id || doc.id;
            const isSelected = docId === selectedDocId;
            return (
              <button
                key={docId}
                onClick={() => {
                  setSelectedDocId(docId || null);
                  setActiveTab('evidence');
                }}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold shrink-0 border transition-all ${
                  isSelected
                    ? 'border-teal-500 bg-teal-600 text-white shadow-sm'
                    : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                }`}
              >
                {doc.metadata?.original_filename || 'document.pdf'}
              </button>
            );
          })}
        </div>
      )}

      {/* Main Workbench Tabs */}
      <div className="flex items-center gap-1 border-b border-slate-200 pb-2 text-xs font-semibold">
        <button
          onClick={() => setActiveTab('evidence')}
          className={`px-4 py-2 rounded-xl transition-all flex items-center gap-2 ${
            activeTab === 'evidence'
              ? 'bg-navy-950 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <FileText className="w-4 h-4" />
          Visual Evidence Explorer
        </button>

        <button
          onClick={() => setActiveTab('cross_doc')}
          className={`px-4 py-2 rounded-xl transition-all flex items-center gap-2 ${
            activeTab === 'cross_doc'
              ? 'bg-navy-950 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <GitCompare className="w-4 h-4" />
          Cross-Document Intelligence ({crossDoc?.total_checks || 0})
        </button>

        <button
          onClick={() => setActiveTab('compliance')}
          className={`px-4 py-2 rounded-xl transition-all flex items-center gap-2 ${
            activeTab === 'compliance'
              ? 'bg-navy-950 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Scale className="w-4 h-4" />
          Regulatory Rules ({compliance?.total_rules || 0})
        </button>

        <button
          onClick={() => setActiveTab('risk')}
          className={`px-4 py-2 rounded-xl transition-all flex items-center gap-2 ${
            activeTab === 'risk'
              ? 'bg-navy-950 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Sparkles className="w-4 h-4 text-teal-400" />
          Review Priority Signals ({risk?.signals?.length || 0})
        </button>
      </div>

      {/* Content for Active Tab */}
      {activeTab === 'evidence' && selectedDoc && (
        <VisualEvidenceExplorer document={selectedDoc} />
      )}

      {activeTab === 'cross_doc' && crossDoc && (
        <CrossDocMatrix summary={crossDoc} />
      )}

      {activeTab === 'compliance' && compliance && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
                Regulatory Policy Compliance Evaluation
              </h3>
              <p className="text-xs text-slate-500">
                AICTE Approval Process Norms & Ministry of Education Guidelines.
              </p>
            </div>
            <span className="text-xs font-bold text-teal-800 bg-teal-50 border border-teal-200 px-3 py-1 rounded-full">
              Compliance Rate: {compliance.overall_compliance_rate}%
            </span>
          </div>

          <div className="space-y-3">
            {compliance.results.map((r) => (
              <div
                key={r.rule_id}
                className={`p-4 rounded-xl border text-xs space-y-2 ${
                  r.status === 'compliant'
                    ? 'border-emerald-200 bg-emerald-50/40'
                    : r.status === 'missing_evidence'
                    ? 'border-purple-200 bg-purple-50/40'
                    : 'border-rose-200 bg-rose-50/40'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-navy-950 text-sm">
                    {r.rule_id}: {r.rule_name}
                  </span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      r.status === 'compliant'
                        ? 'bg-emerald-100 text-emerald-800'
                        : r.status === 'missing_evidence'
                        ? 'bg-purple-100 text-purple-800'
                        : 'bg-rose-100 text-rose-800'
                    }`}
                  >
                    {r.status.replace(/_/g, ' ')}
                  </span>
                </div>

                <p className="text-slate-700 font-medium">{r.evidence_found || r.explanation}</p>

                <div className="p-3 bg-white/80 rounded-lg border border-slate-200/80 text-[11px] text-slate-600 space-y-1">
                  <p className="font-semibold text-navy-900">
                    Statutory Source: {r.policy_reference.title} ({r.policy_reference.authority})
                  </p>
                  <p className="italic text-slate-500">"{r.policy_reference.excerpt}"</p>
                  {r.policy_reference.source_url && (
                    <a
                      href={r.policy_reference.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-teal-600 hover:underline flex items-center gap-1 font-semibold text-[10px] pt-1"
                    >
                      <span>View Policy Reference</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>

                {r.remediation_instructions && (
                  <p className="text-[11px] text-navy-800 font-semibold">
                    Remediation: {r.remediation_instructions}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'risk' && risk && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
                Explainable Review Priority Breakdown
              </h3>
              <p className="text-xs text-slate-500">
                Recommended routing queue: <b>{risk.recommended_queue}</b>
              </p>
            </div>
            <PriorityBadge score={risk.priority_score} level={risk.priority_level} />
          </div>

          <div className="space-y-3">
            {risk.signals.map((sig, i) => (
              <div key={i} className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-navy-950">{sig.title}</span>
                  <span className="font-mono text-teal-700 font-bold">
                    +{sig.contribution_points} pts
                  </span>
                </div>
                <p className="text-slate-600">{sig.evidence}</p>
                <p className="text-[11px] text-slate-500">{sig.explanation}</p>
              </div>
            ))}
          </div>

          <div className="p-3 rounded-lg bg-slate-100 text-[10px] text-slate-500 italic">
            Notice: {risk.disclaimer}
          </div>
        </div>
      )}

      {/* Decision Dialog Modal */}
      <DecisionDialog
        isOpen={isDecisionOpen}
        onClose={() => setIsDecisionOpen(false)}
        onSubmit={handleCommitDecision}
        applicationRef={app.reference_id}
      />
    </div>
  );
};
