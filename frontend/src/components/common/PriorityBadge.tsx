import React from 'react';
import { ReviewPriorityLevel } from '../../types';
import { ShieldCheck, AlertCircle, AlertTriangle, Flame } from 'lucide-react';

interface Props {
  score?: number;
  level?: ReviewPriorityLevel;
  showScore?: boolean;
}

export const PriorityBadge: React.FC<Props> = ({ score = 0, level = 'low_concern', showScore = true }) => {
  const getBadgeConfig = () => {
    switch (level) {
      case 'critical_review_required':
        return {
          bg: 'bg-red-50 text-red-700 border-red-200',
          icon: <Flame className="w-3.5 h-3.5 text-red-600" />,
          label: 'Critical Review',
        };
      case 'high_concern':
        return {
          bg: 'bg-orange-50 text-orange-700 border-orange-200',
          icon: <AlertTriangle className="w-3.5 h-3.5 text-orange-600" />,
          label: 'High Concern',
        };
      case 'moderate_concern':
        return {
          bg: 'bg-amber-50 text-amber-700 border-amber-200',
          icon: <AlertCircle className="w-3.5 h-3.5 text-amber-600" />,
          label: 'Moderate',
        };
      case 'low_concern':
      default:
        return {
          bg: 'bg-emerald-50 text-emerald-700 border-emerald-200',
          icon: <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />,
          label: 'Low Concern',
        };
    }
  };

  const config = getBadgeConfig();

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${config.bg} shadow-sm transition-all`}
    >
      {config.icon}
      <span>{config.label}</span>
      {showScore && <span className="opacity-75 font-mono">({score})</span>}
    </span>
  );
};
