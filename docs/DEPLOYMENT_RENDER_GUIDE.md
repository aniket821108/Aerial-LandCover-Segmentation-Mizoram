# 🚀 How to Deploy AeroSeg AI on Render (Free Tier)

This guide walks you through deploying the complete **AeroSeg AI** platform (React Frontend + Express API Gateway + Python ML Service + MongoDB Atlas + Gemini Vision AI) on **[Render.com](https://render.com)** for free.

---

## 🌟 Why Docker Deployment on Render is Best:
By using the provided [`Dockerfile`](../Dockerfile) and [`render.yaml`](../render.yaml), Render builds and hosts the **entire full-stack application inside a single free container**:
- **1 Free Service:** Fits within Render's free tier without needing multiple separate web services.
- **Zero Network Lag:** Express communicates with the Python ML service locally via `127.0.0.1:8000`.
- **Single Public URL:** Both the React UI and API endpoints are served from `https://your-app-name.onrender.com`.

---

## 📋 Step-by-Step Deployment Instructions

### Step 1: Sign In to Render
1. Open **[render.com](https://render.com)** and sign in (preferably with your GitHub account).

---

### Step 2: Create a New Web Service
1. In the Render Dashboard, click the **"New +"** button at the top right $\rightarrow$ select **"Web Service"**.
2. Select **"Build and deploy from a Git repository"** $\rightarrow$ click **Next**.
3. Connect your GitHub account and select your repository:
   👉 **`aniket821108/Aerial-LandCover-Segmentation-Mizoram`**

---

### Step 3: Configure the Web Service

Fill in the settings as follows:

| Field | Value |
| :--- | :--- |
| **Name** | `aeroseg-ai` *(or any unique name you prefer)* |
| **Region** | `Oregon (US West)` *(or Frankfurt / Singapore)* |
| **Branch** | `main` |
| **Root Directory** | *(Leave empty - uses repository root)* |
| **Language / Environment** | **`Docker`** |
| **Dockerfile Path** | `Dockerfile` |
| **Instance Type** | **`Free`** |

---

### Step 4: Add Environment Variables

Scroll down to the **"Environment Variables"** section and click **"Add Environment Variable"** for each of these:

| Key | Value | Notes |
| :--- | :--- | :--- |
| `MONGO_URI` | `mongodb+srv://AeroSeg_AI:TGSLYyBCK5cQ20lb@cluster0.yi4ir.mongodb.net/aerial_segmentation?retryWrites=true&w=majority` | Your MongoDB Atlas connection string |
| `GEMINI_API_KEY` | `AIzaSyDwr0WWPFO9iXJnG141kKcWRnV4et5XFXw` | Your Google Gemini API Key |
| `NODE_ENV` | `production` | Enables production React SPA serving |
| `ML_SERVICE_URL` | `http://127.0.0.1:8000` | Internal Python ML worker URL |

---

### Step 5: Deploy!
1. Click **"Deploy Web Service"** at the bottom of the page.
2. Render will automatically:
   - Pull your repository from GitHub.
   - Install Python ML dependencies.
   - Install Node.js dependencies and build the Vite React client.
   - Start the Python FastAPI microservice on port 8000 and the Express server on Render's assigned port.
3. Once the build completes and shows **"Live"**, your website will be accessible at:
   👉 **`https://aeroseg-ai.onrender.com`**

---

## 🔍 How to Verify Deployment

1. Open your Render public URL (`https://your-service.onrender.com`).
2. You will see the **AeroSeg AI** dashboard live!
3. Click **"Scene 2522"** or **"Scene 2532"** to run segmentation.
4. Click **"Test Non-Aerial"** to verify the Gemini Vision Guardrail.
5. Check your MongoDB Atlas dashboard $\rightarrow$ browse collections $\rightarrow$ you will see new scans logged into `aerial_segmentation.scanrecords`!
