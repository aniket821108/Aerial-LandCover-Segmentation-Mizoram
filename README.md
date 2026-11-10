# Aerial Image Segmentation for Land Use Classification
### Unsupervised Domain Adaptation (Urban -> Rural) with DeepLabV3+ & GDAL
**Project Code:** BT23CS028 | **Course:** 7th Semester B.Tech Computer Science Capstone  
**Target Geography:** Mizoram (Mountainous terrain, shifting *jhum* terrace agriculture, dense forest canopy)  

---

## 📌 Project Overview
This repository implements an end-to-end aerial image semantic segmentation and unsupervised domain adaptation pipeline on the **LoveDA** remote sensing dataset (0.3m Ground Sampling Distance). 

Deep learning models trained on structured urban cities suffer severe degradation when deployed to rural, mountainous regions. This project bridges that domain gap using **Class-Balanced Self-Training (CBST)** without requiring manual annotations in the rural target domain. Additionally, it features a **GDAL Geospatial Engine** to export georeferenced 8-bit GeoTIFF rasters and calculate physical land-cover surface area in hectares.

```text
[Urban Source Domain] (1,156 scenes) ---> DeepLabV3+ (ResNet-50) Baseline ---> 38.93% Urban mIoU
                                                                                   |
                                      Zero-Shot on Rural: 23.39% mIoU  <-----------+
                                      (Domain Gap: -15.55% Drop!)
                                                    |
                                                    v
[Rural Target Domain] (1,366 scenes) ---> True CBST Adaptation (3 Rounds) ---> 27.90% Rural mIoU
                                                                               (+4.52% Gain / +19.3% rel.)
```

---

## 🖼️ Visual Demonstration: Original Image vs. Classified Output
Below is an empirical demonstration of the adapted model performing pixel-wise land-use classification on a representative rural aerial scene (Scene 2522):

### 1. Two-Panel View: Raw Input vs. Predicted Segmentation
![Original vs Classified](results/original_vs_classified.png)

### 2. Three-Panel View with Superimposed Translucent Overlay
![Classification Comparison with Overlay](results/classification_comparison.png)

* 🔴 **Building (Red):** Accurate rooftop localization on scattered rural settlements.
* 🟡 **Road (Yellow):** Continuous extraction of narrow, unpaved rural tracks (+11.27% IoU gain!).
* 🔵 **Water (Blue):** Clear boundary identification of natural ponds and irrigation streams.
* 🟢 **Forest (Green):** Dense canopy coverage on hillsides.
* 🌾 **Agriculture (Tan/Orange):** Precision mapping of terraced farmland and crop parcels (71.3% of scene).

---

## 🎯 Classification Categories (6 Target Land-Use Classes)
The pipeline classifies high-resolution overhead scenes into **6 primary land-use categories** (+ Background, with invalid boundary pixels mapped to `IGNORE_INDEX = 255`):
1. 🏢 **Building (Urban):** Rooftops, built structures
2. 🛣️ **Road:** Paved highways, winding rural dirt tracks
3. 💧 **Water:** Rivers, natural mountain streams, reservoirs
4. 🪨 **Barren:** Exposed rock, excavation sites, cleared slopes
5. 🌲 **Forest:** Dense subtropical canopy, bamboo groves
6. 🌾 **Agriculture:** Terraced hillside cultivation, valley plots

---

## 📊 Experimental Results

### 1. Quantitative Performance: Baseline vs. CBST Adaptation

| Category / Class | Urban Source IoU | Rural Baseline IoU | CBST Adapted IoU | Net Gain ($\Delta$) | Relative Surge |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Overall Rural mIoU** | **38.93%** | **23.39%** | **27.90%** | **+4.52%** | **+19.31%** |
| 🛣️ **Road** | 44.90% | 20.03% | **31.30%** | **+11.27%** | **+56.27% 🚀** |
| 💧 **Water** | 55.57% | 38.21% | **46.15%** | **+7.95%** | **+20.79%** |
| 🌾 **Agriculture** | 46.27% | 42.31% | **48.19%** | **+5.88%** | **+13.90%** |
| 🌲 **Forest** | 38.48% | 14.65% | **17.97%** | **+3.32%** | **+22.64%** |
| 🏢 **Building** | 43.54% | 22.96% | **22.40%** | -0.56% | Preserved |
| 🪨 **Barren** | 4.84% | 2.15% | **1.39%** | -0.76% | Scarce |

