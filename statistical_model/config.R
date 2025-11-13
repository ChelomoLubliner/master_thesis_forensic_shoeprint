# config.R
# This file is located at: master_thesis_forensic_shoeprint/statistical_model/config.R
# ROOT_PATH points to: master_thesis_forensic_shoeprint/

if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
  # Get the directory where config.R is located, then go up one level
  ROOT_PATH <- dirname(dirname(rstudioapi::getSourceEditorContext()$path))
} else {
  # Fallback: assume we're in statistical_model folder
  ROOT_PATH <- dirname(getwd())
}

ROOT_PATH <- paste(ROOT_PATH, "/", sep = "")
CONTOUR_ALGORITHM <- "Active_Contour"
IMAGE_NUMBER <- "171"
# 171/ 135
MODEL_FEATURE <- "NEW_X_NS_XY_RELATIVE"
# "NEW_X_NS_XY"
# "NS_XY"

