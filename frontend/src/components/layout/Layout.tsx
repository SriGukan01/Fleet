import React from 'react';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { Sparkles, Info } from 'lucide-react';
import { NavLink } from 'react-router-dom';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      {/* Demo Banner */}
      <div className="bg-gradient-to-r from-navy-900 via-teal-950 to-navy-900 border-b border-teal-800/40 px-4 py-1.5 text-xs text-slate-300 flex items-center justify-between">
        <div className="flex items-center gap-2 max-w-4xl mx-auto sm:mx-0">
          <Sparkles className="w-3.5 h-3.5 text-teal-400 shrink-0" />
          <span>
            <b>HACKATHON DEMO ENVIRONMENT:</b> Pre-seeded with 6 synthetic AICTE test scenarios & local verification engines.
          </span>
        </div>
        <div className="hidden sm:flex items-center gap-3">
          <NavLink
            to="/scenarios"
            className="text-teal-300 hover:text-white font-semibold underline underline-offset-2 flex items-center gap-1 text-[11px]"
          >
            Launch Demo Scenarios &rarr;
          </NavLink>
        </div>
      </div>

      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 lg:p-8 max-w-7xl mx-auto w-full overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};
