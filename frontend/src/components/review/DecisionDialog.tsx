import React, { useState } from 'react';
import { CheckCircle2, XCircle, AlertCircle, HelpCircle, ArrowUpRight } from 'lucide-react';
import confetti from 'canvas-confetti';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (action: string, reason: string, notes?: string) => Promise<void>;
  applicationRef: string;
}

export const DecisionDialog: React.FC<Props> = ({ isOpen, onClose, onSubmit, applicationRef }) => {
  const [action, setAction] = useState<'approve' | 'reject' | 'request_evidence' | 'escalate'>('approve');
  const [reason, setReason] = useState<string>('');
  const [notes, setNotes] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reason || reason.trim().length < 8) {
      setError('A mandatory justification reason (at least 8 characters) is legally required for consequential decisions.');
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      await onSubmit(action, reason.trim(), notes.trim() || undefined);
      if (action === 'approve') {
        // Trigger celebratory confetti on legitimate approval
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#0D9488', '#14B8A6', '#0B192C'],
        });
      }
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to record decision');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/60 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div>
            <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
              Finalize Officer Adjudication
            </h3>
            <p className="text-xs text-slate-500">Application: {applicationRef}</p>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          {error && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-700 font-medium flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Action Choice Buttons */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Select Adjudication Outcome
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setAction('approve')}
                className={`p-3 rounded-xl border text-xs font-bold flex items-center gap-2 transition-all ${
                  action === 'approve'
                    ? 'border-emerald-500 bg-emerald-50 text-emerald-800 ring-2 ring-emerald-500/20'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Approve Application
              </button>

              <button
                type="button"
                onClick={() => setAction('reject')}
                className={`p-3 rounded-xl border text-xs font-bold flex items-center gap-2 transition-all ${
                  action === 'reject'
                    ? 'border-rose-500 bg-rose-50 text-rose-800 ring-2 ring-rose-500/20'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <XCircle className="w-4 h-4 text-rose-600" />
                Reject Application
              </button>

              <button
                type="button"
                onClick={() => setAction('request_evidence')}
                className={`p-3 rounded-xl border text-xs font-bold flex items-center gap-2 transition-all ${
                  action === 'request_evidence'
                    ? 'border-purple-500 bg-purple-50 text-purple-800 ring-2 ring-purple-500/20'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <HelpCircle className="w-4 h-4 text-purple-600" />
                Request Evidence
              </button>

              <button
                type="button"
                onClick={() => setAction('escalate')}
                className={`p-3 rounded-xl border text-xs font-bold flex items-center gap-2 transition-all ${
                  action === 'escalate'
                    ? 'border-blue-500 bg-blue-50 text-blue-800 ring-2 ring-blue-500/20'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <ArrowUpRight className="w-4 h-4 text-blue-600" />
                Senior Officer Escalate
              </button>
            </div>
          </div>

          {/* Mandatory Reason */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
              Mandatory Justification Reason <span className="text-rose-500">*</span>
            </label>
            <p className="text-[11px] text-slate-400 mb-1.5">
              Explain why this decision is warranted based on extracted evidence, rule checks, and institutional policy.
            </p>
            <textarea
              required
              rows={3}
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="e.g. All mandatory certificates match declared identity records and comply with AICTE annual income cap norms."
              className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-slate-900"
            />
          </div>

          {/* Optional Reviewer Notes */}
          <div>
            <label className="block text-xs font-semibold text-slate-600 mb-1">
              Internal Reviewer Notes (Optional)
            </label>
            <input
              type="text"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Private note for audit trail..."
              className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900"
            />
          </div>

          <div className="pt-3 flex items-center justify-end gap-3 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-navy-950 hover:bg-navy-900 text-white shadow-md transition-all flex items-center gap-1.5 disabled:opacity-50"
            >
              {isSubmitting ? 'Recording Decision...' : 'Commit Consequential Decision'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
