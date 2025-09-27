# Statistical Model Configuration
# This file contains all configuration parameters for the statistical analysis pipeline

# Load environment variables from .env file if it exists
if (file.exists(".env")) {
  readRenviron(".env")
}

# Set seed for reproducibility
set.seed(313)

# =============================================================================
# PROJECT PATHS (Simplified - no algorithm-specific subdirectories needed)
# =============================================================================
ROOT_PATH <- Sys.getenv("R_ROOT_PATH")  # Root of the project
MODEL_FEATURE <- Sys.getenv("R_MODEL_FEATURE")  # Model type selection

# =============================================================================
# SHOE PARAMETERS
# =============================================================================
# Shoe dimensions
COL_SHOE <- as.numeric(Sys.getenv("R_COL_SHOE"))  # Number of columns in each shoe
ROW_SHOE <- as.numeric(Sys.getenv("R_ROW_SHOE"))  # Number of rows in each shoe
NUM_SHOE <- as.numeric(Sys.getenv("R_NUM_SHOE"))  # Total number of shoes

col_shoe <- COL_SHOE
row_shoe <- ROW_SHOE
num_shoe <- NUM_SHOE
# Relevant area parameters
REL_COL_SHOE <- as.numeric(Sys.getenv("R_REL_COL_SHOE"))  # Relevant columns
REL_ROW_SHOE <- as.numeric(Sys.getenv("R_REL_ROW_SHOE"))  # Relevant rows
REL_X_CORD <- as.numeric(Sys.getenv("R_REL_X_CORD"))   # X coordinate range
REL_Y_CORD <- as.numeric(Sys.getenv("R_REL_Y_CORD"))    # Y coordinate range

rel_col_shoe <- REL_COL_SHOE
rel_row_shoe <- REL_ROW_SHOE
rel_x_cord <- REL_X_CORD
rel_Y_cord <- REL_Y_CORD

# =============================================================================
# DATA PATHS
# =============================================================================
# Input data files
CONTACTS_DATA_FILE <- paste0(ROOT_PATH, "Data/contacts_data.txt")
LOCATIONS_DATA_FILE <- paste0(ROOT_PATH, "Data/locations_data.csv")

# Contour data files (from Python pipeline)
CONTOUR_DATA_FILE <- paste0(ROOT_PATH, "shared_data/processing_data/list_contour.npy")

# Output directories (use shared_data for integration)
DATASET_DIR <- paste0(ROOT_PATH, "shared_data/")  # Shared between Python and R
SAVED_MODELS_DIR <- paste0(ROOT_PATH, "shared_data/saved_models/")

# Ensure output directories exist
dir.create(DATASET_DIR, recursive = TRUE, showWarnings = FALSE)
dir.create(SAVED_MODELS_DIR, recursive = TRUE, showWarnings = FALSE)

# =============================================================================
# REQUIRED LIBRARIES
# =============================================================================
required_packages <- c(
  "ggplot2", "dplyr", "Matrix",
  "splines", "survival"
)

# Function to install and load required packages
load_required_packages <- function(packages) {
  # Set user library path
  user_lib <- "~/R/library"
  if (!dir.exists(user_lib)) {
    dir.create(user_lib, recursive = TRUE)
  }
  .libPaths(c(user_lib, .libPaths()))

  for (pkg in packages) {
    if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
      message(paste("Installing package:", pkg, "to user library"))
      install.packages(pkg, dependencies = TRUE, lib = user_lib, repos = "https://cran.rstudio.com/")
      library(pkg, character.only = TRUE)
    }
  }
}

# Load all required packages
load_required_packages(required_packages)
#' Print current configuration
print_config <- function() {
  cat("=== Statistical Model Configuration ===\n")
  cat("Root Path:", ROOT_PATH, "\n")
  cat("Model Feature:", MODEL_FEATURE, "\n")
  cat("Shoe Dimensions:", COL_SHOE, "x", ROW_SHOE, "\n")
  cat("Number of Shoes:", NUM_SHOE, "\n")
  cat("Dataset Directory:", DATASET_DIR, "\n")
  cat("Models Directory:", SAVED_MODELS_DIR, "\n")
  cat("=======================================\n")
}

# Print configuration when loaded
print_config()

message("Configuration loaded successfully!")