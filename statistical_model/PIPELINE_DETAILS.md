# Statistical Model Pipeline - Technical Details

> **Complete technical specification of the R statistical analysis pipeline**

## Pipeline Overview

The statistical model consists of **5 sequential R Markdown files** that process forensic shoeprint data from raw case-control sampling through advanced mixed-effects modeling to final validation.

**Execution Order**: 1 → 2 → 3 → 4 → 5 (strict dependencies)

---

## File Structure

```
statistical_model/
├── config.R                    # Central configuration
├── dataCC_1.Rmd               # Step 1: Data preparation
├── dataCC_distance_2.Rmd      # Step 2: Distance calculations
├── re_model_shoe_std_3.Rmd    # Step 3: Statistical modeling
├── shoe_std_results_4.Rmd     # Step 4: Results & visualization
├── statistical_tests_5.Rmd    # Step 5: Model validation
│
├── saved_models/              # Trained model files (.rds)
├── dataset/                   # Intermediate datasets
└── model_images/              # Generated visualizations
```

---

## Detailed Module Analysis

### Configuration: `config.R`

**Purpose**: Central configuration loaded by all .Rmd files

**Key Variables**:
```r
ROOT_PATH            # Auto-detected project root
CONTOUR_ALGORITHM    # "Active_Contour" or "Convex"
IMAGE_NUMBER         # "171" or "135" (for specific shoe analysis)
MODEL_FEATURE        # "NEW_X_NS_XY_RELATIVE" (model type)
```

**Path Detection**:
- If RStudio: Uses `rstudioapi` to detect file location
- Fallback: Uses `getwd()` assumption

---

### Step 1: `dataCC_1.Rmd` - Data Preparation & Case-Control Sampling

**Author**: Chelomo Lubliner
**Seed**: 313 (reproducibility)

#### Key Operations

**1. Load Raw Data**
- Reads: `../data/contacts_data.txt` (387 shoes × 307×395 pixels)
- Character-based reading: `(307 * 395 + 2) * 387` characters
- Creates list of 387 contact matrices

**2. Data Cleaning**
- **Mirror Shoe 9**: Flips shoe 9 horizontally to match orientation
- **Remove Police Stamps**:
  - Creates cumulative contact surface (`allcont >= 8`)
  - Identifies lower and upper bounds algorithmically
  - Removes stamp regions from all shoes

**3. RAC Location Processing**
- Reads: `../data/locations_data.csv`
- Converts X,Y coordinates to pixel positions using:
  - `aspix_x()`: X coordinate → column pixel
  - `aspix_y()`: Y coordinate → row pixel
- Handles multiple RACs per pixel (counts them)

**4. Contact Surface Adjustment**
- Sets contact surface = 1 where RACs exist
- Rationale: RACs may tear sole, creating apparent gaps

**5. Case-Control Sampling**
- **Strategy**: Within-cluster case-control sub-sampling
- **Per shoe**:
  - ALL cases (pixels with RACs, n_Acc = 1)
  - 20 random controls (pixels without RACs, n_Acc = 0)
- **Rationale**: High-resolution intensity estimation is computationally expensive

#### Outputs
```
../data/dataCC.csv        # Case-control dataset (~8,000 rows)
../data/all_cont.csv      # Cumulative contact surface
```

#### Key Functions
```r
aspix_x(x, col_shoe=307, rel_col_shoe=150, rel_x_cord=0.25)
aspix_y(y, row_shoe=395, rel_row_shoe=300, rel_Y_cord=0.5)
```

#### Coordinate System
- **X range**: [-0.25, 0.25] → 307 pixels
- **Y range**: [-0.5, 0.5] → 395 pixels
- **Relevant region**: 150×300 pixels (center)

---

### Step 2: `dataCC_distance_2.Rmd` - Distance Calculations

**Author**: Chelomo Lubliner
**Date**: 2023-07-17

#### Key Operations

**1. Load Case-Control Data**
- Reads: `../data/dataCC.csv`

**2. Load Contour Data**
- Reads: `../data/contour_Active_Contour.txt` (or `contour_Convex.txt`)
- **Format**: Same as contacts_data.txt (387 shoes × 307×395 pixels)
- Converts contour matrices to X,Y coordinates
- Processes 386 shoes (shoe 127 excluded - no RACs)

