# Project Report Outline: Aerial Image Segmentation for Land Use Classification
**Course:** 7th Semester Computer Vision Project  
**Candidate Roll / Project Code:** BT23CS028  
**Topic:** Land Use / Land Cover (LULC) Semantic Segmentation with Unsupervised Domain Adaptation (Urban -> Rural) for Mizoram Geography  

---

## 1. Introduction & Problem Statement
* Background of aerial remote sensing and deep learning in land-use classification.
* Formal Problem Statement: Segmenting 6 semantic land categories (Water, Building/Urban, Agriculture, Road, Barren, Forest) + Background.
* Relevance to Mizoram: Mountainous terrain, tropical forest canopy, terraced *jhum* farming, and severe lack of labeled rural satellite imagery.

## 2. Dataset & Geospatial Processing (LoveDA & GDAL)
* **Dataset Characteristics:** LoveDA high-spatial-resolution (0.3m Ground Sampling Distance) aerial imagery.
* Split Breakdown:
  * Urban Source Domain (1,156 training images)
  * Rural Target Domain (1,366 training images)
  * Urban & Rural Validation splits
* **GDAL Integration:**
  * Spatial resolution and raster metadata extraction.
  * Geospatial surface area quantification in hectares ($10{,}000\text{ m}^2$).
  * Georeferenced GeoTIFF generation with embedded color lookup tables for GIS software (QGIS / ArcGIS).

## 3. Methodology & System Architecture
* **Backbone Architecture:** DeepLabV3+ with ResNet-50 encoder (ImageNet pretrained) and Atrous Spatial Pyramid Pooling (ASPP).
* **Supervised Source Training:** Baseline model trained on Urban scenes with AdamW and Cosine Annealing learning rate schedule.
* **Domain Gap Analysis:** Empirical evaluation of the Urban-trained model on Rural scenes to quantify performance drop due to domain shift.
* **Class-Balanced Self-Training (CBST):**
  * Dynamic class-specific threshold estimation ($\lambda_c$) using top-$p\%$ quantiles.
  * Progressive multi-round pseudo-label generation.
  * Joint optimization on source ground truth and target pseudo-labels.

## 4. Experimental Results & Discussion
* **Quantitative Comparison Table:**
  * Baseline (Urban only) vs CBST Adapted Model on Rural target domain.
  * Mean Intersection-over-Union (mIoU) and class-wise IoU (Water, Building, Agriculture, Road, Barren, Forest).
  * Domain gap reduction ($\Delta \text{mIoU}$).
* **Visual Progressions:**
  * 4-Panel comparison: `[Input Scene | Ground Truth | Baseline | CBST Adapted]`.
  * Analysis of challenging rural regions (dense tree cover, hill roads, irregular farm plots).
* **Geospatial Area Estimation:**
  * Breakdown of rural land-use distribution in hectares.

## 5. Conclusion & Future Scope
* Summary of findings: CBST effectively bridges the urban-to-rural gap without requiring expensive manual annotations in rural terrain.
* Application for regional planning, environmental monitoring, and disaster risk mapping in Mizoram.

