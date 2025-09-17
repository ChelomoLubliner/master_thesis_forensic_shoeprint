# R script to convert markdown to PDF
# This script will convert the project_workflow_documentation.md to PDF

# Check if required packages are installed
required_packages <- c("rmarkdown", "knitr")

# Install missing packages
for(pkg in required_packages) {
  if(!require(pkg, character.only = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}

# Create a temporary Rmd file with the markdown content
temp_rmd <- "temp_workflow_documentation.Rmd"

# Read the markdown content
md_content <- readLines("project_workflow_documentation.md")

# Create the Rmd file with YAML header
rmd_content <- c(
  "---",
  "title: \"Shoe RAC Analysis Project - Complete Workflow Documentation\"",
  "author: \"Generated from Markdown\"",
  "date: \"`r Sys.Date()`\"",
  "output:",
  "  pdf_document:",
  "    toc: true",
  "    toc_depth: 3",
  "    number_sections: true",
  "    geometry: margin=1in",
  "    fontsize: 11pt",
  "---",
  "",
  "```{r setup, include=FALSE}",
  "knitr::opts_chunk$set(echo = TRUE, warning = FALSE, message = FALSE)",
  "```",
  "",
  md_content
)

# Write the Rmd file
writeLines(rmd_content, temp_rmd)

# Convert to PDF
tryCatch({
  rmarkdown::render(temp_rmd, output_format = "pdf_document")
  cat("PDF successfully created: temp_workflow_documentation.pdf\n")
}, error = function(e) {
  cat("Error creating PDF:", e$message, "\n")
  cat("Trying alternative method...\n")

  # Alternative: Try with html first, then convert
  tryCatch({
    rmarkdown::render(temp_rmd, output_format = "html_document")
    cat("HTML created successfully. You can print this to PDF from your browser.\n")
  }, error = function(e2) {
    cat("Error creating HTML:", e2$message, "\n")
  })
})

# Clean up temporary file
if(file.exists(temp_rmd)) {
  file.remove(temp_rmd)
}