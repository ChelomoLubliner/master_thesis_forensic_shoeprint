knitr::opts_chunk$set(echo = TRUE)

# Load centralized configuration
source("config.R")

# Load data using config variables
file_name <- paste(DATASET_DIR, "dataCC_distance.csv", sep = "")
dataCC<- read.csv(file_name,header=TRUE)
dataCC <- subset(dataCC, select = c("n_Acc","x","y","shoe","row_number","horiz_dist"))
file_name <- paste(ROOT_PATH,"Data/all_cont.csv", sep = "")
allcont<- read.csv(file_name,header=TRUE)

# Data is already prepared with x, y, horiz_dist, min_dist
# No need for arbitrary shoe 135 contour processing
message("Data ready for statistical modeling with variables: x, y, horiz_dist, min_dist")

Random<-function(nknotsx=3,nknotsy=5,dat=dataCC,model_feat = MODEL_FEATURE, initial_values )
{
  
  common_formula <- as.formula("n_Acc ~ (1 | shoe)")
  
  
  knotsx <- as.numeric(quantile(dat$x,1:nknotsx/(1+nknotsx)))
  knots_new_x <- as.numeric(quantile(dat$new_x,1:nknotsx/(1+nknotsx)))
  knotsy <-as.numeric(quantile(dat$y,1:nknotsy/(1+nknotsy)))
  knots_distance <-as.numeric(quantile(dat$min_dist,1:2/(3)))
  shoe<-dat$shoe
  
  
  if(model_feat == 'NS_XY'){
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + (1 | shoe) "}
  else if(model_feat == 'NEW_X_NS_XY'){
            formula_text <- "n_Acc ~ ns(dat$new_x,knots=knots_new_x):ns(dat$y,knots=knotsy) + (1 | shoe) "}
  else if(model_feat == 'NS_MIN'){
            formula_text <- "n_Acc ~ ns(dat$min_dist,knots=knots_distance) + (1 | shoe) "}
  else if(model_feat == 'EMPTY_MODEL'){
            formula_text <- "n_Acc ~ (1 | shoe) "}
  else if(model_feat == 'NS_HORIZ'){
            formula_text <- "n_Acc ~ ns(dat$horiz_dist,knots=knots_distance) + (1 | shoe) "}
  else if(model_feat == 'HORIZ_DIST'){
            formula_text <- "n_Acc ~ dat$horiz_dist + (1 | shoe)"}
  else if(model_feat == 'MIN_DIST'){
            formula_text <- "n_Acc ~ dat$min_dist + (1 | shoe)"}
  else if(model_feat == 'HORIZ_BIN_CAT'){
            formula_text <- "n_Acc ~ dat$horiz_dist_cat + (1 | shoe)"}
  else if(model_feat == 'MIN_BIN_CAT'){
            formula_text <- "n_Acc ~ dat$min_dist_cat + (1 | shoe)"}
  else if(model_feat == 'NS_XY_HORIZ_DIST'){
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + dat$horiz_dist + (1 | shoe) "}
  else if(model_feat == 'NS_XY_MIN_DIST'){
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + dat$min_dist + (1 | shoe) "}
  else if(model_feat == 'NS_XY_HORIZ_BIN_CAT'){
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + dat$horiz_dist_cat + (1 | shoe) "}
    else if(model_feat == 'NS_XY_HORIZ_DUMMY'){
      dat$dummy_0to1 <- as.numeric(dat$horiz_dist <= 0.05)#0.05-0.1
      dat$dummy_1to2 <- as.numeric(dat$horiz_dist > 0.05 & dat$horiz_dist <= 0.1)
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + dat$dummy_0to1 + dat$dummy_1to2 +  (1 | shoe) "
    }
  else if(model_feat == 'NS_XY_MIN_DUMMY'){
      dat$dummy_0to1 <- as.numeric(dat$min_dist <= 0.05)
      dat$dummy_1to2 <- as.numeric(dat$min_dist > 0.05 & dat$min_dist <= 0.1)
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + dat$dummy_0to1 + dat$dummy_1to2 +  (1 | shoe) "
            }
  else if(model_feat == 'NS_XY_MIN_BIN_CAT'){
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + dat$min_dist_cat + (1 | shoe) "}
    else if(model_feat == 'NS_XY_NS_HORIZ'){
            formula_text <- "n_Acc ~ ns(dat$x,knots=knotsx):ns(dat$y,knots=knotsy) + ns(dat$horiz_dist,knots=knots_distance) + (1 | shoe) "}
  else { stop("Invalid model_feat value")}
  cat(formula_text)
  est_formula <- as.formula(formula_text)  
  initial_values <- c(parameter1 = 0)  # Adjust these values
  est<- glmer(est_formula, data = dat, family = binomial(link = "logit"), control =glmerControl(optimizer="nlminbwrap"))#,  start = initial_values)
  #est<- glmer(est_formula, data = dat, family = binomial(link = "logit"), control =glmerControl(optimizer="bobyqa"))nlminbwrap
  cat("file_saving")
  file_name <- paste(SAVED_MODELS_DIR, MODEL_FEATURE,"_RELATIVE.rds", sep = "")
  saveRDS(est, file = file_name)
  return(est)
}
get_initial_values <- function(){
  file_name <- paste(SAVED_MODELS_DIR, "NS_XY.rds", sep = "")
  naomi_model <- readRDS(file = file_name)
  fixed_effects <- fixef(naomi_model) # View the fixed effects coefficients print(fixed_effects) 
  vals <- as.list(fixed_effects)
  if (grepl("DUMMY", MODEL_FEATURE)){ 
  vals <- c(vals, list(dummy_0to1 = 0, dummy_1to2 = 0))}
  else if (grepl("BIN_CAT", MODEL_FEATURE)){
    vals <- c(vals, list(bin_cat = 0))
  }
  return(vals) 
}

rand<-Random(dat=dataCC,initial_values=get_initial_values())
