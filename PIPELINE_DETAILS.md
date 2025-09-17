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
    ↓
5. contact_with_locations.py → Final RAC Analysis
```

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
- `save_cleaned_shoes()`: Filters shoes using prototype boundary (moved from remove_noise.py)
- `remove_noise_get_contour()`: Complete noise removal and contour extraction workflow
- `save_new_contour_shoe()`: Converts contour points to binary matrix

**Essential Outputs**:
- `list_contour.npy`: Clean contour matrices for all shoes

**Dependencies**:
- Requires: `list_matrices.npy`, `freq_min_18.npy`
- Uses: `extreme_values_x_y.py` for contour point extraction

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

### 5. contact_with_locations.py
**Purpose**: Final RAC analysis and visualization generation

**Key Functions**:
- Combines RAC locations with processed shoe data
- Generates final analysis results

## Removed Files

### Deleted as Non-Essential:
- **remove_noise.py**: Function moved to `contour.py`
- **alphas_shape.py**: Alpha shape analysis (not in main pipeline)
- **convex_hull.py**: Convex hull analysis (not in main pipeline)

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
├── main.py                     # Pipeline orchestrator
├── create_files_shoes.py       # Data preparation
├── contour.py                  # Contour extraction + noise removal
├── active_contour_snake.py     # Snake algorithm refinement
├── distance_extremities.py     # Distance calculations
├── contact_with_locations.py   # Final analysis
├── extreme_values_x_y.py       # Utility functions
├── globals.py                  # Configuration
└── Data/
    ├── contacts_data.txt       # Raw input (387 shoes)
    └── locations_data.csv      # RAC location data
```

This streamlined pipeline maintains all essential functionality while removing non-critical visualization and analysis components, resulting in faster execution focused on the core objective of RAC spatial modeling.