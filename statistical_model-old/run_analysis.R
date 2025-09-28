#!/usr/bin/env Rscript

# Statistical Analysis Pipeline Runner
# This script executes the complete statistical analysis pipeline

# Load configuration
source("config.R")

# Function to execute R markdown files
execute_rmd <- function(file_path, output_dir = ".") {
  cat("Processing:", file_path, "\n")

  tryCatch({
    rmarkdown::render(
      file_path,
      output_dir = output_dir,
      quiet = TRUE
    )
    cat("✓ Completed:", file_path, "\n")
  }, error = function(e) {
    cat("✗ Error in:", file_path, "\n")
    cat("Error message:", e$message, "\n")
    stop(paste("Pipeline failed at:", file_path))
  })
}

# Main pipeline execution
main <- function() {
  cat("=== Starting Statistical Analysis Pipeline ===\n")
  cat("Configuration loaded from config.R\n")

  # Pipeline steps in order
  pipeline_steps <- c(
    "1_dataCC.Rmd",
    "2_dataCC_distance.Rmd",
    "3_calculate_shoe_distance.Rmd",
    "4_random_effect_model_standardization_of_shoe.Rmd",
    "5_output_and_results_standardization_of_shoe.Rmd",
    "6_statistical_tests.Rmd"
  )

  start_time <- Sys.time()

  for (step in pipeline_steps) {
    cat("\n--- Step:", step, "---\n")
    execute_rmd(step)
  }

  end_time <- Sys.time()
  execution_time <- difftime(end_time, start_time, units = "mins")

  cat("\n=== Pipeline Completed Successfully ===\n")
  cat("Total execution time:", round(execution_time, 2), "minutes\n")
  cat("Results saved in:", SAVED_MODELS_DIR, "\n")
}

# Execute main function if script is run directly
if (!interactive()) {
  main()
}