**3. Distance Calculations**

**Minimum Euclidean Distance**:
```r
calculate_min_distance(new_data, contour_alg_df)
```
- For each point in dataCC:
  - Finds contour points for same shoe
  - Calculates Euclidean distance to all contour points
  - Records minimum distance
- Progress tracking: Updates every 1000 rows

**Minimum Horizontal Distance**:
```r
calculate_min_horiz_distance(new_data, contour_alg_df)
```
- Finds nearest contour point with similar Y coordinate (±0.01)
- If no horizontal match found: Uses `min_dist` instead
- Handles edge cases with `is.infinite()` check

**4. Binary Categorization**
- Optional distance categories (commented out in current version)
- `horiz_dist_cat`: Binary indicator for distance > 0.1

**5. Visualization**
- Creates plotly scatter plots comparing dataCC points vs contour points
- Example shoe: 200

#### Outputs
```
statistical_model/dataset/dataCC_distance.csv    # Enhanced dataset with distances
```

#### Performance
- Nested loops: ~8,000 rows × ~contour points per shoe
- Runtime: ~3-5 minutes for full dataset

---

### Step 3: `re_model_shoe_std_3.Rmd` - Statistical Modeling

**Seed**: 313
**Key Libraries**: `lme4` (mixed-effects models), `splines` (natural cubic splines), `Matrix`, `spam` (sparse operations)

#### Key Operations

**1. Load Data**
- Reads: `statistical_model/dataset/dataCC_distance.csv`
- Reads: `../data/all_cont.csv`

**2. Distance Shape Calculation**
- Loads contour image for shoe 135 (`new_contour_135.png`)
- Calculates distance per Y coordinate
- Computes `distance_shape` for each point
- Creates `new_x` variable: Standardized X coordinate
  ```r
  new_x = (x * distance_shape) / (abs(x) + horiz_dist)
  ```

**3. Model Fitting Function**
```r
Random(nknotsx=3, nknotsy=5, dat=dataCC, model_feat=MODEL_FEATURE, initial_values)
```

**Model Specifications**:

| Model Feature | Formula | Knots |
|--------------|---------|-------|
| `NEW_X_NS_XY` | `n_Acc ~ ns(new_x,knots):ns(y,knots) + (1|shoe)` | 3×5 |
| `NS_XY` | `n_Acc ~ ns(x,knots):ns(y,knots) + (1|shoe)` | 3×5 |
| `NS_HORIZ` | `n_Acc ~ ns(horiz_dist,knots) + (1|shoe)` | 2 |
| `NS_MIN` | `n_Acc ~ ns(min_dist,knots) + (1|shoe)` | 2 |
| `HORIZ_DIST` | `n_Acc ~ horiz_dist + (1|shoe)` | - |
| `MIN_DIST` | `n_Acc ~ min_dist + (1|shoe)` | - |
| `EMPTY_MODEL` | `n_Acc ~ (1|shoe)` | - |

**Model Details**:
- **Family**: Binomial with logit link
- **Random Effects**: Random intercept per shoe `(1|shoe)`
- **Optimizer**: `nlminbwrap` (default) or `bobyqa`
- **Fixed Effects**: Natural cubic splines with interaction
- **Offset**: `log(0.005)` for case-control design

**4. Initial Values Function**
```r
get_initial_values()
```
- **Issue**: Looks for `NS_XY.rds` but file is `NS_XY_RELATIVE.rds`
- **Status**: Function exists but initial values are overwritten (line 164)
- **Impact**: No error in practice as values aren't actually used

**5. Model Saving**
```r
file_name <- paste(ROOT_PATH, "statistical_model/saved_models/",
                   MODEL_FEATURE, "_RELATIVE.rds", sep = "")
saveRDS(est, file = file_name)
```

#### Outputs
```
statistical_model/saved_models/NEW_X_NS_XY_RELATIVE.rds    # 10.4 MB
statistical_model/saved_models/NS_XY_RELATIVE.rds          # 9.1 MB
statistical_model/dataset/dataCC_distance_part4.csv        # Enhanced with new_x
```

