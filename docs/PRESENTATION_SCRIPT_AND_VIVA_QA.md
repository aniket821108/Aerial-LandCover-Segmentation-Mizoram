# Presentation Script & Viva Defense Q&A: Aerial Image Segmentation
**Project Code:** BT23CS028  
**Project Title:** Aerial Image Segmentation for Land Use Classification  
**Course:** 7th Semester Computer Vision Capstone Evaluation  

---

## Part 1: Slide-by-Slide Speaker Notes (What to Say to the Panel)

Use this script during your 8-10 minute presentation. It hits all key academic points while keeping the delivery confident and structured.

---

### Slide 1: Title Slide
> *"Respected professors and committee members, good morning. Today, I am presenting my 7th-semester project titled **Aerial Image Segmentation for Land Use Classification**. In this work, we tackle semantic segmentation across 6 core land-cover classes, with a dedicated focus on **Unsupervised Domain Adaptation from Urban to Rural aerial scenes**, motivated by the unique geographic terrain of **Mizoram**. Our implementation is built using **PyTorch** and **GDAL**."*

---

### Slide 2: Motivation & Mizoram Geography
> *"To motivate our problem: Remote sensing is critical for monitoring natural resources, deforestation, and urban expansion. However, in regions like **Mizoram**, over 85% of the land is mountainous, heavily forested, and shaped by shifting *jhum* terrace agriculture. While modern deep learning models perform well in structured urban cities, annotated aerial imagery for rural, hilly terrain is exceptionally scarce. Our goal is to train on easily available urban data and adapt the network to rural scenes without needing expensive manual rural annotations."*

---

### Slide 3: Problem Statement & Land-Cover Classes
> *"Our objective is pixel-level semantic segmentation across **6 distinct land-use categories**: Buildings, Roads, Water, Barren land, Forest, and Agriculture. Background is handled separately, and invalid boundary pixels are strictly mapped to an ignore index of 255. This ensures clean cross-entropy loss calculation with zero label collision."*

---

### Slide 4: LoveDA Dataset Overview
> *"We utilized the **LoveDA remote sensing benchmark**, which features high-resolution overhead imagery with a **Ground Sampling Distance of 0.3 meters per pixel**. The dataset is uniquely divided into two geographic domains: an **Urban Source domain** with over 1,100 scenes featuring orthogonal grids and paved infrastructure, and a **Rural Target domain** with over 1,300 scenes characterized by dispersed settlements and irregular vegetation."*

---

### Slide 5: The Challenge: Urban to Rural Domain Shift
> *"When a model trained purely on urban scenes is tested zero-shot on rural aerial imagery, it suffers a severe performance drop—what we quantify as the **Domain Gap**. This degradation happens because rooftop materials, road widths, and vegetation density look drastically different. Mountain topography also introduces cast shadows and non-orthogonal orientations, causing urban models to confuse cleared slopes with barren land or buildings."*

---

### Slide 6: Segmentation Architecture (DeepLabV3+)
> *"For our network architecture, we selected **DeepLabV3+** with a pretrained **ResNet-50 backbone**. DeepLabV3+ utilizes **Atrous Spatial Pyramid Pooling (ASPP)** with multiple dilation rates. This allows the model to capture multi-scale context simultaneously—essential in aerial imagery where a narrow rural road requires fine local details while a large forest reserve requires a wide receptive field."*

---

### Slide 7: Unsupervised Adaptation via True CBST
> *"To bridge the domain gap without rural labels, we implemented **Class-Balanced Self-Training (CBST)**. Standard self-training uses a flat global threshold like 0.9, which fails because dominant classes like Forest monopolize the pseudo-labels, while scarce classes like Buildings or Roads get completely starved. CBST solves this by dynamically calculating **class-specific thresholds ($\lambda_c$)** using confidence quantiles. This guarantees that all 6 classes contribute pseudo-labels for iterative retraining."*

---

### Slide 8: GDAL Geospatial Engine
> *"As specified in the syllabus requirements, we integrated **GDAL** for production-grade GIS workflows. GDAL is used to inspect spatial raster parameters, export predicted masks as standard 8-bit **GeoTIFFs with embedded color lookup tables** for direct viewing in QGIS, and calculate real-world surface area in **hectares** using our known 0.3-meter ground resolution ($0.09\text{ m}^2/\text{pixel}$)."*

---

### Slide 9: Experimental Protocol & Hyperparameters
> *"Our experiments were executed in Google Colab utilizing T4 GPU acceleration with PyTorch Native Mixed Precision (FP16 AMP). We optimized with AdamW and a Cosine Annealing learning rate schedule. We established early stopping on the baseline and executed 3 progressive rounds of CBST adaptation, gradually expanding the selected pseudo-label portion from 20% to 50%."*

---

### Slide 10: Quantitative Results & Domain Gap Reduction
> *"Here we see our quantitative comparison. Training purely on Urban data resulted in a baseline rural mIoU of **23.39%**. After applying Class-Balanced Self-Training over 3 rounds, our adapted model achieved **27.90% mIoU**, delivering a solid net gain of **+4.52% mIoU**—a **+19.3% relative improvement** without using a single rural manual label! In particular, we saw huge surges in **Roads (+11.27% gain, up to 31.30%)**, **Water (+7.95% gain, up to 46.15%)**, **Agriculture (+5.88% gain, up to 48.19%)**, and **Forest (+3.32% gain, up to 17.97%)**, which closed almost 30% of the initial domain gap."*

---

### Slide 11: Visual Comparison & Land-Use Area Case Study
> *"Visually, the baseline model frequently missed narrow rural roads and misidentified hillside crops. The CBST adapted model produces sharp, continuous road boundaries and accurate forest segmentations. Through our GDAL engine, we converted these predictions into real-world land coverage metrics, showing that forest and agriculture account for `[XX%]` of the analyzed rural scene."*

