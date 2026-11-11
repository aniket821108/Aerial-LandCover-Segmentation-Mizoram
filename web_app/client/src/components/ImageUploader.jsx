import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, Sparkles, AlertCircle, FileText, CheckCircle } from 'lucide-react';

export default function ImageUploader({
  onAnalyze,
  onSampleSelect,
  isAnalyzing = false,
  currentStep = '',
  sampleLoadingId = null
}) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [gsd, setGsd] = useState(0.3);
  const inputRef = useRef(null);

  const sampleScenes = [
    {
      id: '2522',
      name: 'Farmland & Terraces (Scene 2522)',
      tag: 'Agriculture 71%',
      color: 'border-orange-500/40 text-orange-300 bg-orange-950/20 hover:bg-orange-900/30',
      icon: '🌾'
    },
    {
      id: '2532',
      name: 'Mountain Forest Canopy (Scene 2532)',
      tag: 'Forest 68%',
      color: 'border-emerald-500/40 text-emerald-300 bg-emerald-950/20 hover:bg-emerald-900/30',
      icon: '🌲'
    },
    {
      id: '2544',
      name: 'River Basin Settlement (Scene 2544)',
      tag: 'Water & Riparian',
      color: 'border-blue-500/40 text-blue-300 bg-blue-950/20 hover:bg-blue-900/30',
      icon: '🌊'
    }
  ];

  const handleFile = (file) => {
    if (!file) return;
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    onAnalyze(selectedFile, gsd);
  };

  // Test Guardrail Rejection with simulated non-aerial image
  const handleTestNegative = () => {
    // Create a dummy image with text "Indoor Cat Portrait"
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#4a2c2c';
    ctx.fillRect(0, 0, 512, 512);
    ctx.fillStyle = '#ffffff';
    ctx.font = '24px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('🐱 Indoor Cat Pet Portrait', 256, 230);
    ctx.font = '16px sans-serif';
    ctx.fillText('Non-Aerial Test Case for Gemini Guardrail', 256, 270);
    
    canvas.toBlob((blob) => {
      const file = new File([blob], 'test_indoor_cat_portrait.png', { type: 'image/png' });
      handleFile(file);
    }, 'image/png');
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-2xl backdrop-blur-md space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
        <div>
          <h2 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            <UploadCloud className="w-5 h-5 text-cyan-400" />
            Upload Aerial / Satellite Orthophoto
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Orthogonal RGB orthophoto (.png, .jpg, .tif) • Evaluated by Gemini 1.5 Guardrail
          </p>
        </div>

        {/* 1-Click Samples Toolbar */}
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="text-xs text-slate-400 font-medium mr-1">Quick Samples:</span>
          {sampleScenes.map((s) => (
            <button
              key={s.id}
              disabled={isAnalyzing || Boolean(sampleLoadingId)}
              onClick={() => onSampleSelect(s.id)}
              className={`px-2.5 py-1 text-xs rounded-lg border font-medium transition-all flex items-center gap-1.5 disabled:opacity-50 ${s.color}`}
            >
              {sampleLoadingId === s.id ? (
                <div className="w-3.5 h-3.5 border-2 border-current border-t-transparent rounded-full animate-spin" />
              ) : (
                <span>{s.icon}</span>
              )}
              <span>{s.name.split(' ')[0]}</span>
              <span className="text-[10px] opacity-80">({s.tag})</span>
            </button>
          ))}
          <button
            onClick={handleTestNegative}
            disabled={isAnalyzing || Boolean(sampleLoadingId)}
            title="Demonstrate Gemini Guardrail rejecting non-aerial input"
            className="px-2.5 py-1 text-xs rounded-lg border border-red-500/40 text-red-300 bg-red-950/20 hover:bg-red-900/30 transition flex items-center gap-1 disabled:opacity-50"
          >
            <span>🚫</span>
            <span>Test Non-Aerial</span>
          </button>
        </div>
      </div>

      {/* Drag & Drop Area */}
      <form onSubmit={handleSubmit} onDragEnter={handleDrag} className="space-y-4">
        <input
          ref={inputRef}
          type="file"
          accept="image/png, image/jpeg, image/jpg, image/tiff"
          onChange={(e) => handleFile(e.target.files[0])}
          className="hidden"
        />

        <div
          onClick={() => inputRef.current?.click()}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          className={`relative border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center min-h-[160px] ${
            dragActive
              ? 'border-cyan-400 bg-cyan-950/30 scale-[1.01]'
              : 'border-slate-700/80 hover:border-slate-500 bg-slate-950/40 hover:bg-slate-950/60'
          }`}
        >
          {previewUrl ? (
            <div className="flex items-center gap-4 text-left w-full max-w-md bg-slate-900/90 p-3 rounded-xl border border-slate-700 relative">
              <img
                src={previewUrl}
                alt="Upload preview"
                className="w-16 h-16 rounded-lg object-cover border border-slate-700 shrink-0"
              />
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium text-slate-100 truncate">
                  {selectedFile?.name || 'Selected Aerial Image'}
                </p>
                <p className="text-xs text-slate-400 mt-0.5">
                  {(selectedFile?.size ? (selectedFile.size / (1024 * 1024)).toFixed(2) + ' MB' : 'Ready')} • Click to change file
                </p>
              </div>
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedFile(null);
                  setPreviewUrl(null);
                }}
                className="p-1 rounded-lg text-slate-400 hover:text-red-400 hover:bg-slate-800 transition"
                title="Remove selected file"
              >
                ✕
              </button>
            </div>
          ) : (
            <>
              <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center mb-3 text-cyan-400 shadow-inner">
                <ImageIcon className="w-6 h-6" />
              </div>
              <p className="text-sm font-medium text-slate-200">
                Click to browse or drop an aerial survey orthophoto here
              </p>
              <p className="text-xs text-slate-500 mt-1">
                Supports RGB PNG, JPG, or GeoTIFF (LoveDA standard: 1024x1024)
              </p>
            </>
          )}
        </div>

        {/* Spatial Settings & Submit */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-1">
          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-400 font-medium">Ground Sampling Distance (GSD):</label>
            <input
              type="number"
              step="0.05"
              min="0.1"
              max="5.0"
              value={gsd}
              onChange={(e) => setGsd(parseFloat(e.target.value) || 0.3)}
              className="w-20 px-2 py-1 rounded bg-slate-800 border border-slate-700 text-xs font-mono text-cyan-300 text-center"
            />
            <span className="text-xs text-slate-500">m / pixel</span>
          </div>

          <button
            type="submit"
            disabled={!selectedFile || isAnalyzing || Boolean(sampleLoadingId)}
            className={`px-6 py-2.5 rounded-xl font-medium text-sm transition-all flex items-center gap-2 shadow-lg ${
              !selectedFile || isAnalyzing || Boolean(sampleLoadingId)
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white shadow-cyan-500/25 active:scale-95'
            }`}
          >
            {isAnalyzing ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>{currentStep || 'Analyzing Scene...'}</span>
              </>
            ) : sampleLoadingId ? (
              <>
                <div className="w-4 h-4 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
                <span>Loading Benchmark Sample...</span>
              </>
            ) : !selectedFile ? (
              <>
                <UploadCloud className="w-4 h-4 text-slate-500" />
                <span>Select Image to Segment</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Verify & Segment Scene</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}