#### Model Fitting Details
- **Convergence**: May show warnings for complex models
- **Runtime**: 5-10 minutes depending on model complexity
- **Memory**: 3-4 GB peak usage

---

### Step 4: `shoe_std_results_4.Rmd` - Results & Visualization

**Seed**: 313

#### Key Operations

**1. Load Trained Model**
```r
file_name <- paste(ROOT_PATH, "statistical_model/saved_models/",
                   MODEL_FEATURE, "_RELATIVE.rds", sep = "")
rand <- readRDS(file = file_name)
```

**2. Create Prediction Grid**
- Generates 307×395 = 121,265 prediction points
- Uses `expand.grid()` for all pixel combinations
- Loads prototype image: `images/cleaned_shoes/im_135.png`

**3. Design Matrix Construction**
- Builds spline basis for entire grid
- Different logic for `NEW_X_NS_XY` vs `NS_XY`
- Matrix multiplication: `(121,265 × N_params) × (N_params × 1)`

**4. Prediction Calculation**
```r
pred.case_control <- newdesignmat %*% fixef(rand) + log(0.005)
```
- Uses fixed effects only (population-level)
- Adds offset `log(0.005)` for case-control adjustment
- Sets NA for areas outside contour

**5. Probability & Intensity Conversion**
```r
prob.pred <- exp(pred) / (1 + exp(pred))     # Logit → Probability
intens <- -log(1 - prob.pred)                 # Probability → Intensity
```

**6. Visualization Generation**

**For Prototype Shoe (135)**:
- Creates intensity heatmaps
- Applies shoe mask (removes non-contact areas)
- Generates PDF files in `model_images/`

**For Target Shoe (171 or other)**:
- Loads specific shoe contour: `new_contour_171.png`
- Loads filled shoe image: `new_filled_171.png`
- **Adaptation algorithm**: `adapt_line()`
  - Stretches/compresses intensity lines to match new shoe shape
  - Handles left (negative) and right (positive) sides separately
  - Preserves intensity distribution while fitting contour

**7. Image Output**
```r
# Prototype visualizations
model_images/NEW_X_NS_XY_RELATIVE_SHOE.pdf
model_images/NEW_X_NS_XY_RELATIVE_CONTOUR.pdf

# Target shoe visualizations
model_images/NEW_X_NS_XY_171_NEW_SHOE.pdf
model_images/NEW_X_NS_XY_171_NEW_CONTOUR.pdf
```

#### Key Algorithm: `adapt_line()`
**Purpose**: Adapt intensity from prototype to different shoe shape

**Logic**:
```r
adapt_line(is_negative, old_line, contour_line)
```
1. Count contour pixels (minus 5 for buffer)
2. If contour exists:
   - Map old intensity indices to new contour length
   - Interpolate intensity values
   - Fill remainder with NA
3. Handle left/right sides independently
4. Reverse if processing negative (left) side

#### Outputs
- PDF heatmaps in `statistical_model/model_images/`
- Rotated images for proper visualization orientation

---

### Step 5: `statistical_tests_5.Rmd` - Model Validation

**Author**: Chelomo Lubliner

#### Key Operations

**1. Load Data**
- Reads: `statistical_model/dataset/dataCC_distance.csv`
- Reads: `../data/all_cont.csv`

**2. Baseline Model Loading**
```r
file_name <- paste(ROOT_PATH, "statistical_model/saved_models/NS_XY_RELATIVE.rds", sep = "")
naomi_model <- readRDS(file = file_name)
```
- Uses `NS_XY_RELATIVE.rds` as baseline "Naomi model"
- Prints full summary statistics

**3. Model Comparison Function**
```r
model_info(model_feat = MODEL_FEATURE)
```

**Performs**:
- Loads specified model from `saved_models/` with `_RELATIVE.rds` suffix
- Prints model summary
- **Likelihood Ratio Test (LRT)** vs baseline:
  ```r
  lrt_naomi <- lrtest(naomi_model, model)
  ```
- Compares nested models for statistical significance

**4. Tests Performed**
- Model goodness-of-fit
- Comparison of NEW_X_NS_XY vs NS_XY
- Chi-square test with degrees of freedom
- P-values for model improvement

