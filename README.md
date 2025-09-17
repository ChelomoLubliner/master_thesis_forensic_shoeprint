# MSc. Thesis: Improving Spatial Modeling of Randomly Acquired Characteristics on Outsoles

This project analyzes forensic shoeprint data using computer vision techniques to model randomly acquired characteristics (RAC) on shoe outsoles.

This repository contains both the computer vision pipeline and the statistical analysis components working together in an integrated workflow.

## Project Overview

The project consists of two main components that work sequentially:

### 1. Computer Vision Pipeline (Python)
Located in `contour_algorithm/` - Processes raw shoeprint data:
1. **Data preparation** - Load and preprocess shoeprint matrices from contact data
2. **Contour extraction** - Extract shoe contours with noise removal
3. **Active contour refinement** - Apply snake algorithms for precise boundaries
4. **Distance calculations** - Compute spatial relationships and distances
5. **Contact analysis** - Generate final RAC location mappings

### 2. Statistical Analysis Pipeline (R)
Located in `statistical_model/` - Performs advanced statistical modeling:
1. **Case-control sampling** - Prepare data for statistical modeling
2. **Distance calculations** - Compute distances from RACs to contours
3. **Mixed-effects modeling** - Apply advanced statistical models with splines
4. **Results generation** - Create visualizations and model outputs
5. **Statistical validation** - Perform hypothesis testing and model validation

> **Integration**: The Python pipeline outputs processed data to `shared_data/locations_new.csv` which is consumed by the R statistical pipeline for analysis.

# Part 1: Python Computer Vision Pipeline

## Prerequisites

- Python 3.12+ (tested with 3.12.3)
- **bash/WSL environment** (Linux/macOS/Windows WSL)
- Virtual environment (.venv)

> **Note**: This project is designed to work only with bash/WSL environments. Windows CMD is not supported.

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd master_thesis_forensic_shoeprint
   ```

2. **Create and activate Python virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

This project uses **environment variables** configured through a `.env` file. 

**Default Configuration** (Old Dataset):
The `.env` file contains default values for the old shoes dataset:
- Dataset: `contacts_data.txt` (387 shoe samples, 307x395 pixels)
- Location data: `locations_data.csv`
- Snake parameters: center=(155,200), radius=(90,162)

The environment variables are automatically loaded from the `.env` file. No manual initialization required.

## Usage

### Run Python Pipeline

**Complete Python pipeline:**
```bash
cd contour_algorithm
source ../.venv/bin/activate
python main.py
deactivate
```

**Individual Python modules (can be run standalone):**
```bash
cd contour_algorithm
source ../.venv/bin/activate

# Run individual modules
python create_files_shoes.py
python contour.py
python active_contour_snake.py
python distance_extremities.py
python contact_with_locations.py

