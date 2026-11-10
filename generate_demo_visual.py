# -*- coding: utf-8 -*-
"""
Generates a high-resolution side-by-side classification demonstration:
Panel 1: Original Aerial Image
Panel 2: Classified / Segmented Image (with Color Legend)
Panel 3: Overlay (Segmented classes superimposed on the real aerial photo)
"""

import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Classes & Colors
CLASS_NAMES = ["background", "building", "road", "water", "barren", "forest", "agriculture"]
ACTIVE_CLASSES = [1, 2, 3, 4, 5, 6]
CLASS_COLORS = np.array([
    [0,   0,   0],      # 0 Background (Black)
    [255, 0,   0],      # 1 Building   (Red)
    [255, 255, 0],      # 2 Road       (Yellow)
    [0,   0,   255],    # 3 Water      (Blue)
    [159, 129, 183],    # 4 Barren     (Purple/Grey)
    [0,   255, 0],      # 5 Forest     (Green)
    [255, 195, 128],    # 6 Agriculture(Orange/Tan)
], dtype=np.uint8)

# Input files
img_path = r"LoveDA\Val\Rural\images_png\2522.png"
gt_path  = r"LoveDA\Val\Rural\masks_png\2522.png"
pred_tif = r"Aerial_Segmentation_Mizoram\gdal_outputs\2522_segmented.tif"

out_path = r"Aerial_Segmentation_Mizoram\results\classification_comparison.png"
out_2panel = r"Aerial_Segmentation_Mizoram\results\original_vs_classified.png"

# 1. Load Original Image
orig_img = Image.open(img_path).convert("RGB")
img_np = np.array(orig_img)
h, w = img_np.shape[:2]

# 2. Load Model Prediction from GeoTIFF
pred_im = Image.open(pred_tif)
pred_mask = np.array(pred_im)

# Convert prediction mask to RGB color image
def mask_to_color(mask):
    rgb = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    for c in range(len(CLASS_NAMES)):
        rgb[mask == c] = CLASS_COLORS[c]
    return rgb

pred_color_np = mask_to_color(pred_mask)
pred_color_img = Image.fromarray(pred_color_np)

# 3. Create Semi-Transparent Overlay (45% blend onto original)
overlay_img = Image.blend(orig_img, pred_color_img, alpha=0.45)

# ==============================================================================
# Figure 1: Clean 2-Panel (Original vs Classified)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

axes[0].imshow(orig_img)
axes[0].set_title("Original Aerial Image (Input)", fontsize=16, fontweight="bold", pad=12)
axes[0].axis("off")

axes[1].imshow(pred_color_img)
axes[1].set_title("Classified / Segmented Image (Model Output)", fontsize=16, fontweight="bold", pad=12)
axes[1].axis("off")

# Legend
legend_patches = [
    mpatches.Patch(color=CLASS_COLORS[c]/255.0, label=CLASS_NAMES[c].capitalize())
    for c in ACTIVE_CLASSES
]
fig.legend(handles=legend_patches, loc="lower center", ncol=6, fontsize=13,
           frameon=True, bbox_to_anchor=(0.5, -0.04), facecolor="#f8f9fa", edgecolor="#ced4da")

plt.suptitle("Aerial Image Segmentation: Original vs. Classified Land-Use (Rural Scene 2522)",
             fontsize=18, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(out_2panel, dpi=200, bbox_inches="tight")
plt.close()
print(f"[OK] Saved 2-Panel: {out_2panel}")

# ==============================================================================
# Figure 2: Detailed 3-Panel with Overlay (Original | Classified | Overlay)
# ==============================================================================
fig, axes = plt.subplots(1, 3, figsize=(24, 8))

axes[0].imshow(orig_img)
axes[0].set_title("1. Original Aerial Photo", fontsize=15, fontweight="bold", pad=12)
axes[0].axis("off")

axes[1].imshow(pred_color_img)
axes[1].set_title("2. Classified Land-Use Mask", fontsize=15, fontweight="bold", pad=12)
axes[1].axis("off")

axes[2].imshow(overlay_img)
axes[2].set_title("3. Classified Overlay on Photo", fontsize=15, fontweight="bold", pad=12)
axes[2].axis("off")

fig.legend(handles=legend_patches, loc="lower center", ncol=6, fontsize=13,
           frameon=True, bbox_to_anchor=(0.5, -0.04), facecolor="#f8f9fa", edgecolor="#ced4da")

plt.suptitle("Model Inference: High-Resolution Overhead Land Cover Classification",
             fontsize=19, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(out_path, dpi=200, bbox_inches="tight")
plt.close()
print(f"[OK] Saved 3-Panel with Overlay: {out_path}")

# ==============================================================================
# Print Quantitative Breakdown
# ==============================================================================
pixel_area_m2 = 0.3 * 0.3
total_pixels = (pred_mask != 255).sum()
print("\n" + "=" * 65)
print("LAND-USE CLASSIFICATION BREAKDOWN (SCENE 2522):")
print("=" * 65)
for c in ACTIVE_CLASSES:
    c_pix = (pred_mask == c).sum()
    area_ha = (c_pix * pixel_area_m2) / 10000.0
    pct = (c_pix / max(total_pixels, 1)) * 100.0
    if pct > 0.1:
        print(f"  {CLASS_NAMES[c].capitalize():<15} : {pct:>6.2f}% of scene | {area_ha:>8.4f} Hectares")
print("=" * 65)
