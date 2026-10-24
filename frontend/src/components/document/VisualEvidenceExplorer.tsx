import React, { useState } from 'react';
import { DocumentRecord, ExtractedField, AuthenticityFinding } from '../../types';
import {
  ShieldAlert,
  ShieldCheck,
  ZoomIn,
  Eye,
  FileSearch,
  Cpu,
  Layers,
  Award,
  Lock,
  AlertTriangle,
  Info,
} from 'lucide-react';

interface Props {
  document: DocumentRecord;
}

export const VisualEvidenceExplorer: React.FC<Props> = ({ document }) => {
  const [activeFieldKey, setActiveFieldKey] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'fields' | 'forensics' | 'digital_signature'>('fields');
  const [selectedFinding, setSelectedFinding] = useState<AuthenticityFinding | null>(null);

  const fields = Object.values(document.extracted_fields || {});
  const findings = document.authenticity_findings || [];
  const digSig = document.digital_signature_info;

  // Active highlighted box
  const activeField = fields.find((f) => f.field_key === activeFieldKey);
  const activeBox = selectedFinding?.region || activeField?.bounding_box;

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
      {/* Header bar */}
      <div className="px-6 py-4 bg-navy-950 text-white flex flex-wrap items-center justify-between gap-4 border-b border-navy-800">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-base font-bold tracking-tight text-white font-['Plus_Jakarta_Sans']">
              Visual Evidence & Forensic Inspection Explorer
            </h2>
            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-500/20 text-teal-300 border border-teal-500/30">
              {document.document_type.replace(/_/g, ' ').toUpperCase()}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            File: {document.metadata.original_filename} • SHA-256: {document.metadata.sha256_hash.slice(0, 16)}...
          </p>
        </div>

        {/* Tab switcher */}
        <div className="flex items-center bg-navy-900 rounded-lg p-1 border border-navy-800">
          <button
            onClick={() => setActiveTab('fields')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'fields' ? 'bg-teal-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            Extracted Fields ({fields.length})
          </button>
          <button
            onClick={() => setActiveTab('forensics')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'forensics' ? 'bg-teal-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            Deep Forensics ({findings.length})
          </button>
          <button
            onClick={() => setActiveTab('digital_signature')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'digital_signature' ? 'bg-teal-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            <Lock className="w-3.5 h-3.5" />
            Digital Signature
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 min-h-[580px]">
        {/* Left Side: Document Visual Canvas with Coordinate Bounding Boxes */}
        <div className="lg:col-span-7 p-6 bg-slate-900/95 flex flex-col items-center justify-center relative border-r border-slate-200">
          <div className="relative max-w-full max-h-[640px] overflow-hidden rounded-lg shadow-2xl border border-slate-700 bg-white">
            <img
              src={`/api/documents/${document._id || document.id}/preview`}
              alt="Document Scan Preview"
              className="max-h-[580px] w-auto object-contain block select-none"
              onError={(e) => {
                // Fallback placeholder if image preview unavailable
                (e.target as HTMLElement).style.display = 'none';
              }}
            />

            {/* Bounding box highlight overlay */}
            {activeBox && (
              <div
                style={{
                  position: 'absolute',
                  left: `${activeBox.x}%`,
                  top: `${activeBox.y}%`,
                  width: `${activeBox.width}%`,
                  height: `${activeBox.height}%`,
                }}
                className="bounding-box-active border-2 border-teal-500 bg-teal-400/20 rounded pointer-events-none transition-all duration-300 z-20 flex items-start justify-end p-0.5"
              >
                <span className="bg-teal-700 text-white text-[9px] font-mono px-1 py-0.2 rounded shadow">
                  Page {selectedFinding?.page_number || activeField?.page_number || 1}
                </span>
              </div>
            )}
          </div>

          <p className="text-slate-400 text-[11px] mt-3 flex items-center gap-1.5">
            <Eye className="w-3.5 h-3.5 text-teal-400" />
            Click any field or forensic finding on the right to project its spatial location.
          </p>
        </div>

        {/* Right Side: Information Panels */}
        <div className="lg:col-span-5 p-6 overflow-y-auto max-h-[680px] space-y-4 bg-slate-50">
          {/* TAB 1: Extracted Fields */}
          {activeTab === 'fields' && (
            <div className="space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                <span className="text-xs font-bold text-slate-700 uppercase tracking-wide">
                  Layout Text Entities ({fields.length})
                </span>
                <span className="text-[11px] text-teal-700 font-medium">
                  Avg OCR Confidence: {Math.round(document.ocr_confidence_score * 100)}%
                </span>
              </div>

              {fields.map((field) => (
                <div
                  key={field.field_key}
                  onClick={() => {
                    setActiveFieldKey(field.field_key);
                    setSelectedFinding(null);
                  }}
                  className={`p-3.5 rounded-xl border text-xs cursor-pointer transition-all ${
                    activeFieldKey === field.field_key
                      ? 'border-teal-500 bg-teal-50/70 shadow-sm ring-1 ring-teal-500'
                      : 'border-slate-200 bg-white hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-slate-600">{field.display_name}</span>
                    <span className="font-mono text-[10px] text-teal-700 bg-teal-100/70 px-1.5 py-0.5 rounded">
                      {Math.round(field.confidence * 100)}% conf
                    </span>
                  </div>
                  <p className="text-sm font-bold text-navy-950 font-mono break-all">{String(field.value)}</p>
                  {field.normalized_value && field.normalized_value !== field.value && (
                    <p className="text-[11px] text-slate-500 mt-1">
                      Normalized: <span className="font-mono text-slate-700">{field.normalized_value}</span>
                    </p>
                  )}
                  <div className="mt-2 flex items-center gap-2 text-[10px] text-slate-400">
                    <span>Method: {field.extraction_method}</span>
                    <span>•</span>
                    <span>Page {field.page_number}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* TAB 2: Deep Forensics & Tampering Analysis */}
          {activeTab === 'forensics' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                <span className="text-xs font-bold text-slate-700 uppercase tracking-wide">
                  Tampering Indicators & Visual Metrics
                </span>
                <span className="text-[11px] font-semibold text-navy-800">
                  {findings.length} findings
                </span>
              </div>

              {findings.length === 0 ? (
                <div className="p-6 text-center bg-white rounded-xl border border-slate-200 text-slate-500 space-y-2">
                  <ShieldCheck className="w-8 h-8 text-emerald-500 mx-auto" />
                  <p className="text-xs font-semibold text-slate-700">No suspicious tampering indicators detected</p>
                  <p className="text-[11px]">Metadata timestamps, fonts, and ELA compression variance fall within normal limits.</p>
                </div>
              ) : (
                findings.map((f) => (
                  <div
                    key={f.id}
                    onClick={() => {
                      setSelectedFinding(f);
                      setActiveFieldKey(null);
                    }}
                    className={`p-4 rounded-xl border text-xs cursor-pointer transition-all ${
                      selectedFinding?.id === f.id
                        ? 'border-navy-800 ring-2 ring-navy-800 shadow-md bg-white'
                        : f.severity === 'critical' || f.severity === 'high'
                        ? 'border-red-200 bg-red-50/50 hover:border-red-300'
                        : 'border-slate-200 bg-white hover:border-slate-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="font-bold text-navy-900 text-xs flex items-center gap-1.5">
                        {f.severity === 'critical' || f.severity === 'high' ? (
                          <AlertTriangle className="w-3.5 h-3.5 text-red-600" />
                        ) : (
                          <Info className="w-3.5 h-3.5 text-amber-600" />
                        )}
                        {f.title}
                      </span>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                          f.severity === 'critical' || f.severity === 'high'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}
                      >
                        {f.severity}
                      </span>
                    </div>

                    <p className="text-slate-700 leading-relaxed text-xs">{f.evidence}</p>

                    <div className="mt-2.5 p-2.5 bg-slate-100/80 rounded-lg text-[11px] text-slate-600 space-y-1">
                      <p>
                        <b>Explanation:</b> {f.explanation}
                      </p>
                      <p className="text-navy-800 font-semibold">
                        <b>Recommended Action:</b> {f.recommended_action}
                      </p>
                    </div>

                    {f.limitations && (
                      <p className="text-[10px] text-slate-400 italic mt-2">
                        Notice: {f.limitations}
                      </p>
                    )}
                  </div>
                ))
              )}
            </div>
          )}

          {/* TAB 3: Digital Signature */}
          {activeTab === 'digital_signature' && (
            <div className="space-y-4">
              <div className="p-4 bg-white rounded-xl border border-slate-200 space-y-3">
                <div className="flex items-center gap-2 text-navy-900 font-bold text-sm">
                  <Lock className="w-4 h-4 text-teal-600" />
                  PDF Cryptographic Digital Signature
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {digSig?.message || 'No digital signature information recorded.'}
                </p>

                {digSig?.has_digital_signature && (
                  <div className="mt-3 p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs space-y-2">
                    <div>
                      <span className="text-slate-500">Signer Identity:</span>
                      <p className="font-semibold text-navy-900 font-mono">{digSig.signer_identity}</p>
                    </div>
                    <div>
                      <span className="text-slate-500">ByteRange Integrity:</span>
                      <p className="font-semibold text-emerald-700">{digSig.byte_range_integrity}</p>
                    </div>
                    <div>
                      <span className="text-slate-500">Trust Chain Status:</span>
                      <p className="font-semibold text-amber-700">{digSig.trust_chain_status}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