deactivate
```

**Alternative execution method:**
```bash
cd contour_algorithm
../.venv/bin/python main.py
```

**To use a different dataset**: Edit the `.env` file in the project root before running the pipeline.

## Python Pipeline Performance

- **Runtime**: 2-5 minutes for complete pipeline (387 shoes)
- **Memory**: 4-8GB RAM recommended
- **Storage**: Generates ~500MB of processed data

## Python Pipeline Output

- Processed shoeprint matrices (`shared_data/processing_data/list_matrices.npy`)
- Extracted contours (`shared_data/processing_data/list_contour.npy`)
- Active contour results (`shared_data/processing_data/active-contour_all.npy`)
- Cleaned shoe images (`Images/Cleaned_Shoes/`)
- Active contour visualizations (`Images/Active-contour/`)
- HTML distance plots (`Images_RAC_html/`)
- **Final output for R pipeline**: `shared_data/locations_new.csv`

## Python Pipeline Troubleshooting

**Common Issues:**
- **Import errors**: Ensure `.venv` is activated and all packages installed
- **Path errors**: Run from project root, use provided scripts
- **Memory issues**: Ensure 4-8GB RAM available
- **Permission errors**: Ensure write permissions for output directories

---

# Part 2: R Statistical Analysis Pipeline

## Prerequisites

- R 4.0+ (must be installed via bash)
- Required R packages (automatically installed via pipeline)
- RStudio (optional, for interactive development)
- **Python pipeline must be completed first** to generate required data files

## Installation

1. **Install R and pandoc (Required for Statistical Analysis)**
   ```bash
   # Update package list
   sudo apt update

   # Install R base and development packages
   sudo apt install r-base r-base-core r-base-dev

   # Install pandoc (required for R Markdown rendering)
   sudo apt install pandoc

   # Verify installations
   R --version
   Rscript --version
   pandoc --version
   ```

2. **Install R packages (within activated .venv for consistency)**
   ```bash
   # Activate Python virtual environment for consistency
   source .venv/bin/activate

   # Method A: Install to user library (Recommended - no sudo required)
   # Note: Package requirements have been simplified to avoid system dependency issues
   Rscript -e "install.packages(c('rmarkdown', 'knitr', 'ggplot2', 'dplyr', 'Matrix', 'splines', 'survival'), repos='https://cran.rstudio.com/', lib='~/R/library')"

   # Method B: If Method A fails, install system-wide (requires sudo)
   sudo Rscript -e "install.packages(c('rmarkdown', 'knitr', 'ggplot2', 'dplyr', 'Matrix', 'splines', 'survival'), repos='https://cran.rstudio.com/')"

   deactivate
   ```

## Configuration

The R pipeline uses **centralized configuration** through `statistical_model/config.R` and environment variables:

**Configuration Files:**
- `statistical_model/.env` - Environment variables (auto-loaded by config.R)
- `statistical_model/config.R` - Central configuration file loaded by all R scripts

**Key Configuration:**
```r
# All R scripts start with:
source("config.R")  # This loads all configuration and required packages
```


**What config.R provides:**
- Loads environment variables from `.env` file
- Installs and loads all required R packages automatically
- Sets up all paths and directories
- Provides utility functions (`aspix_x()`, `aspix_y()`)
- Validates data files exist
- Prints configuration summary

**No manual setup required** - just run the R scripts and config.R handles everything automatically.

## Usage

### Run R Statistical Analysis

**Method 1: Complete R pipeline (Recommended)**
```bash
# Activate Python virtual environment for consistency
source .venv/bin/activate

# Navigate to statistical model directory
cd statistical_model

# Run complete R pipeline via bash
Rscript run_analysis.R

# Deactivate when done
deactivate
```

**Method 2: Interactive R session**
```bash
# Activate Python virtual environment
source .venv/bin/activate

# Start interactive R session
R

# Inside R console:
# > setwd("/path/to/your/master_thesis_forensic_shoeprint/statistical_model")
# > # Replace /path/to/your/ with your actual project path
# > source("run_analysis.R")
# > main()
# > quit()

# Deactivate when done
deactivate
```

**Method 3: Run individual R Markdown files**

⚠️ **Prerequisites for Method 3:**
1. **pandoc must be installed** for R Markdown rendering:
   ```bash
   # Install pandoc (requires sudo access)
   sudo apt install pandoc

   # Verify pandoc installation
   pandoc --version
   ```

2. **First run may take 10-15 minutes** to install missing R packages to user library

**⚠️ IMPORTANT:** If you don't have sudo access or pandoc installation fails, use **Method 3b** instead (no pandoc required).

```bash
# Activate Python virtual environment
source .venv/bin/activate

cd statistical_model

# Run individual R Markdown files (first run installs packages automatically)
Rscript -e "rmarkdown::render('1_dataCC.Rmd')"
Rscript -e "rmarkdown::render('2_dataCC_distance.Rmd')"
Rscript -e "rmarkdown::render('3_calculate_shoe_distance.Rmd')"
Rscript -e "rmarkdown::render('4_random_effect_model_standardization_of_shoe.Rmd')"
Rscript -e "rmarkdown::render('5_output_and_results_standardization_of_shoe.Rmd')"
Rscript -e "rmarkdown::render('6_statistical_tests.Rmd')"

