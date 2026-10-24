import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { Application } from '../types';
import { Download, FileText, CheckCircle2, AlertTriangle, ShieldCheck, Printer, ArrowLeft } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [apps, setApps] = useState<Application[]>([]);
  const [selectedAppId, setSelectedAppId] = useState<string>(id || '');
  const [app, setApp] = useState<Application | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadApps() {
      try {
        const data = await apiRequest<Application[]>('/api/applications');
        setApps(data);
        if (!selectedAppId && data.length > 0) {
          setSelectedAppId(data[0].id || data[0]._id || '');
        }
      } catch (err) {
        console.error('Failed to load apps:', err);
      }
    }
    loadApps();
  }, []);

  useEffect(() => {
    async function loadAppDetail() {
      if (!selectedAppId) return;
      setIsLoading(true);
      try {
        const data = await apiRequest<Application>(`/api/applications/${selectedAppId}`);
        setApp(data);
      } catch (err) {
        console.error('Failed to load detail:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadAppDetail();
  }, [selectedAppId]);

  const handleDownloadPDF = () => {
    if (!selectedAppId) return;
    window.open(`/api/applications/${selectedAppId}/reports/pdf`, '_blank');
  };

  const handleDownloadJSON = () => {
    if (!selectedAppId) return;
    window.open(`/api/applications/${selectedAppId}/reports/json`, '_blank');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
            Verification Report Generator & Preview
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Downloadable audit reports with structured evidence and statutory limitations.
          </p>
        </div>

        {/* Application Selector */}
        <div className="flex items-center gap-3">
          <select
            value={selectedAppId}
            onChange={(e) => setSelectedAppId(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-300 bg-white font-medium text-xs text-navy-950 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            {apps.map((a) => (
              <option key={a.id || a._id} value={a.id || a._id}>
                {a.reference_id} — {a.applicant_name}
              </option>
            ))}
          </select>

          <button
            onClick={handleDownloadPDF}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-navy-950 hover:bg-navy-900 text-white shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download PDF</span>
          </button>

          <button
            onClick={handleDownloadJSON}
            className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 flex items-center gap-1.5 transition-all"
          >
            <span>JSON</span>
          </button>
        </div>
      </div>

      {isLoading || !app ? (
        <div className="p-12 text-center">
          <div className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto" />
        </div>
      ) : (
        /* Report Paper Preview */
        <div className="bg-white rounded-2xl border border-slate-200 shadow-lg p-8 sm:p-12 space-y-8 font-sans">
          {/* Report Header */}
          <div className="flex flex-wrap items-start justify-between gap-4 pb-6 border-b-2 border-teal-600">
            <div>
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-6 h-6 text-teal-600" />
                <span className="text-xl font-extrabold text-navy-950 tracking-tight font-['Plus_Jakarta_Sans']">
                  VERITRUST <span className="text-teal-600">AI</span>
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                AICTE Smart Automation • Decision-Support Verification Report
              </p>
            </div>

            <div className="text-right text-xs">
              <p className="font-mono font-bold text-navy-950">REPORT ID: REP-{app.reference_id}</p>
              <p className="text-slate-400 text-[11px] mt-0.5">
                Generated: {new Date().toLocaleDateString()}
              </p>
              <span className="inline-block mt-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-800 border border-slate-200">
                STATUS: {app.status}
              </span>
            </div>
          </div>

          {/* Section 1: Executive Profile */}
          <div className="p-5 bg-slate-50 rounded-xl border border-slate-200 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div>
              <span className="text-slate-400 font-semibold">Applicant Name</span>
              <p className="font-bold text-navy-950 text-sm mt-0.5">{app.applicant_name}</p>
            </div>
            <div>
              <span className="text-slate-400 font-semibold">Category</span>
              <p className="font-bold text-navy-950 text-sm capitalize mt-0.5">
                {app.category.replace('_', ' ')}
              </p>
            </div>
            <div>
              <span className="text-slate-400 font-semibold">Priority Score</span>
              <p className="font-bold font-mono text-sm mt-0.5 text-teal-800">
                {app.review_priority_score}/100
              </p>
            </div>
            <div>
              <span className="text-slate-400 font-semibold">Processed Docs</span>
              <p className="font-bold font-mono text-sm mt-0.5 text-navy-950">
                {app.documents?.length || 0} Files
              </p>
            </div>
          </div>

          {/* Section 2: Processed Documents */}
          <div className="space-y-3">
            <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider">
              1. Ingested Documents & Cryptographic Hashes
            </h2>
            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-[11px] font-bold text-slate-600 border-b border-slate-200">
                  <tr>
                    <th className="p-3">Classification</th>
                    <th className="p-3">Filename</th>
                    <th className="p-3">SHA-256 Digest</th>
                    <th className="p-3">OCR Conf.</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {app.documents?.map((d) => (
                    <tr key={d._id || d.id}>
                      <td className="p-3 font-semibold capitalize">
                        {d.document_type.replace(/_/g, ' ')}
                      </td>
                      <td className="p-3 text-slate-700">{d.metadata.original_filename}</td>
                      <td className="p-3 font-mono text-[10px] text-slate-500">
                        {d.metadata.sha256_hash.slice(0, 16)}...
                      </td>
                      <td className="p-3 font-mono font-semibold text-teal-700">
                        {Math.round(d.ocr_confidence_score * 100)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Section 3: Adjudication */}
          <div className="space-y-3">
            <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider">
              2. Verification Officer Adjudication Record
            </h2>
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-500">Official Determination:</span>
                <span className="font-bold font-mono uppercase text-teal-800">
                  {app.review_decision?.action || 'PENDING OFFICER ADJUDICATION'}
                </span>
              </div>
              <div>
                <span className="text-slate-500">Mandatory Justification Reason:</span>
                <p className="font-medium text-navy-950 mt-1">
                  {app.review_decision?.reason || 'Awaiting formal human review determination.'}
                </p>
              </div>
            </div>
          </div>

          {/* Statutory Disclaimers */}
          <div className="p-4 bg-amber-50/60 rounded-xl border border-amber-200 text-[11px] text-amber-900 space-y-1">
            <p className="font-bold flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
              Statutory Limitations Notice
            </p>
            <p className="leading-relaxed">
              This automated report is generated by VERITRUST AI as an institutional decision-support system.
              Automated OCR confidence scores, tampering heuristics, and compliance checks DO NOT constitute a government-certified
              document or legally conclusive forensic certificate. Final consequential determinations must be authorized by a designated verification officer.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
