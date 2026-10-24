import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { Application, DocumentType } from '../types';
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  ShieldCheck,
  Cpu,
  Trash2,
} from 'lucide-react';

export const DocumentUploadPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [app, setApp] = useState<Application | null>(null);
  const [docType, setDocType] = useState<DocumentType>('identity_document');
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [uploadedDocs, setUploadedDocs] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadApp() {
      if (!id) return;
      try {
        const data = await apiRequest<Application>(`/api/applications/${id}`);
        setApp(data);
        if (data.documents) {
          setUploadedDocs(data.documents);
        }
      } catch (err) {
        console.error('Failed to load application:', err);
      }
    }
    loadApp();
  }, [id]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !id) return;

    setIsUploading(true);
    setUploadProgress(20);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', docType);

    try {
      setUploadProgress(60);
      const res = await apiRequest(`/api/applications/${id}/documents`, {
        method: 'POST',
        body: formData,
      });
      setUploadProgress(100);
      setUploadedDocs((prev) => [...prev, res]);
      setFile(null);
    } catch (err: any) {
      setError(err.message || 'File upload and analysis failed');
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const handleTriggerVerification = async () => {
    if (!id) return;
    try {
      await apiRequest(`/api/applications/${id}/verify`, { method: 'POST' });
      navigate(`/applications/${id}/review`);
    } catch (err: any) {
      setError(err.message || 'Verification execution failed');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-navy-950 font-['Plus_Jakarta_Sans']">
            Document Ingestion & Automated Verification
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Application: <span className="font-mono font-semibold text-teal-800">{app?.reference_id}</span> •{' '}
            Candidate: <span className="font-semibold text-slate-800">{app?.applicant_name}</span>
          </p>
        </div>

        {uploadedDocs.length > 0 && (
          <button
            onClick={handleTriggerVerification}
            className="px-5 py-2.5 rounded-xl text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-600/20 flex items-center gap-1.5 transition-all"
          >
            <Cpu className="w-4 h-4" />
            <span>Execute Full Verification Pipeline &rarr;</span>
          </button>
        )}
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Upload Box */}
      <form onSubmit={handleUploadSubmit} className="bg-white p-6 rounded-2xl border border-slate-200 space-y-5">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Select Document Classification Type <span className="text-rose-500">*</span>
            </label>
            <select
              value={docType}
              onChange={(e) => setDocType(e.target.value as DocumentType)}
              className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-900 font-medium"
            >
              <option value="identity_document">Identity Document (Aadhaar / Passport / PAN)</option>
              <option value="academic_certificate">Academic Degree / Diploma Certificate</option>
              <option value="marksheet_transcript">Marks Sheet / Semester Transcript</option>
              <option value="income_certificate">Annual Family Income Certificate</option>
              <option value="address_proof">Proof of Residence / Domicile</option>
              <option value="registration_certificate">Professional / Statutory Registration</option>
              <option value="other">Other Official Record</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Permitted File Formats
            </label>
            <p className="text-xs text-slate-500 py-2">
              PDF, PNG, JPEG, WebP • Max 25MB • Up to 30 Pages
            </p>
          </div>
        </div>

        {/* Drag and Drop Zone */}
        <div
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-colors ${
            file
              ? 'border-teal-500 bg-teal-50/50'
              : 'border-slate-300 hover:border-teal-500 hover:bg-slate-50/50'
          }`}
        >
          <input
            type="file"
            id="file-upload"
            onChange={handleFileChange}
            accept=".pdf,.png,.jpg,.jpeg,.webp"
            className="hidden"
          />
          <label htmlFor="file-upload" className="cursor-pointer space-y-2 block">
            <UploadCloud className="w-10 h-10 text-teal-600 mx-auto" />
            <p className="text-xs font-bold text-navy-950">
              {file ? file.name : 'Click to select or drag and drop document file here'}
            </p>
            <p className="text-[11px] text-slate-400">
              {file ? `${(file.size / (1024 * 1024)).toFixed(2)} MB • Ready for ingestion` : 'Files are validated on byte headers'}
            </p>
          </label>
        </div>

        {isUploading && (
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-semibold text-teal-800">
              <span>Running OCR & Forensic Inspection...</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
              <div
                className="bg-teal-600 h-2 transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={!file || isUploading}
            className="px-6 py-2.5 rounded-xl text-xs font-bold bg-navy-950 hover:bg-navy-900 text-white shadow-md disabled:opacity-50 transition-all"
          >
            {isUploading ? 'Ingesting...' : 'Upload & Analyze Document'}
          </button>
        </div>
      </form>

      {/* Uploaded Documents List */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 space-y-4">
        <h2 className="text-sm font-bold text-navy-950 uppercase tracking-wider flex items-center justify-between">
          <span>Ingested Documents ({uploadedDocs.length})</span>
          <span className="text-xs text-slate-400 font-normal">Stored with SHA-256 integrity</span>
        </h2>

        {uploadedDocs.length === 0 ? (
          <div className="p-8 text-center text-slate-400 text-xs">
            No documents uploaded yet. Use the upload box above.
          </div>
        ) : (
          <div className="space-y-3">
            {uploadedDocs.map((doc: any) => (
              <div
                key={doc._id || doc.id}
                className="p-4 rounded-xl border border-slate-200 flex flex-wrap items-center justify-between gap-3 hover:bg-slate-50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-100">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-navy-950 font-mono">
                      {doc.metadata?.original_filename || 'document.pdf'}
                    </h3>
                    <p className="text-[10px] text-slate-400">
                      Type: <span className="capitalize font-medium text-slate-600">{doc.document_type?.replace(/_/g, ' ')}</span> •{' '}
                      Pages: {doc.metadata?.page_count || 1} • SHA-256: {doc.metadata?.sha256_hash?.slice(0, 12)}...
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => navigate(`/applications/${id}/review`)}
                    className="px-3 py-1.5 rounded-lg bg-teal-50 text-teal-700 hover:bg-teal-100 font-semibold text-xs transition-colors"
                  >
                    View in Workbench
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