deactivate
```

**Alternative Method 3b: Run R scripts without rendering (no pandoc required)**
```bash
# Activate Python virtual environment
source .venv/bin/activate

cd statistical_model

# Run R scripts directly (generates results without HTML output)
Rscript -e "source('1_dataCC.Rmd')"
Rscript -e "source('2_dataCC_distance.Rmd')"
Rscript -e "source('3_calculate_shoe_distance.Rmd')"
Rscript -e "source('4_random_effect_model_standardization_of_shoe.Rmd')"
Rscript -e "source('5_output_and_results_standardization_of_shoe.Rmd')"
Rscript -e "source('6_statistical_tests.Rmd')"

deactivate
```

**Method 4: With output logging for debugging**
```bash
# Activate Python virtual environment
source .venv/bin/activate

# Run with output logging
cd statistical_model
Rscript run_analysis.R > analysis_output.log 2>&1

# Monitor progress in real-time (in another terminal)
tail -f statistical_model/analysis_output.log

# Deactivate when done
deactivate
```

**Method 5: Using RStudio (Alternative)**
```r
setwd("statistical_model")
source("run_analysis.R")
main()
```

## R Pipeline Performance

- **Runtime**: 15-30 minutes for complete analysis
- **Memory**: 4-8GB RAM required for large datasets
- **Storage**: Generates ~500MB of model outputs and visualizations

## R Pipeline Output

- Case-control datasets (`statistical_model/dataCC.csv`)
- Distance-augmented dataset (`statistical_model/dataCC_distance.csv`)
- Trained statistical models (`Images/Active_Contour/Saved_Models/`)
- Interactive visualizations and plots (HTML files)
- Model predictions and coefficients
- Statistical summary reports

## R Pipeline Troubleshooting

**Setup Issues:**
- **R not found**: Install R using `sudo apt install r-base r-base-core r-base-dev`
- **Rscript command not found**: Verify R installation with `R --version`
- **R package installation fails - Permission denied**: Use Method A from installation (installs to user library)
- **"lib is not writable" error**: This is the permission issue - use the user library method:
  ```bash
  source .venv/bin/activate
  Rscript -e "install.packages(c('ggplot2', 'dplyr'), repos='https://cran.rstudio.com/', lib='~/R/library')"
  deactivate
  ```

**Runtime Issues:**
- **R packages missing**: Re-run installation step 2 or use `source("config.R")` to auto-install
- **Data file not found**: Ensure Python pipeline completed successfully first
- **Path issues**: Check that `shared_data/locations_new.csv` exists
- **Permission errors**: Ensure write permissions for output directories
- **Memory issues**: Ensure 4-8GB RAM available, increase if needed
- **"pandoc version 1.12.3 or higher is required" error**: Install pandoc using `sudo apt install pandoc`

**Verification Commands:**
```bash
# Check if .venv is activated (should show (.venv) in prompt)
source .venv/bin/activate

# Check R installation
R --version

# Test R package availability (check user library)
Rscript -e ".libPaths('~/R/library'); installed.packages()[c('ggplot2', 'dplyr', 'lme4'), ]"

# Check available memory
free -h

# Monitor R process during execution
top -p $(pgrep R)

# Verify Python-R integration paths
ls -la shared_data/locations_new.csv

deactivate
```

**Important Notes:**
- R runs as a separate process from Python, but both access the same shared file system
- The `.venv` activation ensures consistent working directory and environment variables
- All file paths and outputs remain accessible to both Python and R components
- Always activate `.venv` before running any part of the pipeline for consistency
- **Python pipeline must be completed first** to generate required input data

---

# Complete Integrated Workflow

For users who want to run both pipelines sequentially:

```bash
# Step 1: Run Python Pipeline
source .venv/bin/activate
cd contour_algorithm
python main.py
cd ..

