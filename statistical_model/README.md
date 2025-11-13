# Statistical Analysis Pipeline

> **R-based mixed-effects modeling for forensic shoeprint RAC intensity analysis**

Comprehensive statistical pipeline analyzing Randomly Acquired Characteristics (RACs) spatial distribution across 387 forensic shoeprint samples using advanced mixed-effects models with natural cubic splines.

## 📋 Table of Contents

- [Overview](#overview)
- [Pipeline Architecture](#pipeline-architecture)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Pipeline Components](#pipeline-components)
- [Output Files](#output-files)
- [Model Types](#model-types)
- [Troubleshooting](#troubleshooting)

## 🔍 Overview

This pipeline implements the statistical methodology for RAC spatial modeling:

**Input**: Python pipeline outputs (`contacts_data.txt`, `locations_data.csv`, `contour_Active_Contour.txt`)

**Process**: Case-control sampling → Distance calculations → Mixed-effects modeling → Validation

**Output**: Trained models (.rds), intensity heatmaps (PDF), validation statistics

### Key Features

✅ **5 sequential R Markdown files** (strict execution order)
✅ **Case-control design** - All RACs + 20 random controls per shoe
✅ **Mixed-effects models** - Random intercepts per shoe (387 shoes)
✅ **Natural cubic splines** - Smooth spatial surface modeling
✅ **Multiple algorithms** - Active Contour vs Convex comparison
✅ **Reproducible** - Fixed seed (313) across pipeline

## 🏗️ Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            STATISTICAL ANALYSIS PIPELINE                     │
│                  (5-step sequential)                         │
└─────────────────────────────────────────────────────────────┘

Python Outputs → dataCC_1.Rmd → dataCC_distance_2.Rmd
                      ↓              ↓
                 dataCC.csv    dataCC_distance.csv
                                     ↓
                      re_model_shoe_std_3.Rmd
                                     ↓
                         Models (.rds files)
                      /                    \
    shoe_std_results_4.Rmd    statistical_tests_5.Rmd
             ↓                           ↓
        Heatmaps (PDF)            Validation Results
```

## 🚀 Quick Start

### Prerequisites

- **R** 4.0+ (tested with 4.3.x)
- **RStudio** (recommended for interactive execution)
- **Memory**: 4-8 GB RAM
- **Python pipeline completed** (generates required input files)

### Installation

**Install required R packages**:
```r
install.packages(c("lme4", "splines", "ggplot2", "dplyr",
                   "Matrix", "spam", "plotly", "data.table"))
```

### Running the Pipeline

**Method 1: Step-by-Step (Recommended)**
```r
# In RStudio, open and knit each file in order:
rmarkdown::render("dataCC_1.Rmd")
rmarkdown::render("dataCC_distance_2.Rmd")
rmarkdown::render("re_model_shoe_std_3.Rmd")
rmarkdown::render("shoe_std_results_4.Rmd")
rmarkdown::render("statistical_tests_5.Rmd")
```

**Method 2: Run Code Chunks**
```r
# Open each .Rmd in RStudio
# Run chunks sequentially: Ctrl+Alt+R (Windows) / Cmd+Option+R (Mac)
# Monitor progress in console
```

**⚠️ Important**: Files MUST be run in order (1→2→3→4→5)

### Verify Prerequisites

```r
# Check input files exist
file.exists("../data/contacts_data.txt")
file.exists("../data/locations_data.csv")
file.exists("../data/contour_Active_Contour.txt")

# Check config loads
source("config.R")
print(paste("ROOT_PATH:", ROOT_PATH))
print(paste("CONTOUR_ALGORITHM:", CONTOUR_ALGORITHM))
```

## ⚙️ Configuration

### `config.R` - Central Configuration

```r
ROOT_PATH <- "..."                          # Auto-detected project root
CONTOUR_ALGORITHM <- "Active_Contour"       # or "Convex"
IMAGE_NUMBER <- "171"                       # Specific shoe for visualization
MODEL_FEATURE <- "NEW_X_NS_XY_RELATIVE"     # Model type
```

### Available Algorithms

| Algorithm | Description | File Used |
|-----------|-------------|-----------|
| `Active_Contour` | Snake-based boundary (Python output) | `contour_Active_Contour.txt` |
| `Convex` | Convex hull approach | `contour_Convex.txt` |

### Available Models

| Model Feature | Description | Covariates |
|--------------|-------------|------------|
| `NEW_X_NS_XY_RELATIVE` | **Recommended** - Standardized X with splines | new_x, y (natural cubic splines 3×5) |
| `NS_XY_RELATIVE` | Baseline - Standard coordinates | x, y (natural cubic splines 3×5) |
| `NS_HORIZ` | Horizontal distance only | horiz_dist (natural splines) |
| `NS_MIN` | Minimum distance only | min_dist (natural splines) |
| `EMPTY_MODEL` | Null model | Random intercept only |

**Note on Model File Naming**: Model files are saved with the `_RELATIVE` suffix (e.g., `NEW_X_NS_XY_RELATIVE.rds`). The code in `re_model_shoe_std_3.Rmd` automatically appends `_RELATIVE` when saving (see line 237).

**Recommendation**: Set `MODEL_FEATURE <- "NEW_X_NS_XY"` in config.R (without `_RELATIVE`), and the code will automatically create `NEW_X_NS_XY_RELATIVE.rds`. Alternatively, you can set `MODEL_FEATURE <- "NEW_X_NS_XY_RELATIVE"` to match the actual saved filename.

## 📂 Pipeline Components

### Step 1: `dataCC_1.Rmd` - Data Preparation

**Purpose**: Load data, remove police stamps, perform case-control sampling (all RACs + 20 controls/shoe)

**Outputs**: `dataCC.csv` (740 KB), `all_cont.csv` (240 KB)
**Runtime**: 2-3 minutes

---

### Step 2: `dataCC_distance_2.Rmd` - Distance Calculations

**Purpose**: Calculate minimum Euclidean and horizontal distances from each point to shoe contour

**Outputs**: `dataset/dataCC_distance.csv` (1.6 MB)
**Runtime**: 3-5 minutes

---

### Step 3: `re_model_shoe_std_3.Rmd` - Statistical Modeling

**Purpose**: Fit binomial GLMM with natural cubic splines and random intercepts per shoe

**Key Model**: `n_Acc ~ ns(new_x, knots=3):ns(y, knots=5) + (1|shoe)`

**Outputs**: `NEW_X_NS_XY_RELATIVE.rds` (10.4 MB), `NS_XY_RELATIVE.rds` (9.1 MB)
**Runtime**: 5-10 minutes

---

### Step 4: `shoe_std_results_4.Rmd` - Results & Visualization

**Purpose**: Generate intensity predictions on 121,265-point grid and create heatmap PDFs for prototype and target shoes

**Outputs**: PDF heatmaps in `model_images/`
**Runtime**: 3-5 minutes

---

### Step 5: `statistical_tests_5.Rmd` - Model Validation

**Purpose**: Perform likelihood ratio tests comparing models

**Outputs**: Console output with LRT statistics (Chi-square, df, p-values)
**Runtime**: 2-4 minutes

---

**For detailed technical specifications, see [PIPELINE_DETAILS.md](PIPELINE_DETAILS.md)**

## 📊 Output Files

### Data Files

| File | Size | Description |
|------|------|-------------|
| `../data/dataCC.csv` | 740 KB | Case-control dataset (~8,000 rows) |
| `../data/all_cont.csv` | 240 KB | Cumulative contact surface |
| `dataset/dataCC_distance.csv` | 1.6 MB | With Euclidean & horizontal distances |
| `dataset/dataCC_distance_part4.csv` | 1.9 MB | With new_x standardization |

### Model Files

| File | Size | Description |
|------|------|-------------|
| `saved_models/NEW_X_NS_XY_RELATIVE.rds` | 10.4 MB | Advanced spline model |
| `saved_models/NS_XY_RELATIVE.rds` | 9.1 MB | Baseline spline model |

### Visualizations

| File | Description |
|------|-------------|
| `model_images/*_SHOE.pdf` | Intensity on shoe contact surface |
| `model_images/*_CONTOUR.pdf` | Intensity on contour boundary |
| `model_images/*_171_NEW_SHOE.pdf` | Adapted to specific shoe |

## ⚡ Performance

**Total Runtime**: 15-30 minutes | **Memory**: 4-8 GB RAM | **Output**: ~25 MB

See [PIPELINE_DETAILS.md](PIPELINE_DETAILS.md) for detailed performance metrics and model specifications.

## 🐛 Troubleshooting

**Missing Input Files**
```
Error: cannot open file '../data/contacts_data.txt'
```
**Solution**: Run Python pipeline first (`cd ../contour_algorithm && python main.py`)

**Memory Error**
```
Error: cannot allocate vector of size...
```
**Solution**: `memory.limit(size = 8000)` (Windows) or reduce dataset for testing

**Package Not Found**
```
Error: there is no package called 'lme4'
```
**Solution**: Install packages as shown in Installation section above

---

For detailed troubleshooting, model specifications, and technical details, see **[PIPELINE_DETAILS.md](PIPELINE_DETAILS.md)**

## 📚 Additional Resources

- **[PIPELINE_DETAILS.md](PIPELINE_DETAILS.md)** - Complete technical specification
- **[../README.md](../README.md)** - Project overview
- **[../contour_algorithm/README.md](../contour_algorithm/README.md)** - Python pipeline

## 🔗 Integration with Python Pipeline

**Data Flow**:
```
Python creates:
  ../data/contacts_data.txt
  ../data/locations_data.csv
  ../data/contour_Active_Contour.txt
         ↓
R reads these files in Step 1 & 2
```

**Prerequisites**:
1. ✅ Python pipeline completed successfully
2. ✅ Files exist in `../data/` directory
3. ✅ File sizes reasonable (~45 MB contacts_data.txt)

**Coordinate Consistency**:
- Python and R use same pixel → coordinate mapping
- R functions `aspix_x()` and `aspix_y()` invert Python transformations
- Consistent reference: (0,0) at top-left, X∈[-0.25,0.25], Y∈[-0.5,0.5]

---

**For detailed algorithm specifications and technical documentation, see [PIPELINE_DETAILS.md](PIPELINE_DETAILS.md)**

**Last Updated**: November 2024