#### Outputs
- Console output with statistical test results
- LRT statistics (Chi-square, df, p-value)
- Model summaries (coefficients, random effects, fit statistics)

#### Model Comparison Example
```
LRT : compare with naomi model
  #Df  LogLik Df  Chisq Pr(>Chisq)
1  ...  ...
2  ...  ...   ...  ...   ***
```

---

## Key Technical Details

### Coordinate Transformations

**From coordinates to pixels**:
```r
pix_x = col_shoe - (floor((x + rel_x_cord) / delx) + not_rel_col)
pix_y = row_shoe - (floor((y + rel_Y_cord) / dely) + not_rel_row)
```

Where:
- `delx = (2 * 0.25) / 150 = 0.00333...`
- `dely = (2 * 0.5) / 300 = 0.00333...`
- `not_rel_col = ceiling((307 - 150) / 2) = 79`
- `not_rel_row = ceiling((395 - 300) / 2) = 48`

### Model Formula Construction

For **NEW_X_NS_XY** with 3×5 knots:
- X basis: 5 spline functions (3 knots → 3+2 df)
- Y basis: 7 spline functions (5 knots → 5+2 df)
- Interaction: 5 × 7 = 35 terms
- Plus intercept: 36 fixed effects
- Plus 1 random effect variance: 37 parameters total

### Performance Characteristics

| Step | Runtime | Memory | Bottleneck |
|------|---------|--------|------------|
| 1. dataCC_1 | 2-3 min | ~1 GB | Data loading |
| 2. dataCC_distance_2 | 3-5 min | ~2 GB | Nested distance loops |
| 3. re_model_shoe_std_3 | 5-10 min | 3-4 GB | GLMM fitting |
| 4. shoe_std_results_4 | 3-5 min | ~2 GB | Grid prediction |
| 5. statistical_tests_5 | 2-4 min | ~1 GB | LRT computation |
| **Total** | **15-30 min** | **4-8 GB** | Model fitting |

### File Sizes

```
saved_models/NEW_X_NS_XY_RELATIVE.rds    10.4 MB
saved_models/NS_XY_RELATIVE.rds           9.1 MB
dataset/dataCC_distance.csv               1.6 MB
dataset/dataCC_distance_part4.csv         1.9 MB
../data/dataCC.csv                        740 KB
../data/all_cont.csv                      240 KB
```

---

## Common Issues & Solutions

### Issue 1: Model File Naming with `_RELATIVE` Suffix
**Background**: The `re_model_shoe_std_3.Rmd` script automatically appends `_RELATIVE` suffix when saving models (line 236-238), resulting in filenames like `NEW_X_NS_XY_RELATIVE.rds` and `NS_XY_RELATIVE.rds`.

**Current Config Default**: `MODEL_FEATURE <- "NEW_X_NS_XY_RELATIVE"` (in config.R)

**Minor Issue**: The `get_initial_values()` function (line 173) looks for `NS_XY.rds` instead of `NS_XY_RELATIVE.rds`.
- **Impact**: None (initial values are overwritten on line 164)
- **Fix**: Either update the function to use `NS_XY_RELATIVE.rds` or remove it entirely

**Note**: If you set `MODEL_FEATURE <- "NEW_X_NS_XY"` in config.R, the code will save as `NEW_X_NS_XY_RELATIVE.rds` due to the automatic suffix. The current default already includes `_RELATIVE` to match the actual saved filenames.

### Issue 2: Memory Errors
**Solution**: `memory.limit(size = 8000)` (Windows) or reduce dataset size for testing

### Issue 3: Model Convergence Warnings
**Solution**: Use `glmerControl(optimizer="bobyqa", optCtrl=list(maxfun=100000))`

### Issue 4: Path Issues
**Solution**: Verify `ROOT_PATH` in config.R points to project root

---

## Reproducibility

- **Random Seed**: 313 (consistent across files 1, 3, 4)
- **Package Versions**: Managed via R session
- **Data**: Fixed input files from Python pipeline
- **Models**: Saved as .rds for exact reproduction

---

**Last Updated**: November 2024
**Pipeline Version**: Production (Thesis submission)
