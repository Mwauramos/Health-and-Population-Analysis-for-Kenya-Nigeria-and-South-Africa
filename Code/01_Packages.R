
# Load necessary libraries
library(tidyverse)  # For data tidying, transformation, and visualization
library(readxl)     # To read in Excel files
library(plotly)     # For interactive graphs
library(magrittr)   # Pipe operator for readable code
library(forecast)   # For cross-correlation (ggCcf function)
library(gridExtra)  # To combine multiple plots
library(corrplot)   # To visualize correlations

# Check if packages are installed, if not, install them
required_packages <- c("tidyverse", "readxl", "plotly", "magrittr", "forecast", "gridExtra", "corrplot")
new_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages)

# Load all packages
lapply(required_packages, library, character.only = TRUE)

# Confirm that the packages are successfully loaded
sessionInfo()  # Displays loaded packages and other session info
