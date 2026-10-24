import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, UserCheck, LogOut, Sparkles, Building, Key } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const { user, logout, demoLogin } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 bg-navy-950/95 backdrop-blur-md border-b border-navy-800 text-white shadow-sm">
      <div className="px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/dashboard')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-teal-400 flex items-center justify-center text-white shadow-lg shadow-teal-500/20">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-tight text-white font-['Plus_Jakarta_Sans']">
                VERITRUST <span className="text-teal-400">AI</span>
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                SIH26261
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">AICTE Smart Automation • Document Authentication</p>
          </div>
        </div>

        {/* Demo Role Switcher & User Profile */}
        <div className="flex items-center gap-3 sm:gap-4">
          {/* 1-Click Role Switcher for Hackathon Judges */}
          <div className="hidden md:flex items-center gap-1 bg-navy-900/90 p-1 rounded-lg border border-navy-700/80">
            <span className="text-[11px] text-slate-400 px-2 font-medium flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-teal-400" />
              Role:
            </span>
            <button
              onClick={() => demoLogin('applicant')}
              className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                user?.role === 'applicant'
                  ? 'bg-teal-600 text-white shadow-sm'
                  : 'text-slate-300 hover:text-white hover:bg-navy-800'
              }`}
            >
              Applicant
            </button>
            <button
              onClick={() => demoLogin('officer')}
              className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                user?.role === 'officer'
                  ? 'bg-teal-600 text-white shadow-sm'
                  : 'text-slate-300 hover:text-white hover:bg-navy-800'
              }`}
            >
              Officer
            </button>
            <button
              onClick={() => demoLogin('admin')}
              className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                user?.role === 'admin'
                  ? 'bg-teal-600 text-white shadow-sm'
                  : 'text-slate-300 hover:text-white hover:bg-navy-800'
              }`}
            >
              Admin
            </button>
          </div>

          {/* User Profile */}
          {user ? (
            <div className="flex items-center gap-3 pl-2 border-l border-navy-800">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-semibold text-slate-200">{user.name}</p>
                <p className="text-[10px] text-teal-400 uppercase font-mono tracking-wider">
                  {user.role} {user.is_demo && '• DEMO'}
                </p>
              </div>
              <button
                onClick={logout}
                title="Logout"
                className="p-2 rounded-lg bg-navy-900 text-slate-400 hover:text-white hover:bg-navy-800 border border-navy-700/60 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => navigate('/login')}
              className="px-3.5 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white text-xs font-semibold transition-all shadow-sm"
            >
              Demo Access
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
