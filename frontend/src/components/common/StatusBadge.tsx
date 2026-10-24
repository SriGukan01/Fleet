import React from 'react';
import { ApplicationStatus } from '../../types';

interface Props {
  status: ApplicationStatus | string;
}

export const StatusBadge: React.FC<Props> = ({ status }) => {
  const getStyle = () => {
    switch (status.toLowerCase()) {
      case 'approved':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'rejected':
        return 'bg-rose-100 text-rose-800 border-rose-300';
      case 'needs_evidence':
        return 'bg-purple-100 text-purple-800 border-purple-300';
      case 'under_review':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'processing':
        return 'bg-teal-100 text-teal-800 border-teal-300 animate-pulse';
      case 'submitted':
      default:
        return 'bg-slate-100 text-slate-800 border-slate-300';
    }
  };

  const formatText = (text: string) => {
    return text.replace(/_/g, ' ').toUpperCase();
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border ${getStyle()}`}
    >
      {formatText(status)}
    </span>
  );
};
