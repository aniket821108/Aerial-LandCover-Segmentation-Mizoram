import mongoose from "mongoose";

const classStatSchema = new mongoose.Schema({
  class_id: { type: Number, required: true },
  name: { type: String, required: true },
  color: { type: String, required: true },
  pixels: { type: Number, required: true },
  area_m2: { type: Number, required: true },
  area_ha: { type: Number, required: true },
  percentage: { type: Number, required: true },
});

const scanRecordSchema = new mongoose.Schema(
  {
    originalFilename: { type: String, required: true },
    originalUrl: { type: String, required: true },
    maskUrl: { type: String, required: true },
    overlayUrl: { type: String, required: true },
    
    // Tier 1: Gemini Guardrail Output
    geminiAnalysis: {
      is_aerial_or_satellite: { type: Boolean, default: true },
      confidence_score: { type: Number, default: 0.95 },
      terrain_type: { type: String, default: "Rural Mountainous Terrain" },
      detected_classes: [{ type: String }],
      reasoning: { type: String },
      ai_summary: { type: String },
      guardrail_passed: { type: Boolean, default: true },
    },

    // Tier 2: GIS & ML Hectare Metrics
    metrics: {
      gsd: { type: Number, default: 0.3 },
      total_pixels: { type: Number },
      total_area_m2: { type: Number },
      total_hectares: { type: Number },
      dominant_class: { type: String },
      classes: [classStatSchema],
    },
  },
  { timestamps: true }
);

export const ScanRecord = mongoose.model("ScanRecord", scanRecordSchema);

