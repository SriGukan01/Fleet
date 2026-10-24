import React, { useState } from 'react';
import { Settings, ShieldCheck, Lock, Sliders, Database, Eye, Save } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [weights, setWeights] = useState({
    crossDocContradiction: 35,
    tamperingEla: 30,
    expiredDoc: 25,
    missingMandatory: 20,
    lowOcrBlur: 15,
  });
  const [saved, setSaved] = useState<boolean>(false);

  const handleSaveWeights = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
          System Configuration & Privacy Governance
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Adjust risk engine weights, document retention parameters, and review statutory compliance notices.
        </p>
      </div>

      {/* Configurable Risk Weights */}
      <form onSubmit={handleSaveWeights} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-teal-600" />
            <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider">
              Review Priority Weighted Scoring Engine
            </h2>
          </div>
          {saved && (
            <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
              ✓ Calibration Saved
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Cross-Document Contradiction Weight (pts)
            </label>
            <input
              type="number"
              value={weights.crossDocContradiction}
              onChange={(e) => setWeights({ ...weights, crossDocContradiction: Number(e.target.value) })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 font-mono text-navy-950"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              ELA & Graphic Editor Tampering Weight (pts)
            </label>
            <input
              type="number"
              value={weights.tamperingEla}
              onChange={(e) => setWeights({ ...weights, tamperingEla: Number(e.target.value) })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 font-mono text-navy-950"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Expired Mandatory Document Weight (pts)
            </label>
            <input
              type="number"
              value={weights.expiredDoc}
              onChange={(e) => setWeights({ ...weights, expiredDoc: Number(e.target.value) })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 font-mono text-navy-950"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Missing Mandatory Evidence Weight (pts)
            </label>
            <input
              type="number"
              value={weights.missingMandatory}
              onChange={(e) => setWeights({ ...weights, missingMandatory: Number(e.target.value) })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 font-mono text-navy-950"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            className="px-5 py-2 rounded-xl text-xs font-bold bg-navy-950 hover:bg-navy-900 text-white shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Save className="w-3.5 h-3.5" />
            <span>Save Calibrated Thresholds</span>
          </button>
        </div>
      </form>

      {/* Storage and AI Mode Info */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 text-xs">
        <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider flex items-center gap-2">
          <Database className="w-4 h-4 text-teal-600" />
          Infrastructure & Privacy Isolation
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-400 font-semibold block text-[11px]">Database Backend</span>
            <p className="font-bold text-navy-950 mt-1">MongoDB Atlas / Local JSON Fallback</p>
            <p className="text-[10px] text-slate-500 mt-0.5">Resilient offline execution active</p>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-400 font-semibold block text-[11px]">Storage Abstraction</span>
            <p className="font-bold text-navy-950 mt-1">Local Sandboxed Filesystem</p>
            <p className="text-[10px] text-slate-500 mt-0.5">S3-compatible adapter ready</p>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-400 font-semibold block text-[11px]">AI Processing Mode</span>
            <p className="font-bold text-navy-950 mt-1">Local Deterministic Pipeline</p>
            <p className="text-[10px] text-slate-500 mt-0.5">No unconsented external transmission</p>
          </div>
        </div>
      </div>

      {/* Privacy Notice */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3 text-xs leading-relaxed text-slate-600">
        <div className="flex items-center gap-2 text-navy-950 font-bold text-sm">
          <Lock className="w-4 h-4 text-teal-600" />
          Privacy Notice & Statutory Safeguards
        </div>
        <p>
          VERITRUST AI is architected as an institutional decision-support system. All uploaded credentials are treated as untrusted data
          and subjected to strict magic byte validation, cryptographic hash tracking, and isolated PDF parsing.
        </p>
        <p>
          In compliance with AICTE and Digital Personal Data Protection (DPDP) principles, raw identity records are never exposed without
          authenticated role permissions. Machine learning risk scores indicate review routing urgency, strictly preserving final consequential
          decision authority for designated human verification officers.
        </p>
      </div>
    </div>
  );
};