* **Domain Gap Reduction:** The cross-domain deficit shrank from **15.55% down to 11.03%**, closing **29.1%** of the total performance gap.

### 2. Full-Dataset GeoTIFF Batch Verification (GDAL Engine)
Beyond standard tensor evaluation, the notebook features an end-to-end geospatial verification pipeline that re-reads all **992 exported GeoTIFF files** via GDAL (`osgeo.gdal`) and computes the confusion matrix directly on the physical rasters:

| Land-Cover Class | Exported GeoTIFF IoU | Performance Impact |
| :--- | :---: | :--- |
| 🛣️ **Road** | **43.59%** | Outstanding extraction of rural dirt tracks & unpaved trails |
| 🌾 **Agriculture** | **47.87%** | Sharp delineation of terraced hillside crop parcels |
| 🏢 **Building** | **34.06%** | Accurate rooftop localization across rural settlements |
| 🌲 **Forest** | **22.96%** | Continuous canopy mapping across mountainous terrain |
| 💧 **Water** | **25.55%** | Reliable natural creek & pond segmentation |
| 🪨 **Barren** | **3.38%** | Exposed rock outcrop and landslide slope detection |
| **Overall GeoTIFF mIoU** | **29.57%** | **Verified over 992 production GeoTIFF rasters** |

---

## 🗺️ Geospatial Engine Integration (GDAL)
* **Spatial Resolution:** Ground Sampling Distance (GSD) = $0.3\text{ m/pixel} \implies 1\text{ pixel} = 0.09\text{ m}^2$.
* **Real-World Surface Area Calculation:**
  $$\text{Area (Hectares)} = \frac{\text{Pixel Count} \times 0.09\text{ m}^2}{10{,}000\text{ m}^2}$$
* **GeoTIFF Generation:** Exports standard 8-bit GeoTIFF rasters (`.tif`) with embedded `GDALColorTable` matching the LoveDA palette for direct import into **QGIS** and **ArcGIS**.

---

## 🛠️ Tech Stack
* **Deep Learning:** PyTorch, Segmentation-Models-PyTorch (`smp`), Albumentations
* **Geospatial Processing:** GDAL (`osgeo.gdal`, `osgeo.osr`)
* **Computer Vision:** OpenCV (`cv2`), NumPy, Matplotlib
* **Hardware:** Google Colab T4 GPU (FP16 Native Mixed Precision)

---

## 📁 Repository Structure
```text
├── notebooks/
│   └── Mizoram_Aerial_Segmentation_Colab.ipynb  # Complete executable Colab notebook
├── docs/
│   ├── PROJECT_FINAL_REPORT.md                  # Comprehensive academic report
│   ├── PRESENTATION_SCRIPT_AND_VIVA_QA.md       # Speaker script + top 10 Viva Q&A
│   └── ROADMAP.md                               # System architecture & milestones
├── results/
│   ├── final_metrics.json                       # Evaluated class IoUs & mIoU
│   ├── domain_gap_metrics.json                  # Baseline domain gap analysis
│   ├── cbst_comparison_bar.png                  # IoU improvement bar charts
│   ├── side_by_side_comparison.png              # 4-panel visual comparisons
│   └── gdal_outputs/                            # Sample GeoTIFF outputs for GIS
└── .gitignore                                   # Safe rules (ignores datasets & large weights)
```

---

## 🚀 How to Run in Google Colab
1. Upload [`notebooks/Mizoram_Aerial_Segmentation_Colab.ipynb`](notebooks/Mizoram_Aerial_Segmentation_Colab.ipynb) to Google Colab.
2. Ensure GPU runtime is selected (`T4 GPU`).
3. Set your Google Drive dataset path to `LoveDA_Project/` (containing `Train` and `Val`).
4. Execute cells sequentially. Checkpoints and figures will automatically sync to your Drive.

