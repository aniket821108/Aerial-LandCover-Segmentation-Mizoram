import React from 'react';
import { ShieldCheck, ShieldAlert, Sparkles, AlertTriangle, Info } from 'lucide-react';

export default function GuardrailBadge({ guardrail, isRejected }) {
  if (!guardrail) return null;

  if (isRejected || !guardrail.proceed_to_segmentation) {
    return (
      <div className="bg-red-950/50 border border-red-500/40 rounded-xl p-5 backdrop-blur-md text-red-200 animate-fadeIn">
        <div className="flex items-start gap-3.5">
          <div className="p-2.5 rounded-lg bg-red-900/60 border border-red-500/50 shrink-0">
            <ShieldAlert className="w-6 h-6 text-red-400" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-red-500/20 text-red-300 border border-red-500/30">
                Tier 1 Guardrail Blocked
              </span>
              <span className="text-xs text-red-300/80">
                Confidence: {Math.round((guardrail.confidence_score || 0.95) * 100)}%
              </span>
            </div>
            <h3 className="text-base font-semibold text-red-100">
              Out-of-Domain Input Detected
            </h3>
            <p className="text-sm text-red-200/90 mt-1.5 leading-relaxed">
              {guardrail.reasoning || guardrail.ai_summary || "The uploaded image does not appear to be an orthogonal aerial or satellite orthophoto. LoveDA DeepLabV3+ is calibrated strictly for overhead earth-observation."}
            </p>
            <div className="mt-3 flex items-center gap-2 text-xs text-red-300/70 bg-red-900/30 p-2 rounded-lg border border-red-800/40">
              <AlertTriangle className="w-4 h-4 shrink-0 text-red-400" />
              <span>Please upload an aerial survey, drone orthomosaic, or satellite raster with land-cover features.</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-xl p-5 backdrop-blur-md text-emerald-200">
      <div className="flex items-start gap-3.5">
        <div className="p-2.5 rounded-lg bg-emerald-900/50 border border-emerald-500/40 shrink-0">
          <ShieldCheck className="w-6 h-6 text-emerald-400" />
        </div>
        <div className="flex-1">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                Tier 1: Gemini Vision Verified
              </span>
              <span className="text-xs text-emerald-300/70">
                Confidence: {Math.round((guardrail.confidence_score || 0.98) * 100)}%
              </span>
            </div>
            <span className="text-xs text-slate-400 font-mono">
              Mode: {guardrail.mode || "Gemini 1.5 Flash"}
            </span>
          </div>

          <h3 className="text-base font-semibold text-emerald-100 mt-1">
            {guardrail.terrain_type || "Verified Rural / Agricultural Aerial Scene"}
          </h3>
          
          <p className="text-sm text-emerald-200/90 mt-1.5 leading-relaxed">
            {guardrail.ai_summary || guardrail.reasoning}
          </p>

          {guardrail.detected_classes && guardrail.detected_classes.length > 0 && (
            <div className="mt-3 flex flex-wrap items-center gap-1.5">
              <span className="text-xs text-emerald-300/80 mr-1 font-medium">Classes Identified by Gemini:</span>
              {guardrail.detected_classes.map((cls, idx) => (
                <span
                  key={idx}
                  className="text-xs px-2 py-0.5 rounded-md bg-emerald-900/60 border border-emerald-700/60 text-emerald-200 font-medium capitalize"
                >
                  {cls}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
