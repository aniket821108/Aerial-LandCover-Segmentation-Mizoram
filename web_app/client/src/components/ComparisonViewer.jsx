import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Sliders, Eye, Layers, Split, Download, Maximize2, RefreshCw } from 'lucide-react';

export default function ComparisonViewer({
  originalSrc,
  maskSrc,
  overlaySrc,
  geotiffSrc,
  filename = 'aerial_scene'
}) {
  const [sliderPos, setSliderPos] = useState(50);
  const [viewMode, setViewMode] = useState('split'); // 'split' | 'overlay' | 'side-by-side' | 'mask-only'
  const [opacity, setOpacity] = useState(65);
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef(null);

  // Drag handler for Split Slider
  const handleMove = useCallback((clientX) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    const clamped = Math.max(0, Math.min(100, (x / rect.width) * 100));
    setSliderPos(clamped);
  }, []);

  const handleMouseDown = () => setIsDragging(true);

  useEffect(() => {
    const handleMouseUp = () => setIsDragging(false);
    const handleMouseMove = (e) => {
      if (isDragging) {
        handleMove(e.clientX);
      }
    };
    const handleTouchMove = (e) => {
      if (isDragging && e.touches[0]) {
        handleMove(e.touches[0].clientX);
      }
    };

    window.addEventListener('mouseup', handleMouseUp);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('touchmove', handleTouchMove);
    window.addEventListener('touchend', handleMouseUp);

    return () => {
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('touchmove', handleTouchMove);
      window.removeEventListener('touchend', handleMouseUp);
    };
  }, [isDragging, handleMove]);

  const handleDownload = (src, suffix) => {
    const link = document.createElement('a');
    link.href = src;
    link.download = `${filename}_${suffix}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col">
      {/* Top Toolbar */}
      <div className="px-5 py-3.5 bg-slate-800/80 border-b border-slate-700/60 flex flex-wrap items-center justify-between gap-3">
        {/* Mode Switcher */}
        <div className="flex items-center gap-1.5 bg-slate-950/70 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setViewMode('split')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              viewMode === 'split'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Split className="w-3.5 h-3.5" />
            Split Slider
          </button>

          <button
            onClick={() => setViewMode('overlay')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              viewMode === 'overlay'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            Alpha Overlay
          </button>

          <button
            onClick={() => setViewMode('side-by-side')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              viewMode === 'side-by-side'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            Side-by-Side
          </button>
        </div>

        {/* View Mode Controls */}
        <div className="flex items-center gap-4">
          {viewMode === 'overlay' && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400 font-medium">Mask Opacity:</span>
              <input
                type="range"
                min="0"
                max="100"
                value={opacity}
                onChange={(e) => setOpacity(Number(e.target.value))}
                className="w-28 h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-400"
              />
              <span className="text-xs text-cyan-300 font-mono w-8 text-right">{opacity}%</span>
            </div>
          )}

          {/* Quick Downloads */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleDownload(maskSrc, 'mask')}
              className="px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1.5"
              title="Download Classification Mask (.png)"
            >
              <Download className="w-3.5 h-3.5 text-cyan-400" />
              Mask
            </button>
            <button
              onClick={() => handleDownload(overlaySrc, 'overlay')}
              className="px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1.5"
              title="Download Blended Overlay (.png)"
            >
              <Download className="w-3.5 h-3.5 text-emerald-400" />
              Overlay
            </button>
            {geotiffSrc && (
              <a
                href={geotiffSrc}
                download={`${filename}_segmented.tif`}
                className="px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1.5"
                title="Download Calibrated 8-bit GeoTIFF (.tif) for QGIS/ArcGIS"
              >
                <Download className="w-3.5 h-3.5 text-purple-400" />
                GeoTIFF (.tif)
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Main Visual Stage */}
      <div className="p-4 flex items-center justify-center bg-slate-950/60 min-h-[480px]">
        {/* VIEW MODE 1: Interactive Split Comparison Slider */}
        {viewMode === 'split' && (
          <div
            ref={containerRef}
            className="relative w-full max-w-4xl aspect-[4/3] rounded-xl overflow-hidden shadow-2xl border border-slate-800 select-none cursor-ew-resize group"
            onMouseDown={handleMouseDown}
            onTouchStart={handleMouseDown}
          >
            {/* Background: Raw Original Aerial Image */}
            <img
              src={originalSrc}
              alt="Raw Aerial Photo"
              className="absolute inset-0 w-full h-full object-cover"
              draggable="false"
            />
            <div className="absolute top-3 left-3 px-2.5 py-1 rounded bg-black/70 backdrop-blur-md text-[11px] font-mono tracking-wider text-slate-200 border border-white/10 uppercase">
              Raw Aerial Photo
            </div>

            {/* Foreground: Segmented Mask (Clipped by slider position) */}
            <div
              className="absolute inset-0 overflow-hidden"
              style={{ clipPath: `inset(0 0 0 ${sliderPos}%)` }}
            >
              <img
                src={maskSrc}
                alt="Segmented Mask"
                className="absolute inset-0 w-full h-full object-cover"
                draggable="false"
              />
              <div className="absolute top-3 right-3 px-2.5 py-1 rounded bg-cyan-950/80 backdrop-blur-md text-[11px] font-mono tracking-wider text-cyan-300 border border-cyan-500/30 uppercase">
                DeepLabV3+ Mask
              </div>
            </div>

            {/* Split Handle Divider */}
            <div
              className="absolute top-0 bottom-0 w-0.5 bg-white shadow-[0_0_12px_rgba(255,255,255,0.8)] z-10"
              style={{ left: `${sliderPos}%` }}
            >
              <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-slate-900 border-2 border-white shadow-xl flex items-center justify-center cursor-ew-resize group-hover:scale-110 transition-transform">
                <Sliders className="w-3.5 h-3.5 text-white" />
              </div>
            </div>
          </div>
        )}

        {/* VIEW MODE 2: Alpha-Blended Overlay with Opacity Slider */}
        {viewMode === 'overlay' && (
          <div className="relative w-full max-w-4xl aspect-[4/3] rounded-xl overflow-hidden shadow-2xl border border-slate-800">
            <img
              src={originalSrc}
              alt="Original Aerial"
              className="absolute inset-0 w-full h-full object-cover"
            />
            <img
              src={maskSrc}
              alt="Segmented Mask"
              className="absolute inset-0 w-full h-full object-cover transition-opacity duration-150"
              style={{ opacity: opacity / 100 }}
            />
            <div className="absolute top-3 left-3 px-2.5 py-1 rounded bg-black/70 backdrop-blur-md text-[11px] font-mono tracking-wider text-slate-200 border border-white/10">
              Superimposed Blend ({opacity}%)
            </div>
          </div>
        )}

        {/* VIEW MODE 3: Side-by-Side Comparison */}
        {viewMode === 'side-by-side' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-5xl">
            <div className="relative aspect-[4/3] rounded-xl overflow-hidden border border-slate-800 shadow-xl">
              <img
                src={originalSrc}
                alt="Original Orthophoto"
                className="w-full h-full object-cover"
              />
              <div className="absolute top-3 left-3 px-2.5 py-1 rounded bg-black/70 backdrop-blur-md text-[11px] font-mono tracking-wider text-slate-200 border border-white/10">
                Original Aerial Photo
              </div>
            </div>

            <div className="relative aspect-[4/3] rounded-xl overflow-hidden border border-slate-800 shadow-xl">
              <img
                src={maskSrc}
                alt="Segmented Land Cover"
                className="w-full h-full object-cover"
              />
              <div className="absolute top-3 right-3 px-2.5 py-1 rounded bg-cyan-950/80 backdrop-blur-md text-[11px] font-mono tracking-wider text-cyan-300 border border-cyan-500/30">
                Segmented Land-Cover Mask
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Helper Footer Instruction */}
      <div className="px-5 py-2.5 bg-slate-900 border-t border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
        <span>
          {viewMode === 'split' && '💡 Click and drag the center handle left/right to compare boundaries.'}
          {viewMode === 'overlay' && '💡 Adjust the opacity slider above to see rooftops and road edges through the mask.'}
          {viewMode === 'side-by-side' && '💡 Side-by-side view compares raw spectral channels with calibrated classes.'}
        </span>
        <span className="font-mono text-slate-500">LoveDA ResNet-50 CBST</span>
      </div>
    </div>
  );
}

