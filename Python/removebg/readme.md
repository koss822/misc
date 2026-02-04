# remove_bg.py - Free Background Remover

## Overview

This Python script uses the `rembg` library to automatically remove image backgrounds with AI, just like premium online services such as remove.bg—but completely free and offline. It delivers high-quality results locally without watermarks or usage limits.

## What is CUDA and cuDNN?

**CUDA** (Compute Unified Device Architecture) is NVIDIA's parallel computing platform that lets your NVIDIA GPU accelerate AI/ML workloads beyond graphics rendering. **cuDNN** (CUDA Deep Neural Network library) provides optimized primitives for deep learning operations like convolutions. Together, they speed up background removal significantly (5-10x faster) on compatible hardware, though the script runs perfectly on CPU without them.

**No NVIDIA GPU required**—it falls back to CPU automatically. GPU acceleration is optional but recommended if available for better performance.

## What the Script Does

The script processes any image (JPG, PNG, etc.), detects and removes the background using a pre-trained AI model, and saves a transparent PNG output. It handles portraits, products, and complex scenes effectively.

## Installation

### 1. Python Requirements

Install: `pip install -r requirements.txt`

**Windows note:** Run Command Prompt or PowerShell **as Administrator** before pip installs to avoid permission errors.

### 2. Optional GPU Acceleration (NVIDIA only)

1. Install **CUDA Toolkit 12.x** (e.g., 12.6): Download from [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads?target_os=Windows).
2. Install **cuDNN 9.x** for CUDA 12.x: Register at [NVIDIA cuDNN](https://developer.nvidia.com/cudnn), download ZIP, extract, copy `bin/*.dll` to your CUDA `bin` folder (e.g., `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin`).
3. Add CUDA `bin` to system PATH.
4. Install GPU version: `pip install onnxruntime-gpu` (replaces CPU version).

Verify: `nvidia-smi` shows GPU, script runs without DLL errors.

CPU-only (default, no NVIDIA needed): `pip install onnxruntime`.

## Usage Examples

Save script as `remove_bg.py` and run from command line:

```bash
# Basic usage
python remove_bg.py input.jpg output.png

# Portrait
python remove_bg.py photo.jpg portrait_no_bg.png

# Product photo batch (run multiple times)
python remove_bg.py product1.jpg product1_no_bg.png
python remove_bg.py product2.jpg product2_no_bg.png

# From different directory
python remove_bg.py "C:\Photos\DSC00226.JPG" "me_no_bg.png"
```

**Windows:** Right-click PowerShell/Command Prompt → "Run as administrator", navigate to script folder, then execute.

## Troubleshooting

- **DLL errors** (cudnn64_9.dll): Install cuDNN or switch to CPU (`pip uninstall onnxruntime-gpu; pip install onnxruntime`).
- **Permission denied**: Run as Administrator.
- Works on Windows/Linux/macOS. Tested with Python 3.10+.

