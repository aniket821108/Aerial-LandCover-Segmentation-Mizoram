import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import mongoose from "mongoose";
import path from "path";
import { fileURLToPath } from "url";
import scanRoutes from "./routes/scanRoutes.js";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/aerial_segmentation";

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static Assets
app.use("/uploads", express.static(path.join(__dirname, "uploads")));
app.use("/outputs", express.static(path.join(__dirname, "outputs")));
app.use("/samples", express.static(path.join(__dirname, "samples")));

// Routes
app.use("/api", scanRoutes);

// System Health Endpoint
app.get("/api/health", (req, res) => {
  res.json({
    status: "healthy",
    gateway: "Node.js Express",
    mongo_status: mongoose.connection.readyState === 1 ? "connected" : "disconnected",
    gemini_key_configured: Boolean(process.env.GEMINI_API_KEY && !process.env.GEMINI_API_KEY.includes("AukEuMkbm")),
    timestamp: new Date().toISOString()
  });
});

// Connect to MongoDB
console.log(`[DATABASE] Connecting to MongoDB at: ${MONGO_URI}`);
mongoose
  .connect(MONGO_URI)
  .then(() => console.log("  [OK] Successfully connected to MongoDB."))
  .catch((err) => {
    console.warn("  [WARN] MongoDB connection failed:", err.message);
    console.warn("  [WARN] Running with in-memory persistence fallback.");
  });

app.listen(PORT, () => {
  console.log("=" * 60);
  console.log(`  🛰️ Aerial Land-Use AI Server running on http://localhost:${PORT}`);
  console.log(`  Connected ML Service: ${process.env.ML_SERVICE_URL || "http://127.0.0.1:8000"}`);
  console.log("=" * 60);
});
