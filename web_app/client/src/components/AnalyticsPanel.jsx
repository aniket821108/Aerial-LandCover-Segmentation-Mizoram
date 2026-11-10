import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { PieChart as PieIcon, BarChart3, MapPin, Download, CheckCircle2 } from 'lucide-react';

export default function AnalyticsPanel({ metrics, filename = 'survey_report' }) {
  if (!metrics || !metrics.classes) return null;

  const totalHa = metrics.total_hectares || 0;
  const totalM2 = metrics.total_area_m2 || 0;
  const totalAcres = (totalHa * 2.47105).toFixed(2);
  const dominantClass = metrics.dominant_class || 'Agriculture';

  // Filter out classes with 0% to keep charts clean, or keep all
  const chartData = metrics.classes
    .filter((c) => c.percentage > 0.1)
    .map((c) => ({
      name: c.name.charAt(0).toUpperCase() + c.name.slice(1),
      hectares: c.area_ha,
      percentage: c.percentage,
      color: c.color,
      m2: c.area_m2,
      pixels: c.pixels,
    }));

  const handleExportJSON = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(metrics, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `${filename}_gdal_metrics.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded-xl shadow-xl text-xs">
          <div className="flex items-center gap-2 mb-1.5 font-semibold text-slate-100">
            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: data.color }} />
            <span>{data.name}</span>
          </div>
          <div className="text-slate-300 space-y-0.5">
            <div>Share: <span className="font-mono text-cyan-400 font-bold">{data.percentage}%</span></div>
            <div>Area: <span className="font-mono text-slate-100">{data.hectares} Ha</span> ({data.m2.toLocaleString()} m²)</div>
            <div>Pixels: <span className="font-mono text-slate-400">{data.pixels.toLocaleString()}</span></div>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* Top 3 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Total Area */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg backdrop-blur-sm relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-cyan-500/10 rounded-full blur-xl group-hover:bg-cyan-500/20 transition-all" />
          <div className="flex items-center justify-between text-slate-400 text-xs uppercase tracking-wider font-semibold mb-1">
            <span>Total Mapped Area</span>
            <MapPin className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white font-mono flex items-baseline gap-1.5">
            {totalHa.toFixed(2)}
            <span className="text-sm font-normal text-slate-400">Hectares</span>
          </div>
          <div className="text-xs text-slate-400 mt-1">
            ≈ {totalAcres} Acres • {totalM2.toLocaleString()} m²
          </div>
        </div>

        {/* Dominant Class */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg backdrop-blur-sm relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-xl group-hover:bg-emerald-500/20 transition-all" />
          <div className="flex items-center justify-between text-slate-400 text-xs uppercase tracking-wider font-semibold mb-1">
            <span>Dominant Land Cover</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 font-mono capitalize">
            {dominantClass}
          </div>
          <div className="text-xs text-slate-400 mt-1">
            Primary canopy / surface feature
          </div>
        </div>

        {/* Spatial Resolution */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg backdrop-blur-sm relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-purple-500/10 rounded-full blur-xl group-hover:bg-purple-500/20 transition-all" />
          <div className="flex items-center justify-between text-slate-400 text-xs uppercase tracking-wider font-semibold mb-1">
            <span>Spatial Resolution</span>
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-900/50 text-purple-300 font-mono">GDAL</span>
          </div>
          <div className="text-2xl font-bold text-purple-300 font-mono">
            {metrics.gsd || 0.3} m
            <span className="text-sm font-normal text-slate-400 ml-1">/ pixel</span>
          </div>
          <div className="text-xs text-slate-400 mt-1">
            1 pixel = 0.09 m² ground footprint
          </div>
        </div>
      </div>

      {/* Visual Charts: Donut + Bar Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Donut Chart */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <PieIcon className="w-4 h-4 text-cyan-400" />
              Land-Use Distribution (% Share)
            </h3>
            <span className="text-xs text-slate-400 font-mono">LoveDA 7-Class</span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={3}
                  dataKey="percentage"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar Chart: Hectares */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-emerald-400" />
              Physical Area by Class (Hectares)
            </h3>
            <span className="text-xs text-slate-400 font-mono">Calibrated Ha</span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 25 }}>
                <XAxis
                  dataKey="name"
                  stroke="#64748b"
                  fontSize={11}
                  angle={-25}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="hectares" radius={[4, 4, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`bar-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Quantitative Area Table */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl backdrop-blur-sm">
        <div className="px-5 py-3.5 bg-slate-800/60 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            GDAL Sub-Meter Land-Cover Breakdown
          </h3>
          <button
            onClick={handleExportJSON}
            className="px-3 py-1 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5 text-cyan-400" />
            Export Report (JSON)
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/60 text-slate-400 uppercase tracking-wider text-[11px] border-b border-slate-800">
              <tr>
                <th className="py-2.5 px-4">Class</th>
                <th className="py-2.5 px-4 text-right">Pixels</th>
                <th className="py-2.5 px-4 text-right">Area (m²)</th>
                <th className="py-2.5 px-4 text-right">Area (Ha)</th>
                <th className="py-2.5 px-4 text-right">Share (%)</th>
                <th className="py-2.5 px-4">Visual Distribution</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {metrics.classes.map((c) => (
                <tr key={c.class_id} className="hover:bg-slate-800/40 transition">
                  <td className="py-2.5 px-4 font-medium flex items-center gap-2 text-slate-100">
                    <span className="w-3 h-3 rounded shadow-sm" style={{ backgroundColor: c.color }} />
                    <span className="capitalize">{c.name}</span>
                  </td>
                  <td className="py-2.5 px-4 text-right font-mono text-slate-400">
                    {c.pixels.toLocaleString()}
                  </td>
                  <td className="py-2.5 px-4 text-right font-mono text-slate-300">
                    {c.area_m2.toLocaleString()}
                  </td>
                  <td className="py-2.5 px-4 text-right font-mono font-bold text-white">
                    {c.area_ha.toFixed(3)}
                  </td>
                  <td className="py-2.5 px-4 text-right font-mono text-cyan-400 font-bold">
                    {c.percentage.toFixed(1)}%
                  </td>
                  <td className="py-2.5 px-4 w-40">
                    <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{ width: `${Math.min(c.percentage, 100)}%`, backgroundColor: c.color }}
                      />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

