import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { ApplicationCategory, Application } from '../types';
import {
  GraduationCap,
  Building,
  Briefcase,
  FileBadge,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  AlertCircle,
  Sparkles,
} from 'lucide-react';

export const NewApplicationWizard: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState<number>(1);
  const [category, setCategory] = useState<ApplicationCategory>('scholarship');
  const [applicantName, setApplicantName] = useState<string>('');
  const [applicantEmail, setApplicantEmail] = useState<string>('');
  const [applicantPhone, setApplicantPhone] = useState<string>('');
  const [institution, setInstitution] = useState<string>('');
  const [annualIncome, setAnnualIncome] = useState<string>('350000');
  const [notes, setNotes] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const categories = [
    {
      id: 'scholarship',
      title: 'Scholarship & Fee Waiver',
      desc: 'AICTE Pragati, Saksham, Merit-cum-Means & State Scholarships',
      icon: <GraduationCap className="w-6 h-6 text-teal-600" />,
      docs: ['Identity Document (Aadhaar)', 'Academic Degree/Transcript', 'Income Certificate'],
    },
    {
      id: 'admissions',
      title: 'University / Institute Admissions',
      desc: 'Undergraduate, Postgraduate, and Lateral Entry verification',
      icon: <Building className="w-6 h-6 text-cyan-600" />,
      docs: ['Identity Document', '10+2 / Diploma Mark Sheet', 'Migration / Transfer Certificate'],
    },
    {
      id: 'recruitment',
      title: 'Faculty & Technical Recruitment',
      desc: 'Academic appointment credential verification and background check',
      icon: <Briefcase className="w-6 h-6 text-indigo-600" />,
      docs: ['Identity Document', 'Doctoral / Master Degree', 'Experience Certificate'],
    },
    {
      id: 'regulatory_licensing',
      title: 'Regulatory & Professional Licensing',
      desc: 'Accreditation, statutory council permits, and trade certificates',
      icon: <FileBadge className="w-6 h-6 text-amber-600" />,
      docs: ['Registration Certificate', 'Statutory Declaration', 'Identity Proof'],
    },
  ];

  const handleCreate = async () => {
    setIsSubmitting(true);
    setError(null);
    try {
      const payload = {
        applicant_name: applicantName.trim(),
        applicant_email: applicantEmail.trim(),
        applicant_phone: applicantPhone.trim() || undefined,
        category,
        organization_or_institution: institution.trim() || undefined,
        declared_details: {
          applicant_name: applicantName.trim(),
          annual_income: annualIncome ? `₹${Number(annualIncome).toLocaleString()}` : undefined,
          institution: institution.trim(),
        },
        notes: notes.trim() || undefined,
      };

      const res = await apiRequest<Application>('/api/applications', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      // Redirect immediately to upload documents for this new application
      navigate(`/applications/${res.id || (res as any)._id}/upload`);
    } catch (err: any) {
      setError(err.message || 'Failed to create application');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 font-sans">
      <div>
        <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
          New Application Intake Scrutiny Wizard
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Define application category, candidate details, and ingest credentials for AI scrutiny.
        </p>
      </div>

      {/* Steps Indicator */}
      <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-slate-200">
        <div className="flex items-center gap-2">
          <div
            className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
              step >= 1 ? 'bg-teal-600 text-white' : 'bg-slate-100 text-slate-400'
            }`}
          >
            1
          </div>
          <span className="text-xs font-semibold text-slate-700">Category Selection</span>
        </div>
        <div className="w-12 h-0.5 bg-slate-200" />
        <div className="flex items-center gap-2">
          <div
            className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
              step >= 2 ? 'bg-teal-600 text-white' : 'bg-slate-100 text-slate-400'
            }`}
          >
            2
          </div>
          <span className="text-xs font-semibold text-slate-700">Applicant Profile</span>
        </div>
        <div className="w-12 h-0.5 bg-slate-200" />
        <div className="flex items-center gap-2">
          <div
            className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
              step >= 3 ? 'bg-teal-600 text-white' : 'bg-slate-100 text-slate-400'
            }`}
          >
            3
          </div>
          <span className="text-xs font-semibold text-slate-700">Confirm & Upload</span>
        </div>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Step 1: Category */}
      {step === 1 && (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 space-y-4">
          <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider">
            Step 1: Choose Application Framework
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {categories.map((c) => (
              <div
                key={c.id}
                onClick={() => setCategory(c.id as ApplicationCategory)}
                className={`p-4 rounded-xl border text-xs cursor-pointer transition-all ${
                  category === c.id
                    ? 'border-teal-500 bg-teal-50/70 shadow-sm ring-2 ring-teal-500/20'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <div className="p-2 rounded-lg bg-slate-50 w-fit mb-2">{c.icon}</div>
                <h3 className="font-bold text-navy-950 text-sm">{c.title}</h3>
                <p className="text-slate-500 text-[11px] mt-1">{c.desc}</p>
                <div className="mt-3 pt-2 border-t border-slate-100 text-[10px] text-teal-700 font-semibold">
                  Required: {c.docs.join(' • ')}
                </div>
              </div>
            ))}
          </div>

          <div className="pt-4 flex justify-end">
            <button
              onClick={() => setStep(2)}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-navy-950 hover:bg-navy-900 text-white flex items-center gap-1.5 transition-all"
            >
              <span>Continue to Profile</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Applicant Profile */}
      {step === 2 && (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 space-y-4">
          <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider">
            Step 2: Enter Applicant Credentials
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Applicant Full Name <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                required
                value={applicantName}
                onChange={(e) => setApplicantName(e.target.value)}
                placeholder="e.g. Aarav Sharma"
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Email Address <span className="text-rose-500">*</span>
              </label>
              <input
                type="email"
                required
                value={applicantEmail}
                onChange={(e) => setApplicantEmail(e.target.value)}
                placeholder="aarav.sharma@example.edu"
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
              <input
                type="text"
                value={applicantPhone}
                onChange={(e) => setApplicantPhone(e.target.value)}
                placeholder="+91 98765 43210"
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Institution / University
              </label>
              <input
                type="text"
                value={institution}
                onChange={(e) => setInstitution(e.target.value)}
                placeholder="e.g. Delhi Technological University"
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900"
              />
            </div>

            {category === 'scholarship' && (
              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Declared Annual Family Income (INR)
                </label>
                <input
                  type="number"
                  value={annualIncome}
                  onChange={(e) => setAnnualIncome(e.target.value)}
                  placeholder="350000"
                  className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900 font-mono"
                />
                <p className="text-[10px] text-slate-400 mt-1">
                  AICTE Pragati/Saksham income ceiling is ₹8,00,000 per annum.
                </p>
              </div>
            )}
          </div>

          <div className="pt-4 flex items-center justify-between border-t border-slate-100">
            <button
              onClick={() => setStep(1)}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
            >
              &larr; Back
            </button>
            <button
              onClick={() => {
                if (!applicantName || !applicantEmail) {
                  setError('Please fill in Applicant Name and Email Address');
                  return;
                }
                setError(null);
                setStep(3);
              }}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-navy-950 hover:bg-navy-900 text-white flex items-center gap-1.5 transition-all"
            >
              <span>Next: Review & Ingest</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Confirmation */}
      {step === 3 && (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 space-y-4">
          <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider">
            Step 3: Review Application Summary
          </h2>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2 text-xs">
            <div className="flex justify-between py-1 border-b border-slate-200">
              <span className="text-slate-500">Category:</span>
              <span className="font-bold text-navy-950 capitalize">{category.replace('_', ' ')}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-200">
              <span className="text-slate-500">Applicant:</span>
              <span className="font-bold text-navy-950">{applicantName}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-200">
              <span className="text-slate-500">Email:</span>
              <span className="font-mono text-slate-700">{applicantEmail}</span>
            </div>
            {institution && (
              <div className="flex justify-between py-1 border-b border-slate-200">
                <span className="text-slate-500">Institution:</span>
                <span className="text-slate-700">{institution}</span>
              </div>
            )}
            {category === 'scholarship' && (
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Declared Income:</span>
                <span className="font-bold font-mono text-teal-800">₹{Number(annualIncome).toLocaleString()}</span>
              </div>
            )}
          </div>

          <div className="p-3.5 bg-teal-50 rounded-xl border border-teal-200 text-xs text-teal-800 space-y-1">
            <p className="font-bold flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-teal-600" />
              Automated Document Upload Pipeline Ready
            </p>
            <p className="text-[11px] text-teal-700">
              Upon submission, a unique Application Reference ID will be issued and you will proceed to the drag-and-drop document intake page.
            </p>
          </div>

          <div className="pt-4 flex items-center justify-between border-t border-slate-100">
            <button
              onClick={() => setStep(2)}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
            >
              &larr; Back
            </button>
            <button
              onClick={handleCreate}
              disabled={isSubmitting}
              className="px-6 py-2.5 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-600/20 flex items-center gap-1.5 disabled:opacity-50"
            >
              {isSubmitting ? 'Creating Application...' : 'Create Intake & Proceed to Upload'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
