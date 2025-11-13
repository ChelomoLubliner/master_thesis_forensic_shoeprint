# Contour Algorithm Pipeline

> **Computer Vision Component**: Advanced image processing for forensic shoeprint contour extraction and spatial analysis

This Python pipeline processes forensic shoeprint data to extract precise shoe contours using active contour algorithms and calculate spatial relationships between Randomly Acquired Characteristics (RACs) and shoe boundaries.

## 📋 Table of Contents

- [Overview](#overview)
- [Pipeline Architecture](#pipeline-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Module Descriptions](#module-descriptions)
- [Output Files](#output-files)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)

## 🔍 Overview

The contour algorithm pipeline transforms raw shoe contact data into refined contour representations suitable for statistical analysis. It employs:

- **Prototype-based noise filtering** for data cleaning
- **Active contour (snake) algorithms** for precise boundary detection
- **Multi-stage refinement** (coarse → fine) for accuracy
- **Spatial distance calculations** for RAC analysis

### Key Features

✅ Processes 387 forensic shoeprint samples
✅ Handles 307×395 pixel images
✅ Dual-snake active contour refinement
✅ Automated noise removal using prototype boundary
✅ Support for multiple datasets via configuration
✅ Progress tracking with tqdm

## 🏗️ Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTOUR PIPELINE FLOW                     │
└─────────────────────────────────────────────────────────────┘

Data Input: contacts_data.txt (387 shoes, 47 MB)
                    ↓
┌───────────────────────────────────────────────────────────┐
│ Step 1: create_files_shoes.py                             │
│ • Load raw contact data                                   │
│ • Generate frequency map across all shoes                 │
│ • Create prototype boundary (freq_min_18)                 │
│ • Apply active contour to prototype                       │
└───────────────────────────────────────────────────────────┘
                    ↓
        Outputs: list_matrices.npy, freq_min_18.npy
                    ↓
┌───────────────────────────────────────────────────────────┐
│ Step 2: contour.py                                         │
│ • Filter shoes using prototype boundary                   │
│ • Remove noise from individual shoes                      │
│ • Extract contour points                                  │
│ • Convert contours to binary matrices                     │
└───────────────────────────────────────────────────────────┘
                    ↓
              Outputs: list_contour.npy
                    ↓
┌───────────────────────────────────────────────────────────┐
│ Step 3: active_contour_snake.py                           │
│ • Initialize elliptical snake boundaries                  │
│ • Apply coarse refinement (large radius)                  │
│ • Apply fine refinement (small radius)                    │
│ • Extract extreme contour points                          │
└───────────────────────────────────────────────────────────┘
                    ↓
          Outputs: active-contour_all.npy
                    ↓
┌───────────────────────────────────────────────────────────┐
│ Step 4: distance_extremities.py                           │
│ • Calculate distances from RACs to contours               │
│ • Update location coordinates                             │
│ • Generate spatial relationship data                      │
└───────────────────────────────────────────────────────────┘
                    ↓
            Outputs: locations_new.csv
                    ↓
              Ready for R Pipeline

Note: Files like contact_with_locations.py, alphas_shape.py,
      convex_hull.py exist as alternative methods but are NOT
      called in the standard pipeline execution.
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4-8 GB RAM
- ~500 MB free disk space

### Setup

```bash
# Navigate to contour_algorithm directory
cd contour_algorithm

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

The `requirements.txt` includes:

```
numpy              # Array operations
pandas             # Data manipulation
plotly             # Interactive visualizations
matplotlib         # Static plotting
scipy              # Scientific computing
Pillow             # Image I/O
scikit-image       # Image processing algorithms
opencv-python      # Computer vision tools
tqdm               # Progress bars
alphashape         # Alpha shape analysis
```

## ⚙️ Configuration

### Dataset Selection

Edit `globals.py` to select dataset:

```python
# Use old dataset (default)
OLD_DATASET = True  # 387 shoes, 307×395 pixels

# Or use new dataset
OLD_DATASET = False  # 255×367 pixels
```

### Configuration Options

| Variable | Old Dataset | New Dataset |
|----------|-------------|-------------|
| `DATASET` | `contacts_data.txt` | `contacts_data_naomi_fast.txt` |
| `LOCATIONS` | `locations_data.csv` | `results_data_naomi_fast.txt` |
| `W, H` | 307, 395 | 255, 367 |
| `FOLDER` | `../images/` | `../images/` |

### Advanced Configuration

**Active Contour Parameters** (in `active_contour_snake.py`):
```python
# Snake initialization
center = (155, 200)  # Snake center point
radius = (90, 162)   # Ellipse radii (x, y)

# Coarse refinement
alpha_coarse = 0.015
beta_coarse = 10
gamma_coarse = 0.001

# Fine refinement
alpha_fine = 0.015
beta_fine = 10
gamma_fine = 0.001
```

## 💻 Usage

### Quick Start

```bash
# Ensure you're in contour_algorithm directory
cd contour_algorithm

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run complete pipeline
python main.py
```

### Step-by-Step Execution

```python
# Run individual modules (as executed by main.py)
import create_files_shoes
import contour
import active_contour_snake
import distance_extremities

# Execute pipeline steps
create_files_shoes.main()      # Step 1: Data preparation
contour.main()                  # Step 2: Contour extraction
active_contour_snake.main()     # Step 3: Active contour refinement
distance_extremities.main()     # Step 4: Distance calculations

# Note: contact_with_locations is NOT called in standard pipeline
```

### Verifying Setup

```bash
# Test imports
python -c "import numpy, pandas, plotly, scipy, skimage, cv2; print('All imports successful!')"

# Check data files exist
ls ../data/contacts_data.txt
ls ../data/locations_data.csv
```

## 📂 Module Descriptions

### 1. `create_files_shoes.py` - Data Preparation

**Purpose**: Initial data processing and prototype generation

**Key Functions**:
- `contacts_data()` - Loads raw 387-shoe dataset
- `superposed_pixels()` - Creates frequency map, generates prototype
- `active_contour_on_prototype()` - Applies active contour to prototype

**Outputs**:
- `list_matrices.npy` - Processed shoe contact matrices (387 samples)
- `freq_min_18.npy` - Prototype shoe boundary for noise filtering

**Runtime**: ~10-15 minutes

### 2. `contour.py` - Contour Extraction

**Purpose**: Noise removal and initial contour extraction

**Key Functions**:
- `remove_noise_get_contour()` - Complete noise removal and contour extraction workflow
- `save_new_contour_shoe()` - Converts contour points to binary matrix
- `scatter_plot_contour()` - Visualization of contour points

**Dependencies**:
- Requires: `list_matrices.npy`, `freq_min_18.npy`
- Imports: `remove_noise.py` - Uses `save_cleaned_shoes()`, `superpose_image_prototype()`
- Imports: `extreme_values_x_y.py` - Uses `get_contour()`

**Outputs**:
- `list_contour.npy` - Clean contour matrices for all shoes

**Runtime**: ~20-30 minutes

### 3. `active_contour_snake.py` - Active Contour Refinement

**Purpose**: Advanced contour refinement using snake algorithms

**Key Functions**:
- `active_contour_shoe()` - Applies dual-snake algorithm (coarse → fine)
- `init_snake()` - Initializes elliptical snake boundary
- `get_snake_image()` - Converts snake coordinates to image
- `extreme_values()` - Extracts extreme contour points

**Algorithm**:
1. Initialize elliptical snake around shoe
2. Apply coarse refinement with large radius
3. Apply fine refinement with small radius
4. Extract and save refined contours

**Outputs**:
- `active-contour_all.npy` - Refined active contour boundaries

**Runtime**: ~1.5-2.5 hours (most computationally intensive)

### 4. `distance_extremities.py` - Distance Calculations

**Purpose**: Calculate spatial distances between RACs and contours

**Key Functions**:
- Computes Euclidean distances from RAC points to boundaries
- Updates location coordinates with distance measurements
- Generates spatial relationship data for statistical analysis

**Outputs**:
- `locations_new.csv` - Location data with distance calculations

**Runtime**: ~15-20 minutes

### Supporting Modules (Actively Used)

**`remove_noise.py`** - Noise removal functions
- **Status**: ✅ Actively imported and used by `contour.py`
- **Functions**:
  - `save_cleaned_shoes()` - Applies prototype boundary mask to filter shoes
  - `superpose_image_prototype()` - Creates visualization of prototype overlay
- **Purpose**: Essential for noise filtering step in contour extraction

**`extreme_values_x_y.py`** - Contour extraction utilities
- **Status**: ✅ Actively imported by `contour.py` and `active_contour_snake.py`
- **Functions**: Extract extreme contour points and coordinate manipulation
- **Purpose**: Core utility for contour point processing

**`globals.py`** - Central configuration file
- **Status**: ✅ Used by all modules
- **Contains**: Dataset selection, dimensions, file paths

### Alternative Methods (Not Used in Main Pipeline)

**`contact_with_locations.py`** - Alternative RAC analysis module
- **Status**: ❌ Not imported anywhere, not called in main.py

**`alphas_shape.py`** - Alpha shape contour analysis
- **Status**: ❌ Not imported anywhere (alternative contour method)

**`convex_hull.py`** - Convex hull contour analysis
- **Status**: ❌ Not imported anywhere (alternative contour method)

## 📊 Output Files

| File | Size | Description |
|------|------|-------------|
| `list_matrices.npy` | ~50 MB | Raw processed shoe matrices |
| `freq_min_18.npy` | ~1 MB | Prototype boundary mask |
| `list_contour.npy` | ~40 MB | Initial extracted contours |
| `active-contour_all.npy` | ~30 MB | Refined active contours (numpy binary format) |
| `../data/contour_Active_Contour.txt` | ~30 MB | Same as above in text format (exported for R pipeline) |
| `locations_new.csv` | ~2 MB | RAC locations with distances |

**Note**: `active-contour_all.npy` and `contour_Active_Contour.txt` contain the same contour data in different formats (binary vs text).

**Total Storage Required**: ~500 MB (excluding optional visualizations)

## ⚡ Performance

### Runtime Characteristics

| Stage | Runtime | Bottleneck |
|-------|---------|------------|
| Data Preparation | 10-15 min | File I/O |
| Contour Extraction | 20-30 min | Image processing |
| Active Contour | 1.5-2.5 hrs | Snake iterations |
| Distance Calculations | 15-20 min | Distance computations |
| **Total** | **2-4 hours** | Active contour stage |

### Optimization Notes

- Image visualization is disabled for speed (`plot_img=False`)
- PNG/HTML generation is disabled in intermediate steps
- Progress bars via `tqdm` provide real-time feedback
- One shoe processed at a time (memory efficient)

### Hardware Recommendations

- **CPU**: Multi-core processor (parallelization possible)
- **RAM**: 4-8 GB minimum
- **Storage**: 2 GB free space recommended
- **OS**: Linux, macOS, or Windows

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'numpy'`
```bash
# Solution: Ensure virtual environment is activated and packages installed
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: `FileNotFoundError: [Errno 2] No such file or directory: '../data/contacts_data.txt'`
```bash
# Solution: Verify data files exist
ls ../data/
# Ensure you're running from contour_algorithm directory
pwd
```

**Issue**: Active contour stage is too slow
```python
# Solution: Reduce dataset size for testing in main.py
# Modify active_contour_snake.py to process fewer shoes:
for i in range(10):  # Process only first 10 shoes
    active_contour_shoe(i, list_contours)
```

**Issue**: Memory error during processing
```bash
# Solution: Increase available memory or process in batches
# Close other applications
# Consider processing shoes in smaller batches
```

### Validation

```bash
# Verify outputs were created
ls -lh list_matrices.npy
ls -lh freq_min_18.npy
ls -lh list_contour.npy
ls -lh active-contour_all.npy
ls -lh locations_new.csv

# Check file sizes are reasonable
du -h *.npy
```

## 📚 Additional Resources

- **[PIPELINE_DETAILS.md](PIPELINE_DETAILS.md)** - In-depth technical specifications
- **[Project README](../README.md)** - Complete project overview
- **[Statistical Model README](../statistical_model/README.md)** - R analysis documentation

## 🔗 Integration

This pipeline generates contour data consumed by the R statistical analysis pipeline. Key integration points:

- **Output**: `locations_new.csv` → Input for R pipeline
- **Coordinate System**: Consistent with R coordinate transformations
- **Data Format**: Compatible with R data processing scripts

**Next Step**: Run the statistical analysis pipeline in `../statistical_model/`

---

**For technical details and algorithm specifications, see [PIPELINE_DETAILS.md](PIPELINE_DETAILS.md)**
