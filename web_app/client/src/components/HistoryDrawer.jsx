import React from 'react';
import { X, Clock, Trash2, MapPin, ChevronRight, Database } from 'lucide-react';

export default function HistoryDrawer({ isOpen, onClose, history, onSelectRecord, onDeleteRecord }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Drawer Panel */}
      <div className="relative w-full max-w-md bg-slate-900 border-l border-slate-800 h-full flex flex-col shadow-2xl z-10">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/70">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-cyan-950/60 border border-cyan-500/30 text-cyan-400">
              <Database className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-slate-100">Scan History</h2>
              <p className="text-xs text-slate-400">Persisted in MongoDB</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {history.length === 0 ? (
            <div className="h-64 flex flex-col items-center justify-center text-center p-6 text-slate-500">
              <Clock className="w-8 h-8 mb-2 opacity-50" />
              <p className="text-sm font-medium">No past scans found</p>
              <p className="text-xs mt-1">Uploaded or analyzed aerial scenes will appear here.</p>
            </div>
          ) : (
            history.map((item) => (
              <div
                key={item._id}
                onClick={() => {
                  onSelectRecord(item);
                  onClose();
                }}
                className="group p-3 rounded-xl bg-slate-800/40 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 cursor-pointer transition-all flex items-center gap-3"
              >
                <div className="w-14 h-14 rounded-lg overflow-hidden bg-slate-950 shrink-0 border border-slate-700 relative">
                  <img
                    src={item.maskBase64 || item.maskUrl}
                    alt="Mask thumbnail"
                    className="w-full h-full object-cover"
                  />
                </div>

                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between">
                    <p className="text-xs font-semibold text-slate-200 truncate">
                      {item.originalFilename}
                    </p>
                    <span className="text-[10px] text-slate-500">
                      {new Date(item.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-slate-700 text-slate-300 capitalize">
                      {item.metrics?.dominant_class || 'Agriculture'}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">
                      {item.metrics?.total_hectares ? item.metrics.total_hectares.toFixed(2) + ' Ha' : ''}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-1">
                  {onDeleteRecord && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteRecord(item._id);
                      }}
                      className="p-1 text-slate-500 hover:text-red-400 hover:bg-red-950/40 rounded transition"
                      title="Delete record"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  )}
                  <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-slate-300 transition-transform group-hover:translate-x-0.5" />
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/50 text-xs text-slate-500 text-center">
          Showing latest {history.length} scans from database
        </div>
      </div>
    </div>
  );
}

