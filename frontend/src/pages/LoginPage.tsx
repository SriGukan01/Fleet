import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, UserCheck2, FileText, Settings, Sparkles, ArrowRight, Lock, AlertCircle } from 'lucide-react';
import { UserRole } from '../types';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, demoLogin, isLoading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleStandardLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed. Check your credentials.');
    }
  };

  const handleDemoAccess = async (role: UserRole) => {
    setError(null);
    try {
      await demoLogin(role);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Demo login failed');
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans selection:bg-teal-500 selection:text-white">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-teal-500 to-teal-400 mx-auto flex items-center justify-center text-white shadow-xl shadow-teal-500/25">
          <ShieldCheck className="w-7 h-7" />
        </div>
        <h2 className="text-2xl font-extrabold text-white tracking-tight font-['Plus_Jakarta_Sans']">
          Sign In to VERITRUST AI
        </h2>
        <p className="text-xs text-slate-400">
          AICTE Smart Automation • Application & Document Scrutiny
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-xl px-4">
        <div className="bg-slate-800/90 py-8 px-6 sm:px-10 rounded-2xl shadow-2xl border border-slate-700/80 space-y-6">
          {/* Hackathon 1-Click Quick Demo Access */}
          <div className="p-4 rounded-xl bg-navy-950/80 border border-teal-800/50 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-teal-300 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-teal-400" />
                Hackathon Demo Access (1-Click)
              </span>
              <span className="text-[10px] text-slate-400 font-medium">No credentials needed</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              <button
                type="button"
                onClick={() => handleDemoAccess('officer')}
                disabled={isLoading}
                className="p-3 rounded-xl bg-slate-800/90 hover:bg-teal-950/80 border border-slate-700 hover:border-teal-500/60 text-left transition-all group"
              >
                <div className="flex items-center justify-between mb-1">
                  <UserCheck2 className="w-4 h-4 text-teal-400 group-hover:scale-110 transition-transform" />
                  <span className="text-[10px] font-bold text-teal-400 bg-teal-500/20 px-1.5 py-0.2 rounded">Primary</span>
                </div>
                <p className="text-xs font-bold text-white">Verification Officer</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Scrutiny & Review</p>
              </button>

              <button
                type="button"
                onClick={() => handleDemoAccess('applicant')}
                disabled={isLoading}
                className="p-3 rounded-xl bg-slate-800/90 hover:bg-slate-700 border border-slate-700 hover:border-slate-500 text-left transition-all group"
              >
                <div className="flex items-center justify-between mb-1">
                  <FileText className="w-4 h-4 text-cyan-400 group-hover:scale-110 transition-transform" />
                  <span className="text-[10px] text-slate-400 font-mono">Demo</span>
                </div>
                <p className="text-xs font-bold text-white">Applicant</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Upload & Status</p>
              </button>

              <button
                type="button"
                onClick={() => handleDemoAccess('admin')}
                disabled={isLoading}
                className="p-3 rounded-xl bg-slate-800/90 hover:bg-slate-700 border border-slate-700 hover:border-slate-500 text-left transition-all group"
              >
                <div className="flex items-center justify-between mb-1">
                  <Settings className="w-4 h-4 text-amber-400 group-hover:scale-110 transition-transform" />
                  <span className="text-[10px] text-slate-400 font-mono">Demo</span>
                </div>
                <p className="text-xs font-bold text-white">Administrator</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Rules & Registry</p>
              </button>
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-700" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-slate-800 px-3 text-slate-400 font-medium">Or Sign In with Credentials</span>
            </div>
          </div>

          {error && (
            <div className="p-3 rounded-xl bg-rose-950/60 border border-rose-800/60 text-xs text-rose-300 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleStandardLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="officer@veritrust.ai"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Demo@123"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-lg shadow-teal-600/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>{isLoading ? 'Authenticating...' : 'Sign In'}</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
