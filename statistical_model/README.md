# Statistical Analysis Pipeline

This directory contains the statistical analysis pipeline for forensic shoeprint RAC (Randomly Acquired Characteristics) analysis.

## Overview

The pipeline consists of 6 sequential R Markdown files that perform:

1. **Data preparation and case-control sampling** (`1_dataCC.Rmd`)
2. **Distance calculations to contours** (`2_dataCC_distance.Rmd`)
3. **Individual shoe distance analysis** (`3_calculate_shoe_distance.Rmd`)
4. **Statistical modeling with mixed-effects** (`4_random_effect_model_standardization_of_shoe.Rmd`)
5. **Results generation and visualization** (`5_output_and_results_standardization_of_shoe.Rmd`)
6. **Model validation and testing** (`6_statistical_tests.Rmd`)

## Prerequisites

### Required Software
- **R** (version 4.0 or higher)
- **RStudio** (recommended)

### Required R Packages
The pipeline automatically installs missing packages. Required packages include:
- `ggplot2`, `dplyr`, `Matrix`, `spam`
- `lme4`, `splines`, `survival`, `smoothie`
- `plotly`, `rgl`, `fields`, `imager`
- `rmarkdown`, `knitr`

## Configuration

### Method 1: Using Configuration File (Recommended)

All parameters are centralized in `config.R`. Key settings:

```r
# Algorithm and model selection
CONTOUR_ALGORITHM <- 'Active_Contour'  # or 'Convex'
MODEL_FEATURE <- 'NEW_X_NS_XY'

# Shoe parameters
COL_SHOE <- 307  # Shoe width in pixels
ROW_SHOE <- 395  # Shoe height in pixels
NUM_SHOE <- 387  # Total number of shoes

# Data paths (automatically configured)
CONTACTS_DATA_FILE <- "../Data/contacts_data.txt"
LOCATIONS_DATA_FILE <- "../Data/locations_data.csv"
```

### Method 2: Environment Variables

Set environment variables before running:

```bash
export R_CONTOUR_ALGORITHM="Active_Contour"
export R_MODEL_FEATURE="NEW_X_NS_XY"
export R_ROOT_PATH="../"
```

## Usage

### Quick Start

**Method 1: Run complete pipeline**
```bash
cd statistical_model
Rscript run_analysis.R
```

**Method 2: Interactive execution**
```r
# In R/RStudio
setwd("statistical_model")
source("run_analysis.R")
main()
```

**Method 3: Step-by-step execution**
```r
# Load configuration
source("config.R")

# Run individual steps
rmarkdown::render("1_dataCC.Rmd")
rmarkdown::render("2_dataCC_distance.Rmd")
# ... continue with remaining files
```

### Advanced Configuration

**For different datasets:**
```r
# Edit config.R before running
CONTOUR_ALGORITHM <- 'Convex'        # Change algorithm
MODEL_FEATURE <- 'NS_XY'            # Change model type
NUM_SHOE <- 200                     # Different dataset size
```

**For specific shoe analysis:**
```r
# In 3_calculate_shoe_distance.Rmd
IMAGE_NUMBER <- 171  # Analyze specific shoe
```

## Output

The pipeline generates:

### Data Files
- `dataCC.csv` - Case-control dataset
- `all_cont.csv` - Cumulative contact surfaces
- `dataCC_distance.csv` - Distance-augmented dataset

### Model Files
- `*.rds` files in `Active_Contour/Saved_Models/` - Trained models
- Model predictions and coefficients

### Visualizations
- Interactive plots (HTML)
- 3D surface plots
- Statistical summary plots

## File Structure

```
statistical_model/
├── config.R                    # Central configuration
├── run_analysis.R              # Pipeline runner
├── README.md                   # This file
├── 1_dataCC.Rmd               # Data preparation
├── 2_dataCC_distance.Rmd      # Distance calculations
├── 3_calculate_shoe_distance.Rmd  # Individual shoe analysis
├── 4_random_effect_model_standardization_of_shoe.Rmd  # Modeling
├── 5_output_and_results_standardization_of_shoe.Rmd   # Results
├── 6_statistical_tests.Rmd    # Validation
└── convert_md_to_pdf.R         # Documentation export
```

## Performance

- **Runtime**: 15-30 minutes for complete pipeline
- **Memory**: Requires 4-8GB RAM for large datasets
- **Storage**: Generates ~500MB of output files

## Troubleshooting

### Common Issues

**Missing packages:**
```r
# Install all required packages
source("config.R")  # Automatically installs missing packages
```

**Data file not found:**
```
Error: Required data file not found: ../Data/contacts_data.txt
```
- Ensure the contour algorithm pipeline has been run first
- Check that data files exist in the `../Data/` directory

**Path issues:**
```r
# Verify paths in config.R
print_config()  # Shows current configuration
validate_data_files()  # Checks file existence
```

**Memory issues:**
```r
# For large datasets, increase memory limit
memory.limit(size = 8000)  # Windows
```

### Model Selection

**Available algorithms:**
- `Active_Contour` - Advanced boundary detection (recommended)
- `Convex` - Faster geometric approach

**Available models:**
- `NEW_X_NS_XY` - Advanced spline model (recommended)
- `NS_XY` - Standard spline model
- `NS_HORIZ` - Horizontal distance model
- `NS_MIN` - Minimum distance model

## Quality Assurance

The pipeline includes:
- ✅ Automatic package installation
- ✅ Data file validation
- ✅ Error handling and reporting
- ✅ Reproducible results (fixed seed)
- ✅ Progress tracking
- ✅ Output validation

## Integration

This statistical pipeline integrates with:
- **Python contour algorithm** - Processes shoe images and generates contour data
- **Shared data directory** - Uses outputs from the contour algorithm
- **Common coordinate system** - Consistent with image processing pipeline