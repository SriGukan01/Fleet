import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { Scale, BookOpen, PlusCircle, CheckCircle2, AlertCircle, ExternalLink, ShieldCheck } from 'lucide-react';

export const ComplianceRulesPage: React.FC = () => {
  const [rules, setRules] = useState<any[]>([]);
  const [sources, setSources] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'rules' | 'knowledge'>('rules');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [toggleLoading, setToggleLoading] = useState<string | null>(null);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [rData, sData] = await Promise.all([
        apiRequest<any[]>('/api/compliance-rules'),
        apiRequest<any[]>('/api/compliance-rules/sources'),
      ]);
      setRules(rData);
      setSources(sData);
    } catch (err) {
      console.error('Failed to load rules:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleToggleRule = async (ruleId: string, currentActive: boolean) => {
    setToggleLoading(ruleId);
    try {
      await apiRequest(`/api/compliance-rules/${ruleId}`, {
        method: 'PATCH',
        body: JSON.stringify({ is_active: !currentActive }),
      });
      await fetchData();
    } catch (err) {
      console.error('Failed to toggle rule:', err);
    } finally {
      setToggleLoading(null);
    }
  };

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
            Regulatory Compliance Rules & Policy Knowledge
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Grounded rule engine based on statutory AICTE norms, National Scholarship Portal guidelines, and UGC frameworks.
          </p>
        </div>

        {/* Tab switcher */}
        <div className="flex items-center bg-white rounded-xl p-1 border border-slate-200">
          <button
            onClick={() => setActiveTab('rules')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'rules'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Scale className="w-3.5 h-3.5" />
            Configured Rules ({rules.length})
          </button>
          <button
            onClick={() => setActiveTab('knowledge')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'knowledge'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            Statutory Sources ({sources.length})
          </button>
        </div>
      </div>

      {activeTab === 'rules' ? (
        <div className="space-y-4">
          {rules.map((rule) => {
            const rId = rule._id || rule.rule_id;
            const isActive = rule.is_active !== false;
            return (
              <div
                key={rId}
                className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm space-y-3 transition-all hover:border-slate-300"
              >
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-teal-800 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                        {rule.rule_id}
                      </span>
                      <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
                        {rule.jurisdiction} • {rule.application_type}
                      </span>
                      <span
                        className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                          rule.severity === 'critical'
                            ? 'bg-red-100 text-red-800'
                            : rule.severity === 'high'
                            ? 'bg-orange-100 text-orange-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {rule.severity} Severity
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
                      {rule.name}
                    </h3>
                  </div>

                  <button
                    onClick={() => handleToggleRule(rId, isActive)}
                    disabled={toggleLoading === rId}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border ${
                      isActive
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-300 hover:bg-emerald-100'
                        : 'bg-slate-100 text-slate-500 border-slate-300 hover:bg-slate-200'
                    }`}
                  >
                    {isActive ? '✓ Rule Active' : '✕ Disabled'}
                  </button>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed">{rule.explanation}</p>

                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1 text-slate-600">
                  <p className="font-semibold text-navy-900">
                    Statutory Source: {rule.policy_reference?.title} ({rule.policy_reference?.section_or_clause})
                  </p>
                  <p className="italic text-slate-500 text-[11px]">
                    "{rule.policy_reference?.excerpt}"
                  </p>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-100">
                  <span>Rule Type: <b className="text-slate-600">{rule.rule_type}</b></span>
                  <span>Version: {rule.version || '1.0'}</span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {sources.map((s, idx) => (
            <div
              key={idx}
              className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-teal-700 uppercase tracking-wider bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                  {s.authority}
                </span>
                <span className="text-[10px] text-slate-400">Effective: {s.effective_date}</span>
              </div>
              <h3 className="font-bold text-navy-950 text-sm">{s.title}</h3>
              <p className="text-xs font-semibold text-teal-800">{s.clause}</p>
              <blockquote className="p-3 rounded-lg bg-slate-50 border-l-2 border-teal-500 text-xs italic text-slate-600 leading-relaxed">
                "{s.excerpt}"
              </blockquote>
              {s.source_url && (
                <a
                  href={s.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-teal-600 hover:underline flex items-center gap-1 font-semibold text-xs"
                >
                  <span>Verify at Official Portal</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
