# AeroSeg AI • Aerial Land-Cover Segmentation & Geospatial Analytics Platform

An end-to-end full-stack web application designed for aerial image segmentation and land-use quantification, implementing a **Two-Tier Multimodal AI Pipeline**:

1. **Tier 1 (Domain Guardrail):** Google Gemini 1.5 Flash Vision AI checks whether uploaded images are valid overhead orthogonal aerial/satellite scenes with target land-cover features. Out-of-domain images (e.g., selfies, pets, cars, indoor photos) are caught and gracefully rejected before consuming inference compute.
2. **Tier 2 (Semantic Segmentation & GIS Analytics):** PyTorch DeepLabV3+ (ResNet-50 CBST Urban $\to$ Rural Domain Adapted model) performs sub-meter pixel-level land-cover segmentation. The GDAL engine calculates calibrated physical ground areas in Hectares ($Ha$) and Square Meters ($m^2$) based on Ground Sampling Distance (GSD = 0.3 m/pixel).

---

## Architecture Overview

```mermaid
flowchart TD
    User([User / Urban Planner]) -->|Uploads Image| WebApp[React Dashboard UI (Port 5173)]
    WebApp -->|POST /api/scan| Gateway[Express.js API Gateway (Port 5000)]
    
    subgraph Tier1["Tier 1: Multimodal Gemini Vision AI"]
        Gateway -->|Verify Domain & Classes| Gemini[Gemini 1.5 Flash Vision API]
        Gemini --> Check{"Valid Overhead Aerial Scene?"}
        Check -->|NO: Cat/Selfie/Indoor| Reject[Return 422 Rejection & Explanation]
        Check -->|YES: Valid Aerial Scene| Passed[Extract Domain Context & Proceed]
    end
    
    subgraph Tier2["Tier 2: Python ML Microservice (Port 8000)"]
        Passed --> PyTorch[DeepLabV3+ ResNet-50 CBST]
        PyTorch --> PredMask[7-Class Color Mask]
        PredMask --> Overlay[Alpha-Blended Overlay]
        PredMask --> GDAL[GDAL Hectare Engine (0.3m GSD)]
    end
    
    subgraph Storage["Database & Persistence"]
        Gateway --> MongoDB[(MongoDB Server)]
    end

    Reject --> WebApp
    GDAL --> Gateway
    Overlay --> Gateway
    Gateway --> MongoDB
    Gateway --> WebApp
```

---

## Tech Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | React 19 + Vite + Tailwind CSS | Interactive dashboard, Before/After split slider, Opacity blend, Recharts analytics |
| **Backend Gateway** | Node.js + Express.js + Mongoose | Multipart uploads, Gemini Vision guardrail, API proxy, history persistence |
| **Database** | MongoDB (`localhost:27017`) | Stores scan history, timestamps, class breakdowns, and hectare metrics |
| **ML Microservice** | Python 3 + FastAPI + Uvicorn | PyTorch DeepLabV3+, GDAL surface hectare quantification, GeoTIFF processing |
| **Multimodal AI** | Google Gemini 1.5 Flash | Pre-inference domain validation and natural language terrain synthesis |

---

## Directory Structure

```text
web_app/
├── client/                     # React Frontend (Vite + Tailwind CSS + Recharts)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ComparisonViewer.jsx  # Split Comparison & Opacity slider
│   │   │   ├── AnalyticsPanel.jsx    # Recharts Donut & Bar charts + Hectare table
│   │   │   ├── GuardrailBadge.jsx    # Gemini AI status & terrain description
│   │   │   ├── ImageUploader.jsx     # Drag & drop upload + 1-click sample scenes
│   │   │   ├── Legend.jsx            # LoveDA 7-class color key
│   │   │   ├── Navbar.jsx            # Header & system health indicators
│   │   │   └── HistoryDrawer.jsx     # MongoDB scan history drawer
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
│
├── server/                     # Node.js / Express Backend Gateway
│   ├── models/
│   │   └── ScanRecord.js       # Mongoose Schema for MongoDB persistence
│   ├── routes/
│   │   └── scanRoutes.js       # /api/scan, /api/samples, /api/history
│   ├── services/
│   │   └── geminiGuardrail.js  # Multimodal Gemini Vision AI gatekeeper
│   ├── samples/                # Sample scenes (2522, 2532, 2544)
│   ├── server.js               # Main Express entrypoint (Port 5000)
│   └── .env                    # PORT, MONGO_URI, GEMINI_API_KEY
│
├── ml_service/                 # Python FastAPI ML Microservice
│   ├── service.py              # Segmentation & GDAL hectare quantification (Port 8000)
│   └── requirements.txt
│
├── start_all.bat               # 1-Click launcher for Windows CMD
├── start_all.ps1               # 1-Click launcher for Windows PowerShell
└── README.md
```

---

## Getting Started

### 1. Prerequisites
- **Node.js**: v18+ (tested on v22.20.0)
- **Python**: 3.10+ (tested on Python 3.13)
- **MongoDB**: Running locally on `mongodb://localhost:27017` (app includes graceful fallback if MongoDB is offline)

### 2. Configure Environment Variables
In `server/.env`:
```env
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/aerial_segmentation
ML_SERVICE_URL=http://127.0.0.1:8000
# Optional: Paste your Gemini API key from https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If no Gemini key is provided, the system seamlessly operates in intelligent offline guardrail mode with sample scenarios).*

### 3. Launching the Application
Simply double-click `start_all.bat` or run:
```powershell
./start_all.ps1
```
Or start each service manually:

```powershell
# Terminal 1: Python ML Microservice
cd ml_service
python -m uvicorn service:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Express Backend Gateway
cd server
npm run dev

# Terminal 3: React Frontend Dashboard
cd client
npm run dev
```

Open your browser to: **`http://localhost:5173`**

---

## Interactive Features

1. **Split Comparison Slider:** Drag the center handle left and right to peel away the raw aerial orthophoto and reveal the underlying land-cover mask.
2. **Opacity Slider:** Real-time alpha blending (0% to 100%) to inspect road corridors and building rooftops under the segmentation mask.
3. **1-Click Sample Scenes:** Instantly load and evaluate verified rural Mizoram scenes:
   - 🌾 **Scene 2522:** Farmland & Terraced Agriculture (71.3% Agriculture, 9.44 Ha)
   - 🌲 **Scene 2532:** Mountain Forest Canopy & Ridge (68.2% Forest, 9.44 Ha)
   - 🌊 **Scene 2544:** River Basin & Riparian Settlement (45.1% Water, 9.44 Ha)
4. **Guardrail Demonstration:** Click **"Test Non-Aerial"** to verify that Gemini Vision AI catches non-aerial photos (pets, portraits, indoor scenes) and stops out-of-domain inputs before inference.
5. **GIS Analytics:** View Recharts Donut & Bar charts of real-world coverage in Hectares and $m^2$, and export JSON reports.
6. **MongoDB History:** View and reload past scans with a dedicated history drawer.
