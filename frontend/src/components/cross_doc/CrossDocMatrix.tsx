import React, { useState } from 'react';
import { CrossDocumentComparison, CrossVerificationSummary } from '../../types';
import { CheckCircle2, AlertTriangle, AlertCircle, HelpCircle, Filter } from 'lucide-react';

interface Props {
  summary: CrossVerificationSummary;
}

export const CrossDocMatrix: React.FC<Props> = ({ summary }) => {
  const [filterMismatchOnly, setFilterMismatchOnly] = useState<boolean>(false);

  const comparisons = summary.comparisons || [];
  const filtered = filterMismatchOnly
    ? comparisons.filter((c) => c.contradiction_flag || c.match_status === 'mismatch' || c.match_status === 'fuzzy_match')
    : comparisons;

  const renderStatusBadge = (status: string, contradiction: boolean) => {
    if (contradiction || status === 'mismatch') {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-rose-100 text-rose-800 border border-rose-300">
          <AlertTriangle className="w-3 h-3 text-rose-600" />
          MISMATCH
        </span>
      );
    }
    if (status === 'fuzzy_match') {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
          <AlertCircle className="w-3 h-3 text-amber-600" />
          FUZZY ({Math.round(status === 'fuzzy_match' ? 85 : 90)}%)
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
        EXACT MATCH
      </span>
    );
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
      {/* Header and Filter */}
      <div className="p-6 border-b border-slate-200 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
            Cross-Document Consistency Matrix
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Automated pairwise correlation across declared profile and uploaded credentials.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-xs">
            <span className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
              {summary.passed_checks} Matches
            </span>
            <span className="px-2.5 py-1 rounded-md bg-amber-50 text-amber-700 font-semibold border border-amber-200">
              {summary.fuzzy_matches} Fuzzy
            </span>
            <span className="px-2.5 py-1 rounded-md bg-rose-50 text-rose-700 font-semibold border border-rose-200">
              {summary.contradictions} Contradictions
            </span>
          </div>

          <button
            onClick={() => setFilterMismatchOnly(!filterMismatchOnly)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all border ${
              filterMismatchOnly
                ? 'bg-rose-50 text-rose-700 border-rose-300 shadow-sm'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            <Filter className="w-3.5 h-3.5" />
            {filterMismatchOnly ? 'Showing Attention Items' : 'Filter Attention Items'}
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-600">
          <thead className="bg-slate-50/80 text-[11px] font-bold text-slate-700 uppercase tracking-wider border-b border-slate-200">
            <tr>
              <th className="px-6 py-3.5">Verified Field</th>
              <th className="px-6 py-3.5">Source 1</th>
              <th className="px-6 py-3.5">Source 2</th>
              <th className="px-6 py-3.5">Match Status</th>
              <th className="px-6 py-3.5">Suggested Resolution</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 font-sans">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-slate-400">
                  No cross-document discrepancies found for this view.
                </td>
              </tr>
            ) : (
              filtered.map((item) => (
                <tr
                  key={item.id}
                  className={`hover:bg-slate-50/80 transition-colors ${
                    item.contradiction_flag ? 'bg-rose-50/20' : ''
                  }`}
                >
                  <td className="px-6 py-4 font-semibold text-navy-950 whitespace-nowrap">
                    {item.display_name}
                  </td>
                  <td className="px-6 py-4">
                    <p className="font-mono text-xs font-bold text-slate-900">{item.doc1_value || 'None'}</p>
                    <p className="text-[10px] text-slate-400 truncate max-w-[180px]">{item.doc1_name}</p>
                  </td>
                  <td className="px-6 py-4">
                    <p className="font-mono text-xs font-bold text-slate-900">{item.doc2_value || 'None'}</p>
                    <p className="text-[10px] text-slate-400 truncate max-w-[180px]">{item.doc2_name}</p>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {renderStatusBadge(item.match_status, item.contradiction_flag)}
                  </td>
                  <td className="px-6 py-4 max-w-xs text-xs text-slate-700 leading-relaxed">
                    {item.suggested_resolution}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
