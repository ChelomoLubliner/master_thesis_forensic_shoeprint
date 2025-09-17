# Claude Memory: Complete Shoe RAC Analysis Project

## Project Overview
This is a comprehensive forensic analysis project combining computer vision and statistical modeling for analyzing Randomly Acquired Characteristics (RACs) in shoe prints. The project consists of two main components:
1. **Contour Algorithm Pipeline** (Python) - Image processing and contour extraction
2. **Statistical Model** (R/RMarkdown) - Advanced statistical analysis and modeling

---

# Part 1: Computer Vision Pipeline (Python)

## Core Processing Steps
1. **Data preparation** - Load and preprocess shoeprint matrices
2. **Contour extraction** - Extract shoe contours with noise removal
3. **Active contour refinement** - Apply snake algorithms for precise boundaries
4. **Distance calculations** - Compute spatial relationships
5. **Contact analysis** - Generate final RAC location mappings

## Key Files (contour_algorithm/)
- `main.py` - Main pipeline runner
- `active_contour_snake.py` - Active contour implementation
- `contour.py` - Basic contour extraction
- `distance_extremities.py` - Distance calculations
- `contact_with_locations.py` - RAC location mapping
- `create_files_shoes.py` - File processing utilities
- `globals.py` - Configuration settings

## Configuration
- **Dataset**: 387 shoe samples (386 with RACs, excluding shoe 127)
- **Dimensions**: 307×395 pixels per shoe
- **Snake parameters**: center=(155,200), radius=(90,162)
- **Environment variables** for dataset switching

---

# Part 2: Statistical Analysis (R)

## Statistical Pipeline Components

### 1. Data Processing Pipeline (`1_dataCC.Rmd`)
- **Purpose**: Initial data cleaning and case-control sampling
- **Key Functions**:
  - `aspix_x()` and `aspix_y()`: Convert coordinates to pixel positions
  - Data cleaning: Remove police identification stamps from shoe prints
  - Case-control sampling: All RAC cases + 20 random controls per shoe
- **Outputs**:
  - `dataCC.csv`: Case-control dataset
  - `all_cont.csv`: Cumulative contact surface data

### 2. Distance Calculations (`2_dataCC_distance.Rmd`)
- **Purpose**: Calculate distances from RACs to shoe contours
- **Key Features**:
  - Supports two contour algorithms: 'Active_Contour' and 'Convex'
  - Calculates minimum distance and horizontal distance to contour
  - Creates binary categories for distance analysis
- **Functions**:
  - `calculate_min_distance()`: Minimum Euclidean distance to contour
  - `calculate_min_horiz_distance()`: Minimum horizontal distance

### 3. Shoe Distance Analysis (`3_calculate_shoe_distance.Rmd`)
- **Purpose**: Calculate distances for specific shoe images
- **Features**: Configurable for different image numbers and contour algorithms
- **Key Function**: `min_distance_xy()`: Distance calculations for coordinate grids

### 4. Statistical Modeling (`4_random_effect_model_standardization_of_shoe.Rmd`)
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

### 5. Results and Outputs (`5_output_and_results_standardization_of_shoe.Rmd`)
- **Purpose**: Generate model outputs and visualizations
- **Features**: Model comparison and result standardization

### 6. Statistical Testing (`6_statistical_tests.Rmd`)
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