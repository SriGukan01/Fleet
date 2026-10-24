import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { DemoScenario, Application } from '../types';
import {
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Layers,
  ArrowRight,
  RefreshCw,
  Eye,
  UserCheck2,
  FileSearch,
} from 'lucide-react';

export const ScenariosDemoPage: React.FC = () => {
  const navigate = useNavigate();
  const [scenarios, setScenarios] = useState<DemoScenario[]>([]);
  const [apps, setApps] = useState<Application[]>([]);
  const [isReloading, setIsReloading] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const fetchScenariosAndApps = async () => {
    setIsLoading(true);
    try {
      const [scData, appsData] = await Promise.all([
        apiRequest<DemoScenario[]>('/api/scenarios'),
        apiRequest<Application[]>('/api/applications'),
      ]);
      setScenarios(scData);
      setApps(appsData);
    } catch (err) {
      console.error('Failed to load demo scenarios:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchScenariosAndApps();
  }, []);

  const handleReload = async () => {
    setIsReloading(true);
    try {
      await apiRequest('/api/scenarios/reload', { method: 'POST' });
      await fetchScenariosAndApps();
    } catch (err) {
      console.error('Reload failed:', err);
    } finally {
      setIsReloading(false);
    }
  };

  const findAppForScenario = (refId: string) => {
    return apps.find((a) => a.reference_id === refId);
  };

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-bold border border-teal-200 mb-1">
            <Sparkles className="w-3.5 h-3.5 text-teal-600" />
            <span>Hackathon Evaluation Showcase</span>
          </div>
          <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
            Pre-Seeded Synthetic Scenarios (6 Test Cases)
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Reproducible, evidence-backed evaluation scenarios designed for SIH26261 jury testing.
          </p>
        </div>

        <button
          onClick={handleReload}
          disabled={isReloading}
          className="px-4 py-2.5 rounded-xl text-xs font-bold bg-navy-900 hover:bg-navy-800 text-teal-300 border border-teal-800/50 shadow-sm flex items-center gap-2 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isReloading ? 'animate-spin' : ''}`} />
          <span>{isReloading ? 'Refreshing Datasets...' : 'Reset Synthetic Scenarios'}</span>
        </button>
      </div>

      {/* Scenarios Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {scenarios.map((sc, index) => {
          const matchedApp = findAppForScenario(sc.reference_id);
          const appId = matchedApp?.id || matchedApp?._id;

          return (
            <div
              key={sc.id}
              className="bg-white rounded-2xl border border-slate-200/90 shadow-sm hover:shadow-md transition-all p-6 space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2.5 py-1 rounded-lg border border-teal-200">
                    {sc.reference_id}
                  </span>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                    {sc.category}
                  </span>
                </div>

                <div>
                  <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
                    {sc.title}
                  </h3>
                  <p className="text-xs font-medium text-slate-500 mt-0.5">
                    Candidate: <b>{sc.applicant}</b>
                  </p>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed">{sc.description}</p>

                {/* Key Verification Checks */}
                <div className="space-y-1.5 pt-2">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    Expected Verification Outcomes:
                  </span>
                  <div className="space-y-1">
                    {sc.key_checks.map((chk, i) => (
                      <div
                        key={i}
                        className="text-[11px] font-mono text-slate-700 bg-slate-50 p-1.5 rounded-lg border border-slate-100 flex items-center gap-2"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                        <span>{chk}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                <div className="text-xs">
                  <span className="text-slate-400">Target Priority: </span>
                  <span className="font-bold text-navy-900">{sc.expected_level}</span>
                </div>

                <div className="flex items-center gap-2">
                  {appId ? (
                    <button
                      onClick={() => navigate(`/applications/${appId}/review`)}
                      className="px-4 py-2 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-sm flex items-center gap-1.5 transition-all"
                    >
                      <span>Review Workbench</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  ) : (
                    <span className="text-xs text-slate-400 italic">Load scenarios to inspect</span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
