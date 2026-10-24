import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { Building2, ShieldCheck, CheckCircle2, AlertTriangle, ExternalLink, RefreshCw, Key } from 'lucide-react';

export const IssuerIntegrationsPage: React.FC = () => {
  const [issuers, setIssuers] = useState<any[]>([]);
  const [testResult, setTestResult] = useState<any>(null);
  const [isTesting, setIsTesting] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadIssuers() {
      try {
        const data = await apiRequest<any[]>('/api/issuers');
        setIssuers(data);
      } catch (err) {
        console.error('Failed to load issuers:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadIssuers();
  }, []);

  const handleTestDigiLocker = async () => {
    setIsTesting(true);
    setTestResult(null);
    try {
      const res = await apiRequest('/api/issuers/verify', {
        method: 'POST',
        body: JSON.stringify({
          application_id: 'test_app',
          document_id: 'test_doc',
          issuer_code: 'UIDAI_DIGILOCKER',
        }),
      });
      setTestResult(res);
    } catch (err: any) {
      setTestResult({ error: err.message });
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
            Trusted Issuer Registries & Gateway Integrations
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Pluggable verification providers: DigiLocker OAuth sandbox, CBSE Academic Registry, State Revenue e-District.
          </p>
        </div>

        <button
          onClick={handleTestDigiLocker}
          disabled={isTesting}
          className="px-4 py-2.5 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-600/20 flex items-center gap-2 transition-all disabled:opacity-50"
        >
          <Key className="w-3.5 h-3.5" />
          <span>{isTesting ? 'Querying Sandbox...' : 'Test DigiLocker Gateway'}</span>
        </button>
      </div>

      {testResult && (
        <div className="p-4 rounded-xl bg-navy-950 text-white border border-teal-500/40 text-xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-bold text-teal-400">Sandbox Verification Query Result</span>
            <span className="font-mono text-[10px] text-slate-400">
              Ref: {testResult.request_reference || 'N/A'}
            </span>
          </div>
          <p className="text-slate-300 font-mono text-[11px]">{testResult.message}</p>
          <div className="p-2.5 bg-navy-900 rounded border border-navy-800 text-[10px] font-mono text-teal-300">
            {JSON.stringify(testResult.evidence_returned || {}, null, 2)}
          </div>
        </div>
      )}

      {/* Registries List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {issuers.map((iss) => (
          <div
            key={iss._id || iss.issuer_code}
            className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 space-y-4"
          >
            <div className="flex items-start justify-between">
              <div className="space-y-1">
                <span className="text-[10px] font-bold text-teal-700 bg-teal-50 px-2.5 py-0.5 rounded border border-teal-200 uppercase tracking-wider">
                  {iss.category}
                </span>
                <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
                  {iss.name}
                </h3>
                <p className="font-mono text-[11px] text-slate-500">{iss.issuer_code}</p>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                  iss.status === 'operational'
                    ? 'bg-emerald-100 text-emerald-800'
                    : 'bg-amber-100 text-amber-800'
                }`}
              >
                {iss.status}
              </span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl text-xs space-y-1">
              <p className="text-slate-500 text-[11px]">Endpoint:</p>
              <p className="font-mono text-xs text-navy-900 truncate">{iss.api_endpoint || 'Local PKI Cache'}</p>
            </div>

            <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-100">
              <span>Environment: <b>{iss.is_sandbox ? 'Sandbox Simulator' : 'Production API'}</b></span>
              <span>Supported: {iss.supported_doc_types?.join(', ') || 'All'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
