import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ImageUploader from './components/ImageUploader';
import GuardrailBadge from './components/GuardrailBadge';
import ComparisonViewer from './components/ComparisonViewer';
import AnalyticsPanel from './components/AnalyticsPanel';
import Legend from './components/Legend';
import HistoryDrawer from './components/HistoryDrawer';

export default function App() {
  const [activeScan, setActiveScan] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState('');
  const [isRejected, setIsRejected] = useState(false);
  const [rejectedGuardrail, setRejectedGuardrail] = useState(null);
  const [history, setHistory] = useState([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [serverStatus, setServerStatus] = useState(null);

  // Initial Load: Fetch status, history & load default scene 2522
  useEffect(() => {
    fetchHealth();
    fetchHistory();
    // Pre-load Scene 2522 by default
    handleSampleSelect('2522');
  }, []);

  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setServerStatus(data);
      }
    } catch (err) {
      console.warn('API health check failed:', err);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch('/api/history');
      if (res.ok) {
        const data = await res.json();
        if (data.history) setHistory(data.history);
      }
    } catch (err) {
      console.warn('Failed to fetch history:', err);
    }
  };

  // Upload & Process Custom Image
  const handleAnalyze = async (file, gsd = 0.3) => {
    setIsProcessing(true);
    setIsRejected(false);
    setRejectedGuardrail(null);
    setCurrentStep('Tier 1: Gemini Vision AI Domain Guardrail...');

    const formData = new FormData();
    formData.append('image', file);
    formData.append('gsd', gsd.toString());

    try {
      const res = await fetch('/api/scan', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      if (res.status === 422 || !data.success) {
        // Rejected by Tier 1 Gemini Guardrail
        setIsRejected(true);
        setRejectedGuardrail(data.guardrail);
        setIsProcessing(false);
        return;
      }

      // Successful segmentation
      setActiveScan({
        filename: file.name,
        originalUrl: data.original_url || URL.createObjectURL(file),
        maskUrl: data.mask_base64 || data.mask_url,
        overlayUrl: data.overlay_base64 || data.overlay_url,
        guardrail: data.guardrail,
        metrics: data.metrics,
      });

      fetchHistory();
    } catch (err) {
      console.error('Scan failed:', err);
      alert('Analysis error: ' + err.message);
    } finally {
      setIsProcessing(false);
      setCurrentStep('');
    }
  };

  // 1-Click Load for Sample Scenes
  const handleSampleSelect = async (sampleId) => {
    setIsProcessing(true);
    setIsRejected(false);
    setRejectedGuardrail(null);
    setCurrentStep(`Loading Scene ${sampleId} & Running CBST Segmentation...`);

    try {
      const res = await fetch(`/api/scan-sample/${sampleId}`, { method: 'POST' });
      const data = await res.json();

      if (data.success) {
        setActiveScan({
          filename: `Rural_Mizoram_Scene_${sampleId}.png`,
          originalUrl: data.original_url,
          maskUrl: data.mask_base64 || data.mask_url,
          overlayUrl: data.overlay_base64 || data.overlay_url,
          guardrail: data.guardrail,
          metrics: data.metrics,
        });
        fetchHistory();
      }
    } catch (err) {
      console.error('Sample scan error:', err);
    } finally {
      setIsProcessing(false);
      setCurrentStep('');
    }
  };

  // Select from History Drawer
  const handleSelectRecord = (record) => {
    setIsRejected(false);
    setRejectedGuardrail(null);
    setActiveScan({
      filename: record.originalFilename,
      originalUrl: record.originalUrl,
      maskUrl: record.maskBase64 || record.maskUrl,
      overlayUrl: record.overlayBase64 || record.overlayUrl,
      guardrail: record.geminiAnalysis,
      metrics: record.metrics,
    });
  };

  // Delete from History
  const handleDeleteRecord = async (id) => {
    try {
      await fetch(`/api/history/${id}`, { method: 'DELETE' });
      setHistory((prev) => prev.filter((item) => item._id !== id));
    } catch (err) {
      console.error('Failed to delete record:', err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navbar */}
      <Navbar
        onOpenHistory={() => setIsHistoryOpen(true)}
        historyCount={history.length}
        serverStatus={serverStatus}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full space-y-8">
        {/* Project Header Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 rounded-3xl p-6 sm:p-8 relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold mb-3">
              <span>🚀 Sem 7 Capstone Project • BT23CS028</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
              Aerial Image Land-Use Segmentation & Geospatial Analytics
            </h1>
            <p className="text-sm sm:text-base text-slate-300 mt-2.5 leading-relaxed">
              Two-tier architecture: Multimodal <strong>Gemini 1.5 Vision AI</strong> verifies overhead validity, followed by <strong>DeepLabV3+ ResNet-50 CBST</strong> domain-adapted semantic segmentation and sub-meter <strong>GDAL</strong> hectare quantification.
            </p>
          </div>
        </div>

        {/* Section 1: Image Uploader & Sample Selector */}
        <ImageUploader
          onAnalyze={handleAnalyze}
          onSampleSelect={handleSampleSelect}
          isProcessing={isProcessing}
          currentStep={currentStep}
        />

        {/* Section 2: Guardrail Status Feedback (If Rejected or Verified) */}
        {isRejected && (
          <GuardrailBadge
            guardrail={rejectedGuardrail}
            isRejected={true}
          />
        )}

        {/* Section 3: Verified Analysis Results */}
        {activeScan && !isRejected && (
          <div className="space-y-8 animate-fadeIn">
            {/* Tier 1 Guardrail Verification Badge */}
            <GuardrailBadge
              guardrail={activeScan.guardrail}
              isRejected={false}
            />

            {/* Official 7-Class Color Legend */}
            <Legend />

            {/* Split Comparison Viewer & Overlay */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
                  Visual Segmentation Explorer
                </h2>
                <span className="text-xs text-slate-400 font-mono">
                  {activeScan.filename}
                </span>
              </div>

              <ComparisonViewer
                originalSrc={activeScan.originalUrl}
                maskSrc={activeScan.maskUrl}
                overlaySrc={activeScan.overlayUrl}
                filename={activeScan.filename.replace(/\.[^/.]+$/, '')}
              />
            </div>

            {/* Quantitative Hectare Area Analytics (Donut + Bar Charts + Table) */}
            <div className="space-y-3 pt-4">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                Geospatial Land-Cover Area Quantification
              </h2>
              <AnalyticsPanel
                metrics={activeScan.metrics}
                filename={activeScan.filename.replace(/\.[^/.]+$/, '')}
              />
            </div>
          </div>
        )}
      </main>

      {/* History Drawer */}
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        onSelectRecord={handleSelectRecord}
        onDeleteRecord={handleDeleteRecord}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 py-6 mt-12 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4">
          Aerial Image Segmentation for Land-Use Classification (LoveDA Urban $\rightarrow$ Rural CBST Domain Adaptation)
          <div className="mt-1 text-slate-600">
            MERN Stack + Python Microservice • GDAL Real-World Hectare Analytics • Gemini 1.5 Vision Gate
          </div>
        </div>
      </footer>
    </div>
  );
}
