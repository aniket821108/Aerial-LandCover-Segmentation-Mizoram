import React from 'react';

export const CLASSES_INFO = [
  { id: 1, name: 'Building', color: '#ef4444', desc: 'Rooftops, rural settlements, houses' },
  { id: 2, name: 'Road', color: '#eab308', desc: 'Paved highways, dirt tracks, transport corridors' },
  { id: 3, name: 'Water', color: '#3b82f6', desc: 'Rivers, streams, reservoirs, water bodies' },
  { id: 4, name: 'Barren', color: '#a855f7', desc: 'Exposed soil, rock outcrops, uncultivated land' },
  { id: 5, name: 'Forest', color: '#22c55e', desc: 'Dense tree canopy, subtropical forest cover' },
  { id: 6, name: 'Agriculture', color: '#f97316', desc: 'Terraced crop fields, cultivated farmland' },
];

export default function Legend() {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 backdrop-blur-sm">
      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
        LoveDA Land-Cover Legend (Mizoram)
      </h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
        {CLASSES_INFO.map((cls) => (
          <div
            key={cls.id}
            className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/50"
          >
            <span
              className="w-3.5 h-3.5 rounded shadow-sm shrink-0"
              style={{ backgroundColor: cls.color }}
            />
            <div className="min-w-0">
              <span className="text-xs font-medium text-slate-200 block truncate">{cls.name}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
