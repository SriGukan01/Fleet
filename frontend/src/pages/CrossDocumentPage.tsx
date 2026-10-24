import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { Application } from '../types';
import { CrossDocMatrix } from '../components/cross_doc/CrossDocMatrix';
import { GitCompare, Sparkles, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const CrossDocumentPage: React.FC = () => {
  const [apps, setApps] = useState<Application[]>([]);
  const [selectedAppId, setSelectedAppId] = useState<string>('');
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

  const selectedApp = apps.find((a) => (a.id || a._id) === selectedAppId);
  const crossDoc = selectedApp?.verification_summary?.cross_document;

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
            Cross-Document Intelligence Engine
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Detects subtle name transliterations, DOB contradictions, and contradictory credentials across multi-document submissions.
          </p>
        </div>

        {/* Application Selector */}
        <div className="flex items-center gap-2 text-xs">
          <span className="font-semibold text-slate-600">Select Intake:</span>
          <select
            value={selectedAppId}
            onChange={(e) => setSelectedAppId(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-300 bg-white font-medium text-navy-950 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            {apps.map((a) => (
              <option key={a.id || a._id} value={a.id || a._id}>
                {a.reference_id} — {a.applicant_name} ({a.category})
              </option>
            ))}
          </select>
        </div>
      </div>

      {crossDoc ? (
        <CrossDocMatrix summary={crossDoc} />
      ) : (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 text-slate-400 space-y-2">
          <GitCompare className="w-8 h-8 text-slate-300 mx-auto" />
          <p className="text-xs font-semibold text-slate-600">No cross-document checks executed yet for this application.</p>
          <p className="text-[11px]">Run the verification pipeline from the review workbench.</p>
        </div>
      )}
    </div>
  );
};
