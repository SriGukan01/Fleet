import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { Application, DocumentRecord } from '../types';
import { VisualEvidenceExplorer } from '../components/document/VisualEvidenceExplorer';
import { FileCheck2, Layers, Cpu, FileSearch } from 'lucide-react';

export const DocumentVerificationPage: React.FC = () => {
  const [apps, setApps] = useState<Application[]>([]);
  const [selectedAppId, setSelectedAppId] = useState<string>('');
  const [appDetail, setAppDetail] = useState<Application | null>(null);
  const [selectedDocId, setSelectedDocId] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadApps() {
      try {
        const data = await apiRequest<Application[]>('/api/applications');
        setApps(data);
        if (data.length > 0) {
          setSelectedAppId(data[0].id || data[0]._id || '');
        }
      } catch (err) {
        console.error('Failed to load apps:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadApps();
  }, []);

  useEffect(() => {
    async function loadDetail() {
      if (!selectedAppId) return;
      try {
        const detail = await apiRequest<Application>(`/api/applications/${selectedAppId}`);
        setAppDetail(detail);
        if (detail.documents && detail.documents.length > 0) {
          setSelectedDocId(detail.documents[0]._id || detail.documents[0].id || '');
        } else {
          setSelectedDocId('');
        }
      } catch (err) {
        console.error('Failed to load detail:', err);
      }
    }
    loadDetail();
  }, [selectedAppId]);

  const docs = appDetail?.documents || [];
  const selectedDoc = docs.find((d) => (d._id || d.id) === selectedDocId) || docs[0];

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
            Document Authenticity & Visual Evidence Explorer
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Pixel-level forensic inspection, OCR bounding box overlay, Error Level Analysis (ELA), and metadata integrity.
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
        </div>
      </div>

      {/* Document Selector Buttons */}
      {docs.length > 0 ? (
        <div className="space-y-4">
          <div className="flex items-center gap-2 overflow-x-auto pb-1">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider shrink-0 pr-2">
              Select Document:
            </span>
            {docs.map((d) => {
              const dId = d._id || d.id;
              const isSelected = dId === selectedDocId;
              return (
                <button
                  key={dId}
                  onClick={() => setSelectedDocId(dId || '')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold shrink-0 border transition-all ${
                    isSelected
                      ? 'border-teal-500 bg-teal-600 text-white shadow-sm'
                      : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
                  }`}
                >
                  {d.metadata?.original_filename || 'document.pdf'}
                </button>
              );
            })}
          </div>

          {selectedDoc && <VisualEvidenceExplorer document={selectedDoc} />}
        </div>
      ) : (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 text-slate-400 space-y-2">
          <FileSearch className="w-8 h-8 text-slate-300 mx-auto" />
          <p className="text-xs font-semibold text-slate-600">No documents found for this application intake.</p>
        </div>
      )}
    </div>
  );
};
