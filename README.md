# Forensic Shoeprint RAC Analysis

> **MSc Thesis Project**: Improving spatial modeling of randomly acquired characteristics (RACs) on shoe outsoles

A comprehensive forensic analysis system combining computer vision and statistical modeling to analyze and predict the spatial distribution of Randomly Acquired Characteristics in forensic shoeprint evidence.

**Academic Research**
This project is part of academic research by **Dr. Naomi Kaplan Damary** from the Hebrew University of Jerusalem. This master's thesis was completed under the supervision of **Prof. Micha Mandel** from the Hebrew University of Jerusalem.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Workflow](#pipeline-workflow)
- [Output Files](#output-files)
- [Documentation](#documentation)
- [Technical Specifications](#technical-specifications)

## 🔍 Overview

This project analyzes 387 forensic shoeprint samples to model the spatial distribution of Randomly Acquired Characteristics (RACs) - unique wear patterns and damage on shoe outsoles that are crucial for forensic identification.

### Two-Component Architecture

1. **Contour Algorithm Pipeline (Python)**
   - Advanced image processing for shoe contour extraction
   - Active contour refinement using snake algorithms
   - Spatial distance calculations from RACs to shoe boundaries

2. **Statistical Analysis Pipeline (R)**
   - Mixed-effects modeling with random shoe-level effects
   - Natural cubic spline surface modeling
   - Comparative analysis of contour detection methods
   - Forensic-grade statistical validation

## 📁 Project Structure

```
master_thesis_forensic_shoeprint/
│
├── contour_algorithm/          # Python image processing pipeline
│   ├── main.py                 # Pipeline orchestrator (4 modules)
│   ├── create_files_shoes.py   # Step 1: Data preparation
│   ├── contour.py              # Step 2: Contour extraction
│   ├── active_contour_snake.py # Step 3: Active contour refinement
│   ├── distance_extremities.py # Step 4: Distance calculations
│   ├── remove_noise.py         # Supporting: Noise removal (used by contour.py)
│   ├── extreme_values_x_y.py   # Supporting: Contour utilities
│   ├── globals.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── README.md               # Component documentation
│   └── PIPELINE_DETAILS.md     # Technical details
│
├── statistical_model/          # R statistical analysis pipeline
│   ├── dataCC_1.Rmd           # Data preparation & sampling
│   ├── dataCC_distance_2.Rmd  # Distance calculations
│   ├── re_model_shoe_std_3.Rmd # Statistical modeling
│   ├── shoe_std_results_4.Rmd # Results generation
│   ├── statistical_tests_5.Rmd # Validation tests
│   └── README.md               # Component documentation
│
├── data/                       # Data files (input + pipeline outputs)
│   ├── contacts_data.txt       # [Input] Raw shoe contact data (387 shoes, 47 MB)
│   ├── locations_data.csv      # [Input] RAC location coordinates
│   ├── contour_Active_Contour.txt  # [Python→R] Active contour boundaries (text format)
│   ├── contour_Convex.txt      # [Python→R] Alternative contour method
│   ├── dataCC.csv              # [R output] Case-control dataset (740 KB)
│   └── all_cont.csv            # [R output] Cumulative contact surface (240 KB)
│
├── images/                     # Output visualizations
│
└── README.md                   # This file
```

## 🚀 Quick Start

### Complete Pipeline Execution

**Windows CMD:**
```cmd
REM 1. Run Python contour analysis
cd contour_algorithm
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

REM 2. Run R statistical analysis
cd ..\statistical_model
REM Outputs from parts 1, 2, and contour_algorithm are already saved
REM You can directly run files 3 and 4: re_model_shoe_std_3.Rmd and shoe_std_results_4.Rmd
REM In RStudio, run: rmarkdown::render("re_model_shoe_std_3.Rmd")
REM Then run: rmarkdown::render("shoe_std_results_4.Rmd")
```

**Git Bash / WSL / Linux:**
```bash
# 1. Run Python contour analysis
cd contour_algorithm
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# 2. Run R statistical analysis
cd ../statistical_model
# Outputs from parts 1, 2, and contour_algorithm are already saved
# You can directly run files 3 and 4: re_model_shoe_std_3.Rmd and shoe_std_results_4.Rmd
# In RStudio, run: rmarkdown::render("re_model_shoe_std_3.Rmd")
# Then run: rmarkdown::render("shoe_std_results_4.Rmd")
```

## 📦 Prerequisites

### Python Component
- **Python** 3.8+
- **Virtual environment** (recommended)
- **Memory**: 4-8 GB RAM

### R Component
- **R** 4.0+
- **RStudio** (recommended)
- **Memory**: 4-8 GB RAM

## 🔧 Installation

### Python Environment Setup

```bash
cd contour_algorithm

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Python Packages Installed:**
- `numpy`, `pandas` - Data manipulation
- `matplotlib`, `plotly` - Visualization
- `scipy`, `scikit-image` - Image processing
- `opencv-python`, `Pillow` - Image handling
- `alphashape` - Alpha shape analysis
- `tqdm` - Progress tracking

### R Environment Setup

```r
# Install required R packages
install.packages(c("ggplot2", "dplyr", "lme4", "splines",
                   "Matrix", "spam", "plotly", "fields",
                   "imager", "lmtest", "data.table", "rgl"))
```

## 💻 Usage

### Configuration

**Python Configuration (`contour_algorithm/globals.py`):**
```python
OLD_DATASET = True  # Use old dataset (387 shoes, 307×395 pixels)
# OLD_DATASET = False  # Use new dataset (255×367 pixels)
```

**R Configuration (`statistical_model/config.R`):**
```r
CONTOUR_ALGORITHM <- "Active_Contour"       # or "Convex"
MODEL_FEATURE <- "NEW_X_NS_XY_RELATIVE"     # Model type
IMAGE_NUMBER <- "171"                        # Shoe for visualization
# ROOT_PATH is auto-detected
```

### Running the Pipeline

#### Python Contour Analysis

```bash
cd contour_algorithm
python main.py
```

**Pipeline Steps Executed:**
1. Data preparation and prototype generation
2. Contour extraction with noise removal
3. Active contour refinement (snake algorithms)

**Runtime**: 2-4 hours for complete dataset (387 shoes)

#### R Statistical Analysis

**Interactive Step-by-Step Execution:**
```r
# In RStudio
setwd("statistical_model")
rmarkdown::render("dataCC_1.Rmd")
rmarkdown::render("dataCC_distance_2.Rmd")
rmarkdown::render("re_model_shoe_std_3.Rmd")
rmarkdown::render("shoe_std_results_4.Rmd")
rmarkdown::render("statistical_tests_5.Rmd")
```

**Runtime**: 15-30 minutes for complete pipeline

## 🔄 Pipeline Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                   PYTHON CONTOUR PIPELINE                    │
│                    (4-module pipeline)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
    contacts_data.txt (387 shoes, 307×395 pixels)
                              ↓
         [1] create_files_shoes.py
                              ↓
         list_matrices.npy, freq_min_18.npy
                              ↓
              [2] contour.py
                              ↓
            list_contour.npy
                              ↓
         [3] active_contour_snake.py
                              ↓
         active-contour_all.npy
                              ↓
         [4] distance_extremities.py
                              ↓
           locations_new.csv
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  R STATISTICAL PIPELINE                      │
│                    (5-module pipeline)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
            [1] dataCC_1.Rmd
                              ↓
       dataCC.csv, all_cont.csv
                              ↓
        [2] dataCC_distance_2.Rmd
                              ↓
         dataCC_distance.csv
                              ↓
       [3] re_model_shoe_std_3.Rmd
                              ↓
        Trained models (*.rds)
                              ↓
       [4] shoe_std_results_4.Rmd
                              ↓
     Results, predictions, visualizations
                              ↓
      [5] statistical_tests_5.Rmd
                              ↓
        Statistical validation
```

## 📊 Output Files

### Python Outputs

| File | Description | Size |
|------|-------------|------|
| `list_matrices.npy` | Processed shoe contact matrices | ~50 MB |
| `freq_min_18.npy` | Prototype shoe boundary | ~1 MB |
| `list_contour.npy` | Cleaned contour matrices | ~40 MB |
| `active-contour_all.npy` | Refined active contours | ~30 MB |

### R Outputs

| File | Description |
|------|-------------|
| `dataCC.csv` | Case-control dataset |
| `all_cont.csv` | Cumulative contact surfaces |
| `dataCC_distance.csv` | Distance-augmented dataset |
| `Active_Contour/Saved_Models/*.rds` | Trained statistical models |
| `*.html` | Interactive visualizations |
| `*.png` | Statistical plots |

## 📚 Documentation

- **[Contour Algorithm README](contour_algorithm/README.md)** - Detailed Python pipeline documentation
- **[Pipeline Technical Details](contour_algorithm/PIPELINE_DETAILS.md)** - In-depth technical specifications
- **[Statistical Model README](statistical_model/README.md)** - R analysis documentation
- **[Claude Memory](claude_memory.md)** - Complete project knowledge base

## 🔬 Technical Specifications

### Dataset Characteristics
- **Sample Size**: 387 forensic shoeprint samples
- **Image Dimensions**: 307 × 395 pixels (W × H)
- **Coordinate System**: X: [-0.25, 0.25], Y: [-0.5, 0.5]
- **RAC Distribution**: 386 shoes with RACs (shoe 127 excluded)
- **Control Sampling**: 20 random controls per shoe

### Algorithms

**Contour Detection:**
- Active Contour (Snake Algorithm) - Primary method
- Convex Hull - Alternative method
- Alpha Shape - Experimental method

**Statistical Models:**
- NEW_X_NS_XY - Advanced spline model with X,Y coordinates
- NS_XY - Natural splines with coordinates
- NS_HORIZ - Splines with horizontal distance
- NS_MIN - Splines with minimum distance

### Performance Metrics
- **Python Pipeline**: 2-4 hours (complete dataset)
- **R Pipeline**: 15-30 minutes
- **Memory Requirements**: 4-8 GB RAM
- **Storage**: ~500 MB total output

## 🤝 Related Work

Research of Naomi Kaplan: https://arxiv.org/abs/1912.08272

## 📝 Citation

```bibtex
@mastersthesis{forensic_shoeprint_rac,
  title={Improving Spatial Modeling of Randomly Acquired Characteristics on Outsoles},
  author={Naomi Kaplan Damary},
  year={2024},
  school={Hebrew University of Jerusalem},
  type={MSc Thesis},
  supervisor={Prof. Micha Mandel}
}
```

## 📄 License

This project is part of academic research. Please contact the author for usage permissions.

---

**Last Updated**: November 2024
