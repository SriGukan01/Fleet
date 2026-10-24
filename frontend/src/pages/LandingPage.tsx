import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  ShieldCheck,
  CheckCircle,
  FileSearch,
  Scale,
  Sparkles,
  ArrowRight,
  Lock,
  Layers,
  Cpu,
  UserCheck2,
  FileCheck2,
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { demoLogin } = useAuth();

  const handleQuickDemo = async (role: 'officer' | 'applicant' | 'admin') => {
    await demoLogin(role);
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans selection:bg-teal-500 selection:text-white">
      {/* Top Bar */}
      <header className="border-b border-slate-800 bg-navy-950/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-18 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-teal-400 flex items-center justify-center text-white shadow-lg shadow-teal-500/20">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-white font-['Plus_Jakarta_Sans']">
                VERITRUST <span className="text-teal-400">AI</span>
              </span>
              <span className="ml-2 px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                SIH26261 • AICTE
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={() => handleQuickDemo('officer')}
              className="px-4 py-2 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-600/30 transition-all flex items-center gap-2 hover:scale-[1.02]"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Launch Officer Demo</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => navigate('/login')}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:text-white border border-slate-700 hover:border-slate-600 transition-all"
            >
              Sign In
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-24 overflow-hidden bg-gradient-to-b from-navy-950 via-slate-900 to-slate-900 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-6 text-center space-y-8 relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-teal-950/80 border border-teal-800/80 text-teal-300 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-teal-400" />
            <span>AICTE Smart Automation • Problem Statement SIH26261</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight max-w-4xl mx-auto font-['Plus_Jakarta_Sans'] leading-tight">
            AI-Powered Application Validation, Document Authentication &{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-cyan-300">
              Regulatory Compliance
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-400 max-w-3xl mx-auto leading-relaxed">
            Automating application scrutiny, multi-document correlation, tampering forensics, and statutory compliance
            verification with explainable, evidence-backed human-in-the-loop workflows.
          </p>

          {/* Interactive Demo Call to Actions */}
          <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => handleQuickDemo('officer')}
              className="px-6 py-3.5 rounded-xl text-sm font-bold bg-teal-500 hover:bg-teal-400 text-navy-950 shadow-xl shadow-teal-500/25 transition-all flex items-center gap-2 hover:scale-[1.03]"
            >
              <UserCheck2 className="w-4 h-4" />
              <span>Enter as Verification Officer</span>
            </button>

            <button
              onClick={() => handleQuickDemo('applicant')}
              className="px-6 py-3.5 rounded-xl text-sm font-bold bg-slate-800 hover:bg-slate-700 text-white border border-slate-700 transition-all flex items-center gap-2"
            >
              <FileCheck2 className="w-4 h-4 text-teal-400" />
              <span>Submit as Applicant</span>
            </button>

            <button
              onClick={() => {
                demoLogin('officer').then(() => navigate('/scenarios'));
              }}
              className="px-6 py-3.5 rounded-xl text-sm font-bold bg-navy-900 hover:bg-navy-800 text-teal-300 border border-teal-800/60 transition-all flex items-center gap-2"
            >
              <Sparkles className="w-4 h-4" />
              <span>Explore 6 Synthetic Scenarios</span>
            </button>
          </div>
        </div>
      </section>

      {/* 3-Step Systematic Verification Workflow */}
      <section className="py-20 bg-slate-900 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-6 space-y-12">
          <div className="text-center space-y-3">
            <p className="text-xs font-bold text-teal-400 uppercase tracking-widest">Architectural Methodology</p>
            <h2 className="text-3xl font-bold text-white font-['Plus_Jakarta_Sans']">
              Three-Tier Explainable Verification Architecture
            </h2>
            <p className="text-sm text-slate-400 max-w-2xl mx-auto">
              Moving beyond naive OCR scores: triangulating digital forensics, multi-credential correlation, and deterministic policy rules.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="p-7 rounded-2xl bg-slate-800/60 border border-slate-700/80 space-y-4 hover:border-teal-500/50 transition-all">
              <div className="w-12 h-12 rounded-xl bg-teal-900/60 border border-teal-700/50 flex items-center justify-center text-teal-400">
                <FileSearch className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">1. Forensic Document Ingestion</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Cryptographic SHA-256 duplicate detection, PDF object metadata inspection, Laplacian sharpness assessment,
                and Error Level Analysis (ELA) for image compression anomalies.
              </p>
            </div>

            {/* Step 2 */}
            <div className="p-7 rounded-2xl bg-slate-800/60 border border-slate-700/80 space-y-4 hover:border-teal-500/50 transition-all">
              <div className="w-12 h-12 rounded-xl bg-cyan-900/60 border border-cyan-700/50 flex items-center justify-center text-cyan-400">
                <Layers className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">2. Cross-Document Correlation</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Pairwise cross-credential entity matching (applicant name, DOB, marks, roll number) with normalized Levenshtein
                fuzzy scoring to catch subtle identity contradictions.
              </p>
            </div>

            {/* Step 3 */}
            <div className="p-7 rounded-2xl bg-slate-800/60 border border-slate-700/80 space-y-4 hover:border-teal-500/50 transition-all">
              <div className="w-12 h-12 rounded-xl bg-indigo-900/60 border border-indigo-700/50 flex items-center justify-center text-indigo-400">
                <Scale className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">3. Deterministic Compliance Engine</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Ground-truth evaluation against configured AICTE and central policy handbooks with explicit section citations,
                calculating a weighted Review Priority Score (0-100).
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust & Ethical AI Principles */}
      <section className="py-16 bg-navy-950/70">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-2">
            <h3 className="text-lg font-bold text-white font-['Plus_Jakarta_Sans'] flex items-center gap-2">
              <Lock className="w-5 h-5 text-teal-400" />
              Statutory Transparency & Responsible Scrutiny
            </h3>
            <p className="text-xs text-slate-400 max-w-3xl leading-relaxed">
              VERITRUST AI strictly avoids autonomous rejections. Inconsistency indicators flag review urgency for authorized human officers.
              Reports are decision-support summaries, not government-certified forensic certificates.
            </p>
          </div>
          <button
            onClick={() => handleQuickDemo('officer')}
            className="px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shrink-0 shadow-lg shadow-teal-600/20"
          >
            Launch Live Demo Workbench &rarr;
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800 bg-navy-950 py-8 text-center text-xs text-slate-500 space-y-2">
        <p>VERITRUST AI • SIH26261 | AICTE Smart Automation Hackathon Prototype</p>
        <p className="text-[11px] text-slate-600">Built with React, Vite, Tailwind CSS, FastAPI, and Explainable Forensic Intelligence.</p>
      </footer>
    </div>
  );
};
