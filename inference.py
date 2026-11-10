# -*- coding: utf-8 -*-
"""
Standalone Inference Pipeline for Aerial Image Segmentation
Project Code: BT23CS028 (Sem 7 Capstone)

Usage:
    python inference.py --image path/to/aerial_image.png --weights checkpoints/da_best.pth --output results/prediction.png
"""

import os
import argparse
import numpy as np
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="Run inference using trained DeepLabV3+ model on aerial imagery.")
    parser.add_argument("--image", type=str, required=True, help="Path to input aerial RGB image (.png or .jpg)")
    parser.add_argument("--weights", type=str, default="checkpoints/da_best.pth", help="Path to model weights (.pth)")
    parser.add_argument("--output", type=str, default="results/inference_segmented.png", help="Path to save output segmented mask")
    parser.add_argument("--gsd", type=float, default=0.3, help="Ground Sampling Distance in meters/pixel (default: 0.3m)")
    args = parser.parse_args()

    # Classes and Colors
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

    print("=" * 65)
    print("  AERIAL IMAGE SEGMENTATION INFERENCE PIPELINE")
    print("=" * 65)
    print(f"  Input Image   : {args.image}")
    print(f"  Model Weights : {args.weights}")
    print(f"  Output Path   : {args.output}")

    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Input image not found: {args.image}")

    # Check for PyTorch & smp
    try:
        import torch
        import torch.nn.functional as F
        import segmentation_models_pytorch as smp
    except ImportError:
        print("[ERROR] PyTorch or segmentation_models_pytorch not installed.")
        print("Install via: pip install torch segmentation-models-pytorch")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Inference Device: {device}")

    # Build model architecture
    print("  Loading DeepLabV3+ (ResNet-50) architecture...")
    model = smp.DeepLabV3Plus(
        encoder_name="resnet50",
        encoder_weights=None,
        in_channels=3,
        classes=7,
    ).to(device)

    # Load weights
    if os.path.exists(args.weights):
        ck = torch.load(args.weights, map_location=device, weights_only=False)
        state = ck["model_state_dict"] if "model_state_dict" in ck else ck
        model.load_state_dict(state)
        print(f"  [OK] Successfully loaded weights from {args.weights}")
    else:
        print(f"  [WARN] Weights file '{args.weights}' not found locally. Running with initialized weights for demonstration.")

    model.eval()

    # Load and preprocess image
    orig_im = Image.open(args.image).convert("RGB")
    orig_np = np.array(orig_im)
    h, w = orig_np.shape[:2]

    # Normalize (ImageNet stats)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std  = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    norm_img = ((orig_np / 255.0) - mean) / std
    tensor = torch.from_numpy(norm_img).permute(2, 0, 1).unsqueeze(0).float().to(device)

    print("  Running neural segmentation inference...")
    with torch.no_grad():
        logits = model(tensor)
        pred = logits.argmax(dim=1).squeeze(0).cpu().numpy().astype(np.uint8)

    # Convert prediction to RGB color image
    color_mask = np.zeros((h, w, 3), dtype=np.uint8)
    for c in range(len(CLASS_NAMES)):
        color_mask[pred == c] = CLASS_COLORS[c]

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    out_im = Image.fromarray(color_mask)
    out_im.save(args.output)
    print(f"  [OK] Segmented color mask saved to: {args.output}")

    # Geospatial Area Calculation
    pixel_area_m2 = args.gsd * args.gsd
    total_pixels  = (pred != 255).sum()
    print("\n" + "=" * 65)
    print(f"  PHYSICAL LAND-COVER COVERAGE (GSD = {args.gsd} m/pixel)")
    print("=" * 65)
    print(f"  {'Class':<16} {'Pixels':>10} {'Area (m²)':>14} {'Area (Hectares)':>16} {'Share (%)':>12}")
    print("  " + "-" * 72)
    for c in ACTIVE_CLASSES:
        c_pix = (pred == c).sum()
        area_m2 = c_pix * pixel_area_m2
        area_ha = area_m2 / 10000.0
        pct = (c_pix / max(total_pixels, 1)) * 100.0
        name = CLASS_NAMES[c]
        print(f"  {name.capitalize():<16} {c_pix:>10d} {area_m2:>14.1f} {area_ha:>16.4f} ha {pct:>11.2f}%")
    print("=" * 65)

if __name__ == "__main__":
    main()
