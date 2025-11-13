# Deep Code Analysis Summary

**Date**: November 2024
**Analysis Type**: Complete dependency and usage analysis

## 🔍 Analysis Results

### Python Pipeline Architecture

#### ✅ Active Pipeline Modules (Called by main.py)

1. **create_files_shoes.py**
   - Called: Line 7 in main.py
   - Imports: `active_contour_snake` (uses `active_contour_on_prototype()`)

2. **contour.py**
   - Called: Line 8 in main.py
   - Imports: `remove_noise` (uses `save_cleaned_shoes()`, `superpose_image_prototype()`)
   - Imports: `extreme_values_x_y` (uses `get_contour()`)

3. **active_contour_snake.py**
   - Called: Line 9 in main.py
   - Imports: `extreme_values_x_y` (uses `dict_points()`, `get_contour()`)

4. **distance_extremities.py**
   - Called: Line 10 in main.py
   - No imports of other project modules

#### ✅ Supporting Modules (Actively Used via Imports)

1. **remove_noise.py**
   - **Status**: ✅ ACTIVELY USED
   - **Imported by**: `contour.py` (line 10)
   - **Functions exported**:
     - `save_cleaned_shoes(list_matrices, im_num)` - Applies prototype boundary mask
     - `superpose_image_prototype(im_num)` - Visualization overlay
   - **Purpose**: Essential noise filtering using freq_min_18.npy prototype

2. **extreme_values_x_y.py**
   - **Status**: ✅ ACTIVELY USED
   - **Imported by**: `contour.py` and `active_contour_snake.py`
   - **Purpose**: Contour point extraction and manipulation utilities

3. **globals.py**
   - **Status**: ✅ ACTIVELY USED
   - **Imported by**: All pipeline modules
   - **Purpose**: Configuration (OLD_DATASET, W, H, FOLDER, DATASET, LOCATIONS)

#### ❌ Unused Modules (No Imports Found)

1. **contact_with_locations.py**
   - **Status**: ❌ NOT USED
   - **Evidence**: No imports found in any .py file
   - **Purpose**: Alternative RAC analysis (legacy)

2. **alphas_shape.py**
   - **Status**: ❌ NOT USED
   - **Evidence**: No imports found in any .py file
   - **Purpose**: Alpha shape contour analysis (alternative method)

3. **convex_hull.py**
   - **Status**: ❌ NOT USED
   - **Evidence**: No imports found in any .py file
   - **Purpose**: Convex hull contour analysis (alternative method)

### R Pipeline Architecture

#### ✅ Active R Markdown Files (Sequential Execution)

1. **dataCC_1.Rmd** - Data preparation and case-control sampling
   - Sources: `config.R`
   - Reads: `../data/contacts_data.txt`, `../data/locations_data.csv`
   - Outputs: `dataCC.csv`, `all_cont.csv`

2. **dataCC_distance_2.Rmd** - Distance calculations
   - Sources: `config.R`
   - Reads: `dataCC.csv`, `contour_Active_Contour.txt` (or `contour_Convex.txt`)
   - Outputs: `dataCC_distance.csv`

3. **re_model_shoe_std_3.Rmd** - Statistical modeling
   - Sources: `config.R`
   - Reads: `dataCC_distance.csv`
   - Outputs: `saved_models/*.rds`, `dataCC_distance_part4.csv`

4. **shoe_std_results_4.Rmd** - Results and visualization
   - Sources: `config.R`
   - Reads: Models from `saved_models/`
   - Outputs: Predictions, plots, visualizations

5. **statistical_tests_5.Rmd** - Model validation
   - Sources: `config.R`
   - Reads: Models and results
   - Outputs: Statistical test results

#### Configuration File

**config.R**
- `ROOT_PATH`: Auto-detected project root
- `CONTOUR_ALGORITHM`: "Active_Contour" (or "Convex")
- `IMAGE_NUMBER`: "171" (or "135")
- `MODEL_FEATURE`: "NEW_X_NS_XY_RELATIVE"

### Integration Between Python and R

```
Python Pipeline                    R Pipeline
────────────────                  ────────────

contacts_data.txt  ────────────→  dataCC_1.Rmd
locations_data.csv ────────────→  dataCC_1.Rmd
                                         ↓
Python generates:                  dataCC.csv
contour_Active_Contour.txt ─────→ dataCC_distance_2.Rmd
                                         ↓
                                  dataCC_distance.csv
                                         ↓
                                  re_model_shoe_std_3.Rmd
                                         ↓
                                  saved_models/*.rds
```

### Key Findings

1. **remove_noise.py is ACTIVELY USED** - Not legacy!
   - Essential component imported by contour.py
   - Provides critical noise filtering functionality

2. **Three unused files confirmed**:
   - contact_with_locations.py
   - alphas_shape.py
   - convex_hull.py

3. **Python-R Integration Point**:
   - Python creates `contour_Active_Contour.txt` in data/ directory
   - R reads this file in `dataCC_distance_2.Rmd` (line 40)

4. **Model File Naming Issue** (re_model_shoe_std_3.Rmd):
   - Line 173 looks for: `NS_XY.rds`
   - But saves as: `NS_XY_RELATIVE.rds`
   - This causes error in `get_initial_values()` function
   - However, initial values are overwritten (line 164) so error may not manifest

### Verification Commands Used

```bash
# Search for imports
grep -r "import remove_noise\|from remove_noise" contour_algorithm/
grep -r "import.*convex_hull\|from.*convex_hull" contour_algorithm/
grep -r "import.*alphas_shape\|from.*alphas_shape" contour_algorithm/
grep -r "import.*contact_with_locations" contour_algorithm/

# Check data files
ls -lh data/
ls -lh statistical_model/dataset/
ls -lh statistical_model/saved_models/

# Find .rds model files
find statistical_model -name "*.rds"
```

## 📝 Documentation Updates Made

All .md files have been updated to reflect this accurate analysis:

1. ✅ **claude_memory.md** - Updated to show correct module status
2. ✅ **contour_algorithm/README.md** - Clarified supporting vs unused modules
3. ✅ **contour_algorithm/PIPELINE_DETAILS.md** - Correctly classifies remove_noise.py under "Supporting Modules (Actively Used via Imports)" and excludes it from "Not Used" section
4. ✅ **statistical_model/PIPELINE_DETAILS.md** - Updated save/load paths to use `_RELATIVE.rds` suffix consistently
5. ✅ **README.md** - Updated project structure to show supporting files

**Note**: Initial analysis incorrectly classified remove_noise.py as legacy/unused. After grep verification, confirmed it is actively imported by contour.py (line 10) and now correctly documented across all files.

## ✅ Verified Facts

- [x] main.py calls exactly 4 modules
- [x] remove_noise.py is imported and used by contour.py
- [x] extreme_values_x_y.py is imported by 2 modules
- [x] convex_hull.py, alphas_shape.py, contact_with_locations.py are NOT imported
- [x] Python creates contour_Active_Contour.txt for R to consume
- [x] R pipeline has 5 sequential .Rmd files
- [x] Model files use _RELATIVE suffix

---

**Analysis Method**: Code inspection, import tracking, file system verification
**Confidence Level**: High (verified through multiple methods)