# Step 2: Run R Statistical Analysis
cd statistical_model
Rscript run_analysis.R
cd ..

deactivate
```

**One-liner execution:**
```bash
source .venv/bin/activate && cd contour_algorithm && python main.py && cd ../statistical_model && Rscript run_analysis.R && cd .. && deactivate
```

---

# Additional Information

## Detailed R Documentation

For comprehensive R statistical analysis documentation, see `statistical_model/README.md`

## Project Structure

```
├── Data/                           # Input datasets
│   ├── contacts_data.txt          # Raw shoeprint contact data
│   ├── contacts_data_naomi_fast.txt  # Alternative dataset
│   ├── locations_data.csv         # RAC location coordinates
│   └── results_data_naomi_fast.txt # Alternative location data
├── Images/                         # Image processing outputs
│   ├── Active_Contour/            # Active contour results
│   ├── Cleaned_Shoes/             # Processed shoe images
│   ├── Shoes_RAC/                 # RAC visualization images
│   └── RAC_html/                  # HTML distance plots (plotly visualizations)
├── shared_data/                    # Integration point between Python and R pipelines
│   ├── locations_new.csv         # Processed RAC data (Python → R)
│   ├── dataCC.csv                # Case-control data for statistical modeling
│   ├── dataCC_distance.csv       # Distance-augmented dataset
│   ├── all_cont.csv              # Contact surface data
│   ├── contour_algorithm.csv     # Contour points data
│   ├── processing_data/           # Intermediate processing files
│   │   ├── list_matrices.npy     # Processed shoeprint matrices
│   │   ├── list_contour.npy      # Extracted contours
│   │   ├── active-contour_all.npy # Active contour results
│   │   └── freq_min_18.*          # Prototype shoe data
│   ├── saved_models/             # Statistical models (R pipeline output)
│   └── final_results/             # Final analysis outputs
├── contour_algorithm/             # Python computer vision pipeline
│   ├── main.py                    # Main pipeline runner
│   ├── globals.py                 # Configuration management
│   ├── __init__.py                # Package initialization with path handling
│   ├── create_files_shoes.py      # Data preparation module
│   ├── contour.py                 # Contour extraction module
│   ├── active_contour_snake.py    # Active contour refinement
│   ├── distance_extremities.py    # Distance calculation module
│   ├── contact_with_locations.py  # RAC location analysis
│   ├── extreme_values_x_y.py      # Utility functions
│   └── test_paths.py              # Path validation testing
├── statistical_model/             # R statistical analysis pipeline
│   ├── README.md                  # R-specific documentation
│   ├── config.R                   # R configuration management
│   ├── run_analysis.R             # R pipeline runner
│   ├── .env.example               # R environment template
│   ├── 1_dataCC.Rmd              # Data preparation
│   ├── 2_dataCC_distance.Rmd     # Distance calculations
│   ├── 3_calculate_shoe_distance.Rmd # Individual shoe analysis
│   ├── 4_random_effect_model_standardization_of_shoe.Rmd # Statistical modeling
│   ├── 5_output_and_results_standardization_of_shoe.Rmd  # Results generation
│   ├── 6_statistical_tests.Rmd   # Model validation
│   └── convert_md_to_pdf.R        # Documentation export
├── .venv/                         # Python virtual environment
├── .env                           # Environment configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file (global documentation)
```

## Integration Notes

- **Data Flow**: Python pipeline → `shared_data/locations_new.csv` → R statistical analysis
- **Coordinate System**: Consistent coordinate transformations between both pipelines
- **File Permissions**: Ensure read/write access for shared directories
- **Memory Requirements**: 4-8GB RAM recommended for complete workflow

**Prerequisites for Integration:**
1. Complete Python pipeline first to generate required data files
2. Verify `shared_data/locations_new.csv` exists before running R analysis
3. Ensure sufficient storage space (~1GB total for both pipelines)