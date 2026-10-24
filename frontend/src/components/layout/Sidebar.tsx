import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  FileCheck2,
  GitCompare,
  Scale,
  UserCheck2,
  Download,
  Building2,
  History,
  Settings,
  Sparkles,
  PlusCircle,
  HelpCircle,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Sidebar: React.FC = () => {
  const { user } = useAuth();

  const navItems = [
    { label: 'Overview', path: '/dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
    { label: 'Applications', path: '/applications', icon: <FileText className="w-4 h-4" /> },
    { label: 'Demo Scenarios', path: '/scenarios', icon: <Sparkles className="w-4 h-4 text-teal-500" />, badge: '6 Test Cases' },
    { label: 'Document Verification', path: '/verification', icon: <FileCheck2 className="w-4 h-4" /> },
    { label: 'Cross-Document Intelligence', path: '/cross-doc', icon: <GitCompare className="w-4 h-4" /> },
    { label: 'Compliance Rules', path: '/compliance-rules', icon: <Scale className="w-4 h-4" /> },
    { label: 'Review Workbench', path: '/review', icon: <UserCheck2 className="w-4 h-4" /> },
    { label: 'Reports', path: '/reports', icon: <Download className="w-4 h-4" /> },
    { label: 'Issuer Registries', path: '/issuers', icon: <Building2 className="w-4 h-4" /> },
    { label: 'Audit Trail', path: '/audit', icon: <History className="w-4 h-4" /> },
    { label: 'Settings & Privacy', path: '/settings', icon: <Settings className="w-4 h-4" /> },
  ];

  return (
    <aside className="w-64 bg-navy-900 border-r border-navy-800 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="p-4 space-y-6">
        {/* New Application CTA */}
        <NavLink
          to="/applications/new"
          className="flex items-center justify-center gap-2 w-full py-2.5 px-4 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs shadow-md shadow-teal-700/20 transition-all hover:scale-[1.02]"
        >
          <PlusCircle className="w-4 h-4" />
          <span>New Application Intake</span>
        </NavLink>

        {/* Navigation Section */}
        <div className="space-y-1">
          <p className="px-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
            Platform Scrutiny
          </p>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-teal-500/15 text-teal-300 font-semibold border-l-2 border-teal-400 pl-2.5'
                    : 'text-slate-300 hover:text-white hover:bg-navy-800/80'
                }`
              }
            >
              <div className="flex items-center gap-2.5">
                {item.icon}
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                  {item.badge}
                </span>
              )}
            </NavLink>
          ))}
        </div>
      </div>

      {/* Institutional Security Notice */}
      <div className="p-4 m-3 rounded-xl bg-navy-950/70 border border-navy-800 text-[11px] text-slate-400 space-y-1.5">
        <div className="flex items-center gap-1.5 text-teal-400 font-semibold text-xs">
          <HelpCircle className="w-3.5 h-3.5" />
          <span>Human-in-the-Loop</span>
        </div>
        <p className="leading-relaxed">
          AI provides automated inconsistency indicators; only authorized officers finalize consequential adjudications.
        </p>
      </div>
    </aside>
  );
};
