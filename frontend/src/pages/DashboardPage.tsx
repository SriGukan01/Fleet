import React, { useEffect, useState } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { Application } from '../types';
import { StatCard } from '../components/common/StatCard';
import { PriorityBadge } from '../components/common/PriorityBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import {
  FileText,
  Clock,
  CheckCircle2,
  AlertTriangle,
  FileCheck2,
  Cpu,
  Layers,
  ArrowRight,
  TrendingUp,
  Sparkles,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  CartesianGrid,
} from 'recharts';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState<any>(null);
  const [recentApps, setRecentApps] = useState<Application[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [anData, appsData] = await Promise.all([
          apiRequest<any>('/api/analytics/overview'),
          apiRequest<Application[]>('/api/applications'),
        ]);
        setAnalytics(anData);
        setRecentApps(appsData.slice(0, 6));
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-3">
          <div className="w-10 h-10 border-4 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-semibold text-slate-500">Aggregating Scrutiny Records...</p>
        </div>
      </div>
    );
  }

  const kpis = analytics?.kpis || {};
  const funnel = analytics?.funnel_data || [];
  const priorityData = analytics?.priority_data || [];
  const categoryData = analytics?.category_data || [];
  const ruleData = analytics?.rule_failure_data || [];

  const CATEGORY_COLORS = ['#0D9488', '#0284C7', '#4F46E5', '#D97706'];

  return (
    <div className="space-y-8 font-sans">
      {/* Page Title & Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 tracking-tight font-['Plus_Jakarta_Sans']">
            Scrutiny & Verification Analytics Overview
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time pipeline metrics, automated forensic assessments, and regulatory rule clearance.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <NavLink
            to="/scenarios"
            className="px-4 py-2 rounded-xl text-xs font-bold bg-navy-900 hover:bg-navy-800 text-teal-300 border border-teal-700/50 shadow-sm transition-all flex items-center gap-1.5"
          >
            <Sparkles className="w-3.5 h-3.5 text-teal-400" />
            <span>Judge Test Scenarios</span>
          </NavLink>

          <NavLink
            to="/applications/new"
            className="px-4 py-2 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-600/20 transition-all flex items-center gap-1.5"
          >
            <span>+ New Intake</span>
          </NavLink>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Total Applications"
          value={kpis.total_applications || 0}
          subtitle={`${kpis.total_documents || 0} documents processed`}
          icon={<FileText className="w-5 h-5" />}
        />
        <StatCard
          title="Awaiting Review"
          value={kpis.under_review_count || 0}
          subtitle="Human officer scrutiny needed"
          icon={<Clock className="w-5 h-5" />}
        />
        <StatCard
          title="Adjudicated Approved"
          value={kpis.approved_count || 0}
          subtitle="Clearance rate verified"
          icon={<CheckCircle2 className="w-5 h-5 text-emerald-600" />}
        />
        <StatCard
          title="Discrepancies Flagged"
          value={kpis.total_contradictions_detected || 0}
          subtitle={`${kpis.cross_checks_performed || 0} cross-checks performed`}
          icon={<AlertTriangle className="w-5 h-5 text-rose-600" />}
        />
      </div>

      {/* Secondary Metrics Bar */}
      <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-sm flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-teal-600" />
          <span className="text-slate-600">Average OCR Layout Confidence:</span>
          <span className="font-bold font-mono text-navy-950 bg-teal-50 px-2 py-0.5 rounded border border-teal-100">
            {kpis.avg_ocr_confidence || 95}%
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-600" />
          <span className="text-slate-600">Active Rule Set:</span>
          <span className="font-bold text-navy-900">AICTE Technical Process 2024-25 Norms</span>
        </div>
        <div className="flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-indigo-600" />
          <span className="text-slate-600">Decision Paradigm:</span>
          <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100">
            Human-in-the-Loop Active
          </span>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Verification Funnel */}
        <div className="lg:col-span-7 bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-sm font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
                Application Scrutiny Funnel
              </h3>
              <p className="text-[11px] text-slate-500">Live progression through AI pipeline stages</p>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnel} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E2E8F0" />
                <XAxis type="number" textAnchor="end" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis dataKey="stage" type="category" tick={{ fontSize: 11, fill: '#334E68', fontWeight: 500 }} width={120} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0B192C', color: '#fff', borderRadius: '8px', fontSize: '11px' }}
                />
                <Bar dataKey="count" fill="#0D9488" radius={[0, 6, 6, 0]} barSize={22} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Review Priority Distribution */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-sm font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
                Review Priority Routing
              </h3>
              <p className="text-[11px] text-slate-500">Weighted score distributions (0 - 100)</p>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priorityData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="name" angle={-15} textAnchor="end" tick={{ fontSize: 10, fill: '#64748B' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} allowDecimals={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0B192C', color: '#fff', borderRadius: '8px', fontSize: '11px' }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]} barSize={36}>
                  {priorityData.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Applications Scrutiny Queue Table */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden space-y-4 p-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-base font-bold text-navy-950 font-['Plus_Jakarta_Sans']">
              Priority Verification Scrutiny Queue
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Applications prioritized by deterministic rule violations and multi-document consistency.
            </p>
          </div>
          <NavLink
            to="/applications"
            className="text-xs font-bold text-teal-600 hover:text-teal-700 flex items-center gap-1"
          >
            <span>View All Registry</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </NavLink>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50/80 text-[11px] font-bold text-slate-700 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-4 py-3">Reference ID</th>
                <th className="px-4 py-3">Applicant Name</th>
                <th className="px-4 py-3">Category</th>
                <th className="px-4 py-3">Review Priority</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {recentApps.map((app) => (
                <tr key={app.id || app._id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="px-4 py-3 font-mono font-semibold text-teal-800">
                    {app.reference_id}
                  </td>
                  <td className="px-4 py-3 font-medium text-navy-950">
                    {app.applicant_name}
                  </td>
                  <td className="px-4 py-3">
                    <span className="capitalize">{app.category.replace('_', ' ')}</span>
                  </td>
                  <td className="px-4 py-3">
                    <PriorityBadge score={app.review_priority_score} level={app.review_priority_level} />
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge status={app.status} />
                  </td>
                  <td className="px-4 py-3 text-right space-x-2">
                    <button
                      onClick={() => navigate(`/applications/${app.id || app._id}/review`)}
                      className="px-3 py-1.5 rounded-lg bg-navy-900 hover:bg-navy-800 text-white font-semibold text-[11px] transition-colors"
                    >
                      Review
                    </button>
                    <button
                      onClick={() => navigate(`/applications/${app.id || app._id}`)}
                      className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-[11px] transition-colors"
                    >
                      Detail
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
