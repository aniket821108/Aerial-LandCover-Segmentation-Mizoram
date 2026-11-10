# -*- coding: utf-8 -*-
"""
Generates publication-quality presentation slide figures:
1. slide_pair_farms_2522.png    (Original vs Classified: Farmland & Village)
2. slide_pair_forest_2532.png   (Original vs Classified: Mountain Forest & Road)
3. slide_pair_water_2544.png    (Original vs Classified: River Basin & Fields)
4. slide_segmentation_gallery_16x9.png (Full 16:9 slide-ready showcase)
"""

import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

images_dir = r"LoveDA\Val\Rural\images_png"
gdal_dir   = r"Aerial_Segmentation_Mizoram\gdal_outputs\batch_exports"
out_dir    = r"Aerial_Segmentation_Mizoram\results"

def mask_to_rgb(mask_2d):
    h, w = mask_2d.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for c in range(len(CLASS_NAMES)):
        rgb[mask_2d == c] = CLASS_COLORS[c]
    return rgb

# Common legend
legend_patches = [
    mpatches.Patch(color=CLASS_COLORS[c]/255.0, label=CLASS_NAMES[c].capitalize())
    for c in ACTIVE_CLASSES
]

# ------------------------------------------------------------------------------
# 1. Generate Individual 2-Panel Pairs for specific scenes
# ------------------------------------------------------------------------------
scenes = [
    ("2522", "Rural Farmland & Settlement", "slide_pair_farms_2522.png"),
    ("2532", "Dense Mountain Forest & Road", "slide_pair_forest_2532.png"),
    ("2544", "River Basin & Agriculture",   "slide_pair_water_2544.png"),
]

for sid, label, out_name in scenes:
    img_p = os.path.join(images_dir, f"{sid}.png")
    tif_p = os.path.join(gdal_dir, f"{sid}_segmented.tif")

    orig_img = Image.open(img_p).convert("RGB")
    pred_mask = np.array(Image.open(tif_p))
    pred_rgb = mask_to_rgb(pred_mask)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor="white")

    axes[0].imshow(orig_img)
    axes[0].set_title("Original Aerial Photograph (Input)", fontsize=14, fontweight="bold", pad=10)
    axes[0].axis("off")

    axes[1].imshow(pred_rgb)
    axes[1].set_title(f"Classified Land-Cover Mask (CBST Model)", fontsize=14, fontweight="bold", pad=10)
    axes[1].axis("off")

    fig.legend(handles=legend_patches, loc="lower center", ncol=6, fontsize=12,
               frameon=True, bbox_to_anchor=(0.5, -0.05), facecolor="#f8f9fa", edgecolor="#ced4da")

    plt.suptitle(f"Land Use Classification Demonstration — {label} (Scene {sid})",
                 fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    out_path = os.path.join(out_dir, out_name)
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {out_path}")

# ------------------------------------------------------------------------------
# 2. Generate a Complete 16:9 Master Showcase Slide (3 Scenes Side-by-Side)
# ------------------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(18, 10), facecolor="white")

for col, (sid, label, _) in enumerate(scenes):
    img_p = os.path.join(images_dir, f"{sid}.png")
    tif_p = os.path.join(gdal_dir, f"{sid}_segmented.tif")

    orig_img = Image.open(img_p).convert("RGB")
    pred_mask = np.array(Image.open(tif_p))
    pred_rgb = mask_to_rgb(pred_mask)

    # Top row: Original
    axes[0, col].imshow(orig_img)
    axes[0, col].set_title(f"Original: {label}\n(Scene {sid})", fontsize=13, fontweight="bold", pad=8)
    axes[0, col].axis("off")

    # Bottom row: Classified
    axes[1, col].imshow(pred_rgb)
    axes[1, col].set_title(f"Classified: {label}", fontsize=13, fontweight="bold", pad=8)
    axes[1, col].axis("off")

fig.legend(handles=legend_patches, loc="lower center", ncol=6, fontsize=13,
           frameon=True, bbox_to_anchor=(0.5, -0.04), facecolor="#f8f9fa", edgecolor="#ced4da")

plt.suptitle("DeepLabV3+ Semantic Segmentation Across Diverse Rural Scenes (LoveDA / Mizoram Evaluation)",
             fontsize=17, fontweight="bold", y=1.01)
plt.tight_layout()
gallery_out = os.path.join(out_dir, "slide_segmentation_gallery_16x9.png")
plt.savefig(gallery_out, dpi=220, bbox_inches="tight")
plt.close()
print(f"[OK] Generated Master 16:9 Showcase: {gallery_out}")
