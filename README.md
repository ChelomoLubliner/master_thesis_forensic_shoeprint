# MSc. Thesis: Improving Spatial Modeling of Randomly Acquired Characteristics on Outsoles

This project analyzes forensic shoeprint data using computer vision techniques to model randomly acquired characteristics (RAC) on shoe outsoles.

This repository contains both the computer vision pipeline and the statistical analysis components.

## Project Overview

The project consists of two main components:

### Computer Vision Pipeline (Python)
1. **Data preparation** - Load and preprocess shoeprint matrices
2. **Contour extraction** - Extract shoe contours with noise removal
3. **Active contour refinement** - Apply snake algorithms for precise boundaries
4. **Distance calculations** - Compute spatial relationships
5. **Contact analysis** - Generate final RAC location mappings

### Statistical Analysis Pipeline (R)
1. **Case-control sampling** - Prepare data for statistical modeling
2. **Distance calculations** - Compute distances from RACs to contours
3. **Mixed-effects modeling** - Apply advanced statistical models with splines
4. **Results generation** - Create visualizations and model outputs
5. **Statistical validation** - Perform hypothesis testing and model validation

## Setup Instructions

### Prerequisites
- Python 3.7+
- **bash/WSL environment** (Linux/macOS/Windows WSL)
- Virtual environment (recommended)

> **Note**: This project is designed to work only with bash/WSL environments. Windows CMD is not supported.

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd master_thesis_forensic_shoeprint
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

This project uses **environment variables** configured through a `.env` file. 

**Default Configuration** (Old Dataset):
The `.env` file contains default values for the old shoes dataset:
- Dataset: `contacts_data.txt` (387 shoe samples, 307x395 pixels)
- Location data: `locations_data.csv`
- Snake parameters: center=(155,200), radius=(90,162)

The environment variables are automatically loaded from the `.env` file. No manual initialization required.

**Method 1: Direct execution (Recommended)**:
```bash
cd contour_algorithm
../.venv/bin/python main.py
```

**Method 2: Activate virtual environment first**:
```bash
# Activate virtual environment
source .venv/bin/activate
# Navigate and run
cd contour_algorithm
python main.py
```

**To use a different dataset**: Simply edit the `.env` file in the project root with the desired configuration values before running the pipeline.

The pipeline runs the following steps automatically:
1. **Data preparation** - Loads and processes shoe matrices from `../Data/contacts_data.txt`
2. **Contour extraction** - Extracts contours with noise removal
3. **Active contour refinement** - Applies snake algorithms
4. **Distance calculations** - Computes spatial relationships

## Performance Notes

- **Runtime**: Complete pipeline takes several hours
- **Memory**: Requires sufficient RAM for large image datasets
- **Storage**: Generates essential `.npy` files in `Saved/` directory
- **Optimization**: Image generation for visualization has been disabled for faster processing

## Output

The pipeline generates:
- Processed shoeprint matrices (`list_matrices.npy`)
- Extracted contours (`list_contour.npy`)
- Active contour results (`active-contour_all.npy`)
- Final RAC analysis results (`locations_new.csv`)

## Project Structure

```
├── Data/                    # Input datasets
├── Images/                  # Image directories and outputs
│   ├── Active-contour/     # Active contour results
│   ├── Cleaned_Shoes/      # Processed shoe images
│   ├── Saved/              # Generated .npy files
│   └── ...                 # Other processing outputs
├── contour_algorithm/       # Main processing pipeline
│   ├── main.py             # Main pipeline runner
│   ├── globals.py          # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   └── *.py                # Processing modules
├── .env                    # Environment configuration
└── README.md               # This file
```

For detailed implementation information, refer to the Code Details document.