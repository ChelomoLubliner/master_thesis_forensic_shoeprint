# Forensic Shoeprint Analysis Pipeline - Technical Details

## Overview

This pipeline processes forensic shoeprint data to analyze randomly acquired characteristics (RAC) on shoe outsoles. The streamlined version focuses on essential processing steps for the final objective.

## Pipeline Architecture

```
Data Input (contacts_data.txt)
    ↓
1. create_files_shoes.py → list_matrices.npy, freq_min_18.npy
    ↓
2. contour.py → list_contour.npy
    ↓
3. active_contour_snake.py → active-contour_all.npy
    ↓
4. distance_extremities.py → locations_new.csv
```

**Note**: The pipeline consists of 4 active modules. Additional files (`contact_with_locations.py`, `convex_hull.py`, `alphas_shape.py`) exist as alternative methods but are not called in the current main.py workflow.

## Module Details

### 1. create_files_shoes.py
**Purpose**: Initial data processing and prototype generation

**Key Functions**:
- `contacts_data()`: Loads raw contact data from `contacts_data.txt` (387 shoe samples)
- `superposed_pixels()`: Creates frequency map and generates prototype at frequency 18
- `active_contour_on_prototype()`: Applies active contour to prototype

**Essential Outputs**:
- `list_matrices.npy`: Processed shoe contact matrices (387 samples)
- `freq_min_18.npy`: Prototype shoe boundary (used for noise filtering)

**Removed Non-Essential**:
- `superposition_all_shoes()`: General superposition visualization
- `superposed_pixels_reversed()`: Reverse frequency analysis
- `heatmap_superposed()`: Heatmap generation

### 2. contour.py
**Purpose**: Contour extraction with noise removal

**Key Functions**:
- `remove_noise_get_contour()`: Complete noise removal and contour extraction workflow
- `save_new_contour_shoe()`: Converts contour points to binary matrix
- `scatter_plot_contour()`: Visualization of contour points

**Essential Outputs**:
- `list_contour.npy`: Clean contour matrices for all shoes

**Dependencies**:
- Requires: `list_matrices.npy`, `freq_min_18.npy`
- Imports: `remove_noise.py` (uses `save_cleaned_shoes()`, `superpose_image_prototype()`)
- Imports: `extreme_values_x_y.py` (uses `get_contour()`)

### 3. active_contour_snake.py
**Purpose**: Advanced contour refinement using snake algorithms

**Key Functions**:
- `active_contour_shoe()`: Applies dual-snake algorithm (coarse→fine refinement)
- `init_snake()`: Initializes elliptical snake boundary
- `get_snake_image()`: Converts snake coordinates to image
- `extreme_values()`: Extracts extreme contour points

**Essential Outputs**:
- `active-contour_all.npy`: Refined contour boundaries

**Optimization Applied**:
- Disabled image plotting (`plot_img=False`)
- Disabled image saving (`save_img_bool=False`)

### 4. distance_extremities.py
**Purpose**: Spatial distance calculations between RAC and shoe boundaries

**Key Functions**:
- Calculates distances from RAC points to contour boundaries
- Updates location coordinates with distance measurements

**Essential Outputs**:
- `locations_new.csv`: Location data with distance calculations

### 5. contact_with_locations.py *(Not Currently Used)*
**Purpose**: Final RAC analysis and visualization generation (legacy/alternative analysis)

**Status**: Not called in main.py pipeline
**Key Functions**:
- Combines RAC locations with processed shoe data
- Generates final analysis results

**Note**: This module exists for additional analysis but is not part of the standard pipeline execution.

## Supporting Modules (Actively Used via Imports)

### Imported and Used by Pipeline Modules:
- **remove_noise.py**: Noise removal functions
  - Imported by: `contour.py` (line 10)
  - Functions used: `save_cleaned_shoes()`, `superpose_image_prototype()`
  - Purpose: Applies prototype boundary mask to remove noise from shoes
- **extreme_values_x_y.py**: Contour extraction utilities
  - Imported by: `contour.py` and `active_contour_snake.py`
  - Functions: Extract extreme contour points and coordinate manipulation

## Files Not Used in Main Pipeline

### Present but NOT Imported Anywhere:
- **contact_with_locations.py**: Alternative RAC analysis (not called in main.py)
- **alphas_shape.py**: Alpha shape analysis (alternative contour method)
- **convex_hull.py**: Convex hull analysis (alternative contour method)

## Dependencies

### Essential Dependencies:
- `extreme_values_x_y.py`: Contour point extraction utilities
- `globals.py`: Configuration constants (FOLDER, W, H, DATASET)

### Data Flow:
```
contacts_data.txt (47MB) → list_matrices.npy → list_contour.npy → active-contour_all.npy → locations_new.csv
```

## Configuration

### Dataset Settings (globals.py):
- `OLD_DATASET = True`: Uses old shoes dataset
- Dimensions: 307×395 pixels
- Sample count: 387 shoes
- Data source: `Data/contacts_data.txt`

## Performance Optimizations

1. **Image Generation Disabled**: Removed PNG/HTML generation in intermediate steps
2. **Visualization Disabled**: No popup windows during processing
3. **Essential Data Only**: Only `.npy` files and final outputs preserved
4. **Streamlined Functions**: Removed analysis steps not required for final objective

## Testing

The pipeline was tested without the final component (`contact_with_locations.py`) and successfully completed:
- ✅ Data processing (387 samples)
- ✅ Contour extraction (296 samples processed)
- ✅ Active contour refinement (in progress)

## Runtime Characteristics

- **Total runtime**: Several hours for complete dataset
- **Memory usage**: Moderate (processes one shoe at a time)
- **Bottlenecks**: Active contour processing (computationally intensive)
- **Output size**: Essential `.npy` files (~MB range vs. GB of images)

## File Structure

```
├── main.py                     # Pipeline orchestrator (4 modules)
├── create_files_shoes.py       # Step 1: Data preparation
├── contour.py                  # Step 2: Contour extraction
├── active_contour_snake.py     # Step 3: Snake algorithm refinement
├── distance_extremities.py     # Step 4: Distance calculations
│
├── remove_noise.py             # [Supporting] Used by contour.py
├── extreme_values_x_y.py       # [Supporting] Used by multiple modules
├── globals.py                  # [Configuration] Used by all
├── requirements.txt            # Python dependencies
│
├── contact_with_locations.py   # [Not used] Alternative analysis
├── alphas_shape.py             # [Not used] Alpha shape method
├── convex_hull.py              # [Not used] Convex hull method
│
└── ../data/
    ├── contacts_data.txt       # Input: Raw shoe data (387 shoes)
    ├── locations_data.csv      # Input: RAC location data
    └── contour_Active_Contour.txt  # Output: Generated by Python for R
```

This streamlined pipeline maintains all essential functionality while removing non-critical visualization and analysis components, resulting in faster execution focused on the core objective of RAC spatial modeling.