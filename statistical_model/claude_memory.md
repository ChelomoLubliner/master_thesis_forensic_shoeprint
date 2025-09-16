# Claude Memory: Shoe RAC Analysis Project

## Project Overview
This is a comprehensive statistical analysis project focused on Randomly Acquired Characteristics (RACs) in shoe prints. The project uses R/RMarkdown for data processing, statistical modeling, and visualization.

## Key Components

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
  - Uses Active Contour algorithm only
  - Calculates minimum distance and horizontal distance to contour
  - Creates binary categories for distance analysis
- **Functions**:
  - `calculate_min_distance()`: Minimum Euclidean distance to contour
  - `calculate_min_horiz_distance()`: Minimum horizontal distance

### 3. Shoe Distance Analysis (`3_calculate_shoe_distance.Rmd`)
- **Purpose**: Calculate distances for specific shoe images
- **Features**: Configurable for different image numbers using Active Contour algorithm
- **Key Function**: `min_distance_xy()`: Distance calculations for coordinate grids

### 4. Statistical Modeling (`4_random_effect_model_standardization_of_shoe.Rmd`)
- **Purpose**: Random effects modeling for RAC intensity
- **Libraries Used**:
  - `lme4`: Mixed-effects models
  - `splines`: Natural cubic splines
  - `spam`, `Matrix`: Sparse matrix operations
  - `ggplot2`, `plotly`: Visualization
- **Model Type**:
  - NEW_X_NS_XY: Advanced spline model with coordinates (only model used)

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
1. **Active Contour**: Advanced contour detection algorithm (only method used)
2. **Case-Control Sampling**: All cases + 20 controls per shoe
3. **Distance Metrics**: Euclidean and horizontal distances to contours

## File Dependencies
- `Data/contacts_data.txt`: Raw shoe contact surface data
- `Data/locations_data.CSV`: RAC location coordinates
- `Data/contour_Active_Contour.txt`: Active Contour data file
- `Active_Contour/Dataset/`: Active Contour datasets
- `Active_Contour/Saved_Models/`: Trained model objects

## Configuration Variables
- `ROOT_PATH`: Base directory path
- `CONTOUR_ALGORITHM`: 'Active_Contour' (fixed)
- `IMAGE_NUMBER`: Specific shoe image for analysis
- `MODEL_FEATURE`: 'NEW_X_NS_XY' (fixed)

## Analysis Goals
1. Model RAC intensity across shoe surface using Active Contour method
2. Assess impact of distance to contour on RAC probability
3. Validate NEW_X_NS_XY model through statistical testing
4. Generate standardized results for forensic applications

## Technical Notes
- Uses mixed-effects models to account for shoe-level variation
- Employs natural cubic splines for smooth surface modeling
- Implements efficient sparse matrix operations for large datasets
- Supports multiple visualization methods (static and interactive plots)