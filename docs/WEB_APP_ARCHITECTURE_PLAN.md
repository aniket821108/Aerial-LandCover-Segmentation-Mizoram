# Architectural Blueprint & Implementation Plan: AI-Powered Aerial Land-Use Segmentation Web App
**Project Extension:** Interactive Web Application with Gemini Multimodal Gating & DeepLabV3+ Inference  
**Primary Focus:** Dual-Tier AI Pipeline (Domain Verification -> Semantic Segmentation -> GIS Analytics)  

---

## 1. System Vision & Two-Tier AI Pipeline

This system solves a common flaw in standard computer vision apps: **out-of-domain input failure**. If a user uploads a photo of an indoor room, a car, or a pet, traditional segmentation models output garbage masks. 

Our application introduces a **Two-Tier Intelligent Architecture**:

```mermaid
flowchart TD
    User([User / Urban Planner]) -->|Uploads Image| WebApp[React Dashboard UI]
    WebApp -->|POST /api/analyze| Backend[Backend API Service]
    
    subgraph Tier1["Tier 1: Gemini Vision AI (Domain & Class Guardrail)"]
        Backend -->|Send Image + Schema Prompt| Gemini[Gemini 1.5 Flash Vision API]
        Check{"Valid Aerial Scene & Contains Target Classes?"}
        Gemini --> Check
        Check -->|NO: Cat/Selfie/Indoor/Irrelevant| Reject[Return Clean Error & Explanation to User]
        Check -->|YES: Valid Overhead Aerial Scene| Passed[Extract Domain Context & Class Tags]
    end
    
    subgraph Tier2["Tier 2: DeepLabV3+ & GDAL (Segmentation & Quantification)"]
        Passed --> PyTorch[DeepLabV3+ ResNet-50 CBST Model (da_best.pth)]
        PyTorch --> PredMask[Generate Pixel-Wise Classification Mask]
        PredMask --> Overlay[Generate Alpha-Blended Superimposed Overlay]
        PredMask --> GDAL[GDAL Geospatial Engine (0.3m GSD)]
        GDAL --> AreaStats[Calculate Surface Area in Hectares & Sq Meters]
        GDAL --> GeoTIFF[Generate Calibrated 8-Bit GeoTIFF Raster]
    end
    
    Reject --> WebApp
    AreaStats --> WebApp
    Overlay --> WebApp
    GeoTIFF --> WebApp
    WebApp -->|Interactive Dashboard| User
```

---

## 2. Tier 1: Gemini Multimodal Guardrail Specifications

When an image is uploaded, the backend queries the Gemini Vision API using structured JSON schema output:

```json
{
  "is_aerial_or_satellite": true,
  "confidence_score": 0.98,
  "detected_classes": ["forest", "agriculture", "road", "building"],
  "terrain_type": "Mountainous rural valley with terraced farming",
  "reasoning": "High-altitude orthogonal view showing agricultural parcels and mountain canopy.",
  "proceed_to_segmentation": true
}
```

* **If `proceed_to_segmentation == false`:** The UI informs the user:  
  * *"Image rejected: Uploaded image is not an aerial/satellite overhead photograph. Please upload satellite imagery."*
* **If `proceed_to_segmentation == true`:** Gemini generates a contextual natural language report for the user (e.g. *"Identified rural settlement in hilly terrain with 4 distinct land-cover types. Proceeding to sub-meter segmentation..."*).

---

## 3. Recommended Tech Stack Comparison

Since you already know the **MERN Stack (MongoDB, Express, React, Node.js)**, here are the two architectural paths:

### Option A: React (MERN Frontend) + FastAPI (Python Backend) — RECOMMENDED
* **Frontend:** React (Vite + Tailwind CSS + Lucide Icons + Recharts)
* **Backend:** FastAPI (Python)
* **Why this is the best fit:**
  1. **Zero IPC Overhead:** PyTorch, GDAL, Pillow, and the `google-genai` Python SDK all run in the same memory space. Model weights stay pre-loaded in GPU/RAM.
  2. **FastAPI syntax is almost identical to Express.js:** It uses `async/await`, Pydantic request models (similar to Joi/Zod), and JSON routing. As a MERN developer, you will feel at home immediately.
  3. **Performance:** Instant inference without having to spawn child Python processes from Node.js.

### Option B: Full MERN + Python Microservice
* **Frontend:** React + Tailwind
* **API Gateway:** Node.js / Express.js (Handles auth, file uploads, MongoDB history, Gemini API)
* **Inference Worker:** Python Flask/FastAPI worker (Invoked by Express to run PyTorch)
* **Database:** MongoDB (Saves past segmentation history, uploaded photos, and land-use reports)
* **Best used if:** You specifically want user authentication (login/signup), saved user project history, and a MongoDB dashboard.

---

## 4. Key Interactive UI Features (Frontend Dashboard)

1. **Before / After Split Slider:** Slide left/right to reveal the underlying aerial image beneath the colored segmentation mask.
2. **Opacity Slider:** Real-time alpha blending slider (0% to 100%) to inspect building rooftops and road boundaries.
3. **Interactive Charts:** Recharts Donut & Bar chart showing physical hectares calculated via GDAL.
4. **Sample Scene Quick-Selector:** Lets users test the app with 1 click using pre-loaded LoveDA sample scenes without searching for files.

---

## 5. Phased Implementation Roadmap

### Phase 1: Backend Setup & Gemini Multimodal Guardrail
* Initialize backend server (`FastAPI` or `Express`).
* Connect Gemini 1.5 Flash Vision API using your API key.
* Create validation prompt enforcing strict JSON output for aerial scene verification.

### Phase 2: Segmentation Inference & GDAL Pipeline
* Integrate `da_best.pth` DeepLabV3+ model with pre-loaded weights into backend memory.
* Implement `/api/segment` endpoint returning:
  1. Base64-encoded color segmentation mask.
  2. Base64-encoded superimposed overlay image.
  3. JSON payload of physical hectare areas per class calculated via GDAL.
  4. Downloadable 8-bit GeoTIFF raster.

### Phase 3: React Frontend Dashboard UI (Vite + Tailwind)
* Build clean, responsive UI with dark/light theme.
* Implement Drag & Drop aerial photo upload zone.
* Add Quick Sample buttons (Farmland 2522, Mountain Forest 2532, River Basin 2544).

### Phase 4: Interactive Visual Tools & Analytics
* Integrate Before/After split slider component (`react-compare-image` or custom canvas).
* Build interactive land-use Donut and Bar charts with `Recharts`.
* Add one-click export buttons (Download GeoTIFF, Download Mask, Print Summary).

