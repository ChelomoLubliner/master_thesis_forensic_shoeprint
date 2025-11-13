# Claude Memory: Complete Shoe RAC Analysis Project

## Project Overview
This is a comprehensive forensic analysis project combining computer vision and statistical modeling for analyzing Randomly Acquired Characteristics (RACs) in shoe prints. The project consists of two main components:
1. **Contour Algorithm Pipeline** (Python) - Image processing and contour extraction
2. **Statistical Model** (R/RMarkdown) - Advanced statistical analysis and modeling

---

# Part 1: Computer Vision Pipeline (Python)

## Core Processing Steps (4-Module Pipeline)
1. **Data preparation** (create_files_shoes.py) - Load and preprocess shoeprint matrices, generate prototype
2. **Contour extraction** (contour.py) - Extract shoe contours with noise removal
3. **Active contour refinement** (active_contour_snake.py) - Apply snake algorithms for precise boundaries
4. **Distance calculations** (distance_extremities.py) - Compute spatial relationships, generate locations_new.csv

**Note**: The pipeline executes 4 modules. Files like `contact_with_locations.py`, `alphas_shape.py`, and `convex_hull.py` exist as alternative/legacy methods but are NOT called in main.py.

## Key Files (contour_algorithm/)

**Active Pipeline Modules (called by main.py):**
- `main.py` - Main pipeline orchestrator
- `create_files_shoes.py` - Step 1: Data preparation and prototype generation
- `contour.py` - Step 2: Contour extraction with noise removal
- `active_contour_snake.py` - Step 3: Active contour refinement using snake algorithms
- `distance_extremities.py` - Step 4: Distance calculations and locations_new.csv generation

**Supporting Files (Actively Used):**
- `remove_noise.py` - Noise removal functions (imported and used by contour.py)
- `extreme_values_x_y.py` - Utility functions for contour point extraction
- `globals.py` - Configuration settings (OLD_DATASET flag, dimensions, paths)
- `requirements.txt` - Python package dependencies

**Alternative/Legacy Modules (NOT used in main pipeline):**
- `contact_with_locations.py` - Alternative RAC analysis (not called)
- `alphas_shape.py` - Alpha shape analysis (alternative method, not used)
- `convex_hull.py` - Convex hull analysis (alternative method, not used)

## Configuration (globals.py)
- **Dataset Selection**: `OLD_DATASET = True/False` flag
  - Old dataset: `contacts_data.txt`, 387 shoes, 307×395 pixels
  - New dataset: `contacts_data_naomi_fast.txt`, 255×367 pixels
- **Dimensions**: W=307, H=395 (COL, ROW) for old dataset
- **Snake parameters**: center=(155,200), radius=(90,162)
- **Data paths**: `../data/`, `../images/`
- **Locations file**: `locations_data.csv`

## Python Dependencies (requirements.txt)
- numpy, pandas - Data manipulation
- matplotlib, plotly - Visualization
- scipy, scikit-image - Image processing
- Pillow, opencv-python - Image handling
- alphashape - Alpha shape computation
- tqdm - Progress bars

---

# Part 2: Statistical Analysis (R)

## Statistical Pipeline Components

### 1. Data Processing Pipeline (`dataCC_1.Rmd`)
- **Purpose**: Initial data cleaning and case-control sampling
- **Key Functions**:
  - `aspix_x()` and `aspix_y()`: Convert coordinates to pixel positions
  - Data cleaning: Remove police identification stamps from shoe prints
  - Case-control sampling: All RAC cases + 20 random controls per shoe
- **Outputs**:
  - `dataCC.csv`: Case-control dataset
  - `all_cont.csv`: Cumulative contact surface data

### 2. Distance Calculations (`dataCC_distance_2.Rmd`)
- **Purpose**: Calculate distances from RACs to shoe contours
- **Key Features**:
  - Supports two contour algorithms: 'Active_Contour' and 'Convex'
  - Calculates minimum distance and horizontal distance to contour
  - Creates binary categories for distance analysis
- **Functions**:
  - `calculate_min_distance()`: Minimum Euclidean distance to contour
  - `calculate_min_horiz_distance()`: Minimum horizontal distance

### 3. Statistical Modeling (`re_model_shoe_std_3.Rmd`)
- **Purpose**: Random effects modeling for RAC intensity
- **Libraries Used**:
  - `lme4`: Mixed-effects models
  - `splines`: Natural cubic splines
  - `spam`, `Matrix`: Sparse matrix operations
  - `ggplot2`, `plotly`: Visualization
- **Model Types**:
  - NEW_X_NS_XY: Advanced spline model with coordinates
  - NS_XY: Natural splines with X,Y coordinates
  - NS_HORIZ/NS_MIN: Splines with distance features

### 4. Results and Outputs (`shoe_std_results_4.Rmd`)
- **Purpose**: Generate model outputs and visualizations
- **Features**: Model comparison, result standardization, and predictions

### 5. Statistical Testing (`statistical_tests_5.Rmd`)
- **Purpose**: Hypothesis testing and model validation

## Data Structure
- **Shoe Dimensions**: 307 columns × 395 rows per shoe
- **Number of Shoes**: 387 total (386 with RACs, shoe 127 excluded)
- **Relevant Area**: 150×300 pixels in center region
- **Coordinate System**: X: [-0.25, 0.25], Y: [-0.5, 0.5]

## Key Algorithms
1. **Active Contour**: Advanced contour detection algorithm
2. **Convex Hull**: Alternative contour method
3. **Case-Control Sampling**: All cases + 20 controls per shoe
4. **Distance Metrics**: Euclidean and horizontal distances to contours

## File Dependencies
- `Data/contacts_data.txt`: Raw shoe contact surface data
- `Data/locations_data.CSV`: RAC location coordinates
- `Data/contour_[algorithm].txt`: Contour data files
- `[Algorithm]/Dataset/`: Algorithm-specific datasets
- `[Algorithm]/Saved_Models/`: Trained model objects

## Configuration Variables
- `ROOT_PATH`: Base directory path
- `CONTOUR_ALGORITHM`: 'Active_Contour' or 'Convex'
- `IMAGE_NUMBER`: Specific shoe image for analysis
- `MODEL_FEATURE`: Model type selection

## Analysis Goals
1. Model RAC intensity across shoe surface
2. Compare different contour detection methods
3. Assess impact of distance to contour on RAC probability
4. Validate models through statistical testing
5. Generate standardized results for forensic applications

## Technical Notes
- Uses mixed-effects models to account for shoe-level variation
- Employs natural cubic splines for smooth surface modeling
- Implements efficient sparse matrix operations for large datasets
- Supports multiple visualization methods (static and interactive plots)

---

# Integration Notes
- Python pipeline generates contour data consumed by R analysis
- Both parts work with same dataset (387 shoes, 307×395 pixels)
- Shared coordinate system and file structure
- Combined approach enables both precise contour extraction and sophisticated statistical modeling