# Script: 
# Remove scientific notation for readability
options(scipen = 10)

# Load necessary libraries
library(readxl)
library(tidyverse)

# Read in the original Excel file from the same directory
file_path <- "HNP_StatsEXCEL.xlsx"
HNP <- read_excel(file_path, na = "..")

# Filter for Kenya, Nigeria, and South Africa, and select relevant columns for the years 2000-2023
HNP_filtered <- HNP %>%
  filter(`Country Code` %in% c('KEN', 'NGA', 'ZAF')) %>%
  select(`Country Name`, `Country Code`, `Indicator Name`, `Indicator Code`, `2000`:`2023`)

# Remove rows with more than 10 missing values (less than 50% missing data)
HNP_cleaned <- HNP_filtered[rowSums(is.na(HNP_filtered[, -c(1:4)])) <= 10, ]

# Reshape the data from wide to long format (years as rows instead of columns)
HNP_long <- HNP_cleaned %>%
  gather(Year, Value, `2000`:`2023`) %>%
  spread(`Indicator Name`, Value)

# Inspect the cleaned data
head(HNP_long)