---

### Slide 12: Conclusion & Future Scope
> *"In conclusion, this project demonstrates that unsupervised domain adaptation via CBST effectively bridges the urban-to-rural gap in complex remote sensing scenarios like Mizoram. The pipeline delivers both high segmentation accuracy and GIS-ready GeoTIFF exports. In the future, this system can be extended to multi-spectral Sentinel-2 bands for landslide risk assessment and automated forest fire buffer zone mapping. Thank you, and I am now open to your questions."*

---

## Part 2: Top 10 Anticipated Professor / Viva Questions & Model Answers

### Q1: Why did you choose DeepLabV3+ over standard U-Net?
**Answer:**  
*"While U-Net is effective for biomedical images and fine edges, aerial images have an extreme scale variation problem—for example, a single building covers few pixels while agricultural fields cover thousands. DeepLabV3+ introduces **Atrous Spatial Pyramid Pooling (ASPP)**, which applies dilated convolutions at multiple dilation rates ($r=6, 12, 18$). This captures context at multiple receptive field sizes without losing spatial resolution through downsampling."*

---

### Q2: Why is a single global confidence threshold (e.g., 0.90) problematic in Self-Training?
**Answer:**  
*"In remote sensing, class distributions are heavily imbalanced. In rural terrain, Forest and Water are easily predicted with $>90\%$ confidence, while Buildings and Roads may only achieve $60\text{--}70\%$ confidence. A flat 0.90 threshold selects only Forest and Water pseudo-labels, completely starving minority classes and causing the network to ignore buildings and roads. **CBST** computes independent thresholds $\lambda_c$ for each class using top-$p\%$ quantiles, ensuring balanced representation across all 6 categories."*

---

### Q3: What exactly is GDAL doing in your project?
**Answer:**  
*"Standard computer vision libraries like OpenCV or PIL only handle raw RGB pixel arrays. In contrast, **GDAL (Geospatial Data Abstraction Library)** allows us to:
1. Access geospatial raster metadata and coordinate transforms.
2. Calculate real-world surface area in square meters and hectares based on the 0.3m Ground Sampling Distance ($1\text{ pixel} = 0.09\text{ m}^2$).
3. Export predictions into standardized 8-bit **GeoTIFFs with embedded color lookup tables (`GDALColorTable`)**, making the outputs directly usable by urban planners in QGIS or ArcGIS."*

---

### Q4: How is your loss function formulated during the adaptation phase?
**Answer:**  
*"During adaptation, we train on a joint objective:
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{source}}(\text{Urban, Ground Truth}) + \alpha \cdot \mathcal{L}_{\text{target}}(\text{Rural, Pseudo-Labels})$$
Both losses are Cross-Entropy losses configured with `ignore_index = 255`. The source loss preserves semantic features learned on labeled data, while the target pseudo-loss adapts the feature representation to rural appearance."*

---

### Q5: How did you handle the class imbalance between Urban and Rural?
**Answer:**  
*"We addressed this in three ways:
1. Data augmentations including Random Crops ($512\times 512$), flips, and 90-degree rotations to balance feature exposure.
2. Class-balanced pseudo-label thresholding ($\lambda_c$) in CBST.
3. Excluded non-ground and invalid boundary pixels using `IGNORE_INDEX = 255`, evaluating strictly on the 6 active land-cover categories."*

---

### Q6: What is Ground Sampling Distance (GSD), and why does it matter?
**Answer:**  
*"GSD represents the real-world distance between two consecutive pixel centers on the ground. In LoveDA, the GSD is **0.3 meters per pixel**. This means each pixel represents an area of $0.3\text{ m} \times 0.3\text{ m} = 0.09\text{ m}^2$. GSD is fundamental for converting dimensionless pixel counts into physical measurements such as hectares or square kilometers."*

---

### Q7: Why is this work relevant to Mizoram specifically?
**Answer:**  
*"Mizoram has a unique physiography: over 85% forest cover, steep mountainous relief, and widespread practice of *jhum* (slash-and-burn) shifting terrace cultivation. Almost all annotated aerial benchmarks are collected in flat, grid-planned urban areas. An urban model fails on Mizoram's terrain because hillside roads and terrace farms look completely different. Our unsupervised domain adaptation allows regional authorities to monitor land use in Mizoram without having to manually label thousands of rural aerial scenes."*

---

### Q8: What metric did you use to evaluate performance, and why?
**Answer:**  
*"We used **Intersection-over-Union (IoU)** per class and **mean IoU (mIoU)** across the 6 active target categories:
$$\text{IoU}_c = \frac{\text{TP}_c}{\text{TP}_c + \text{FP}_c + \text{FN}_c}$$
Pixel accuracy is misleading in remote sensing because background or forest pixels can dominate the image. IoU heavily penalizes both false positives and false negatives, providing an unbiased assessment of each class."*

---

### Q9: What happens if an image has no pseudo-labels above threshold?
**Answer:**  
*"Pixels failing the class-specific threshold $\lambda_c$ are assigned `IGNORE_INDEX = 255`. In PyTorch, `nn.CrossEntropyLoss(ignore_index=255)` computes zero loss and zero gradient for those pixels. This ensures the model only updates weights on high-confidence pseudo-labels, preventing confirmation bias and error propagation."*

---

### Q10: What are the primary limitations and scope for future work?
**Answer:**  
*"Current limitation: The LoveDA dataset provides 3-band RGB imagery. In real-world remote sensing, multispectral bands (such as Near-Infrared in Sentinel-2) provide NDVI vegetation indices that make distinguishing forest from agriculture even more robust. Future work includes testing on multispectral rasters and deploying the model for landslide and flood risk assessment."*

