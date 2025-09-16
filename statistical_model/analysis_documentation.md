# Shoe RAC Analysis Project Documentation

## Executive Summary

This project implements a comprehensive statistical framework for analyzing Randomly Acquired Characteristics (RACs) in shoe prints for forensic applications. The analysis employs advanced statistical modeling techniques including mixed-effects models and spline-based surface modeling to understand RAC intensity patterns across shoe surfaces.

## Project Structure

### Core Analysis Files

1. **`1_dataCC.Rmd`** - Data Preprocessing and Case-Control Sampling
2. **`2_dataCC_distance.Rmd`** - Distance Calculations to Contours
3. **`3_calculate_shoe_distance.Rmd`** - Individual Shoe Distance Analysis
4. **`4_random_effect_model_standardization_of_shoe.Rmd`** - Statistical Modeling
5. **`5_output_and_results_standardization_of_shoe.Rmd`** - Results Generation
6. **`6_statistical_tests.Rmd`** - Model Validation and Testing
7. **`convert_md_to_pdf.R`** - Documentation Export Utility

## Technical Implementation

### Data Processing Pipeline

The analysis begins with raw shoe print data consisting of:
- **387 shoe prints** (386 with RACs, excluding shoe 127)
- **307×395 pixel resolution** per shoe
- **Contact surface data** with police stamp removal
- **RAC location coordinates** in standardized coordinate system

### Key Algorithms

#### 1. Coordinate Transformation
```r
aspix_x(x, col_shoe=307, rel_col_shoe=150, rel_x_cord=0.25)
aspix_y(y, row_shoe=395, rel_row_shoe=300, rel_Y_cord=0.5)
```
Converts real-world coordinates to pixel positions within the relevant shoe area.

#### 2. Stamp Removal Algorithm
- Identifies cumulative contact surfaces appearing in >8 shoes
- Calculates upper and lower bounds to isolate authentic contact areas
- Removes police identification stamps from analysis

#### 3. Distance Calculations
- **Minimum Distance**: Euclidean distance to nearest contour point
- **Horizontal Distance**: Distance along horizontal axis to contour
- **Binary Categorization**: Distance threshold at 0.1 units

#### 4. Case-Control Sampling
- **Cases**: All pixels containing RACs (n_Acc = 1)
- **Controls**: 20 randomly selected non-RAC pixels per shoe
- Ensures balanced dataset for statistical modeling

### Statistical Modeling Framework

#### Model Types Implemented

1. **NEW_X_NS_XY**: Advanced model with natural cubic splines for X,Y coordinates
2. **NS_XY**: Standard spline model for spatial coordinates
3. **NS_HORIZ**: Horizontal distance-based spline model
4. **NS_MIN**: Minimum distance-based spline model

#### Mixed-Effects Approach
- **Fixed Effects**: Spatial coordinates, distance measures, spline terms
- **Random Effects**: Shoe-level variation to account for individual shoe characteristics
- **Libraries**: `lme4` for mixed-effects modeling, `splines` for basis functions

### Contour Detection Methods

#### Active Contour Algorithm
- Advanced boundary detection using active contour models
- Provides precise shoe outline boundaries
- Better handling of irregular shapes

#### Convex Hull Method
- Simpler geometric approach using convex hull
- Faster computation but less precise boundaries
- Useful for comparison and validation

## Key Findings and Applications

### Forensic Implications
1. **RAC Distribution Patterns**: Identifies areas of shoes most likely to acquire characteristics
2. **Distance Effects**: Quantifies relationship between contour proximity and RAC probability
3. **Individual Shoe Variation**: Accounts for unique characteristics of different shoes
4. **Statistical Validation**: Provides rigorous testing framework for forensic conclusions

### Model Performance
- Supports multiple contour detection algorithms for robustness
- Implements cross-validation through case-control sampling
- Generates standardized results for forensic reporting
- Provides uncertainty quantification through mixed-effects framework

## Data Dependencies

### Input Files
- `Data/contacts_data.txt`: Raw binary contact surface data
- `Data/locations_data.CSV`: RAC coordinate locations
- `Data/contour_[Active_Contour|Convex].txt`: Contour boundary data

### Output Files
- `Data/dataCC.csv`: Case-control dataset
- `Data/all_cont.csv`: Cumulative contact surfaces
- `[Algorithm]/Dataset/dataCC_distance.csv`: Distance-augmented dataset
- `[Algorithm]/Saved_Models/*.rds`: Trained model objects

## Configuration and Reproducibility

### Key Parameters
```r
ROOT_PATH = 'YOUR_PATH'                    # Base directory
CONTOUR_ALGORITHM = 'Active_Contour'       # Algorithm choice
IMAGE_NUMBER = 171                         # Specific shoe analysis
MODEL_FEATURE = 'NEW_X_NS_XY'             # Model type
```

### Reproducibility Features
- Fixed random seed (313) for consistent results
- Modular design allowing algorithm swapping
- Comprehensive documentation and commenting
- Standardized file naming conventions

## Technical Requirements

### R Libraries
- **Core**: `ggplot2`, `dplyr`, `Matrix`, `spam`
- **Modeling**: `lme4`, `splines`, `survival`, `smoothie`
- **Visualization**: `plotly`, `rgl`, `fields`, `imager`
- **Documentation**: `rmarkdown`, `knitr`

### Computational Considerations
- Sparse matrix operations for memory efficiency
- Progress tracking for long-running distance calculations
- Memory management with explicit garbage collection
- Parallel processing capabilities where applicable

## Quality Assurance

### Validation Methods
1. **Cross-validation**: Case-control sampling methodology
2. **Algorithm comparison**: Multiple contour detection methods
3. **Statistical testing**: Formal hypothesis testing framework
4. **Sensitivity analysis**: Parameter variation studies

### Error Handling
- Graceful handling of missing data (shoe 127)
- Infinite distance handling in boundary cases
- Data type validation and conversion
- File existence checking before operations

## Future Enhancements

### Potential Improvements
1. **Additional Contour Algorithms**: Implementation of more sophisticated boundary detection
2. **Spatial Correlation Modeling**: Advanced geostatistical approaches
3. **Machine Learning Integration**: Neural networks for pattern recognition
4. **Real-time Analysis**: Streamlined pipeline for operational use
5. **Interactive Visualization**: Web-based analysis dashboard

### Research Applications
- Extension to other forensic pattern evidence
- Integration with automated image processing systems
- Development of expert system for forensic conclusions
- Standardization for inter-laboratory comparisons

## Conclusion

This project represents a comprehensive statistical framework for forensic shoe print analysis, combining rigorous statistical methodology with practical forensic applications. The modular design ensures flexibility for different analysis scenarios while maintaining scientific rigor through proper validation and uncertainty quantification.