import React, { useState, useEffect } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { Application, ApplicationCategory, ApplicationStatus, ReviewPriorityLevel } from '../types';
import { PriorityBadge } from '../components/common/PriorityBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import {
  Search,
  Filter,
  PlusCircle,
  FileSearch,
  UserCheck2,
  Download,
  Eye,
  RefreshCw,
  Sparkles,
} from 'lucide-react';

export const ApplicationsPage: React.FC = () => {
  const navigate = useNavigate();
  const [applications, setApplications] = useState<Application[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [priorityFilter, setPriorityFilter] = useState<string>('');

  const fetchApplications = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      if (categoryFilter) params.append('category', categoryFilter);
      if (statusFilter) params.append('status', statusFilter);
      if (priorityFilter) params.append('priority_level', priorityFilter);
      if (search) params.append('search', search);

      const data = await apiRequest<Application[]>(`/api/applications?${params.toString()}`);
      setApplications(data);
    } catch (err) {
      console.error('Failed to load applications:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, [categoryFilter, statusFilter, priorityFilter]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchApplications();
  };

  return (
    <div className="space-y-6 font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 tracking-tight font-['Plus_Jakarta_Sans']">
            Application Intake & Scrutiny Registry
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Search, filter, and inspect institutional submissions across configured compliance frameworks.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchApplications}
            className="p-2.5 rounded-xl border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-colors shadow-sm"
            title="Refresh Registry"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          <NavLink
            to="/applications/new"
            className="px-4 py-2.5 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-600/20 transition-all flex items-center gap-1.5"
          >
            <PlusCircle className="w-4 h-4" />
            <span>New Application Intake</span>
          </NavLink>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <form onSubmit={handleSearchSubmit} className="flex-1 min-w-[260px] relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by reference ID, applicant name, or email..."
            className="w-full pl-10 pr-4 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900 placeholder:text-slate-400"
          />
        </form>

        <div className="flex flex-wrap items-center gap-3 text-xs">
          {/* Category Filter */}
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            <option value="">All Categories</option>
            <option value="scholarship">Scholarship</option>
            <option value="admissions">Admissions</option>
            <option value="recruitment">Recruitment</option>
            <option value="regulatory_licensing">Regulatory Licensing</option>
          </select>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            <option value="">All Statuses</option>
            <option value="submitted">Submitted</option>
            <option value="under_review">Under Review</option>
            <option value="needs_evidence">Needs Evidence</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
          </select>

          {/* Priority Level */}
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            <option value="">All Priority Levels</option>
            <option value="low_concern">Low Concern</option>
            <option value="moderate_concern">Moderate Concern</option>
            <option value="high_concern">High Concern</option>
            <option value="critical_review_required">Critical Review</option>
          </select>
        </div>
      </div>

      {/* Applications Table */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50/80 text-[11px] font-bold text-slate-700 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-5 py-3.5">Reference ID</th>
                <th className="px-5 py-3.5">Applicant Details</th>
                <th className="px-5 py-3.5">Category</th>
                <th className="px-5 py-3.5">Review Priority</th>
                <th className="px-5 py-3.5">Docs</th>
                <th className="px-5 py-3.5">Status</th>
                <th className="px-5 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="px-5 py-12 text-center text-slate-400">
                    <div className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
                    Loading registry applications...
                  </td>
                </tr>
              ) : applications.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-5 py-12 text-center text-slate-400 space-y-2">
                    <FileSearch className="w-8 h-8 text-slate-300 mx-auto" />
                    <p className="text-sm font-semibold text-slate-600">No applications found</p>
                    <p className="text-xs">Adjust your search filters or create a new application intake.</p>
                  </td>
                </tr>
              ) : (
                applications.map((app) => (
                  <tr key={app.id || app._id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-5 py-4 font-mono font-bold text-teal-800 whitespace-nowrap">
                      {app.reference_id}
                    </td>
                    <td className="px-5 py-4">
                      <p className="font-bold text-navy-950 text-xs">{app.applicant_name}</p>
                      <p className="text-[11px] text-slate-400">{app.applicant_email}</p>
                    </td>
                    <td className="px-5 py-4">
                      <span className="capitalize font-medium text-slate-700">
                        {app.category.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <PriorityBadge score={app.review_priority_score} level={app.review_priority_level} />
                    </td>
                    <td className="px-5 py-4 font-mono text-slate-700">
                      {app.document_ids?.length || 0}
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <StatusBadge status={app.status} />
                    </td>
                    <td className="px-5 py-4 text-right whitespace-nowrap space-x-1.5">
                      <button
                        onClick={() => navigate(`/applications/${app.id || app._id}/review`)}
                        className="px-2.5 py-1.5 rounded-lg bg-navy-950 hover:bg-navy-900 text-white font-semibold text-[11px] transition-colors"
                      >
                        Workbench
                      </button>
                      <button
                        onClick={() => navigate(`/applications/${app.id || app._id}`)}
                        className="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-[11px] transition-colors"
                      >
                        Details
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
