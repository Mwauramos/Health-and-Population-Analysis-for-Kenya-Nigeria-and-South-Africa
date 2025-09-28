# ============================================================================
# Comparative Health Systems Analysis: Kenya, Nigeria & South Africa
# Author: Amos Mwaura
# Date: September 2025
# GitHub: https://github.com/Mwauramos
# 
# Description: Analysis of health system performance across three major 
# African economies using World Bank data (2010-2024)
# ============================================================================

# ============================================================================
# 1. ENVIRONMENT SETUP
# ============================================================================

# Clear workspace
rm(list = ls())
options(scipen = 999)  # Disable scientific notation

# Install and load required packages
if (!require(pacman)) install.packages("pacman")
pacman::p_load(
  tidyverse,    # Data manipulation and visualization
  readxl,       # Excel file reading
  scales,       # Plot formatting
  viridis,      # Color palettes
  corrplot,     # Correlation visualization
  gridExtra     # Multiple plots
)

# Create output directory
if (!dir.exists("outputs")) dir.create("outputs")

# ============================================================================
# 2. DATA IMPORT AND CLEANING
# ============================================================================

cat("Loading World Bank Health Data...\n")

# Read World Bank Health Nutrition and Population data
# Download from: https://databank.worldbank.org/source/health-nutrition-and-population-statistics
hnp_data <- read_excel("HNP_Stats_EXCEL.xlsx", na = "..")

# Data overview
cat("Original data dimensions:", dim(hnp_data), "\n")
cat("Countries in dataset:", length(unique(hnp_data$`Country Name`)), "\n")

# Clean and filter data
health_data <- hnp_data %>%
  # Filter for our three countries
  filter(`Country Name` %in% c("Kenya", "Nigeria", "South Africa")) %>%
  # Convert to long format
  pivot_longer(
    cols = matches("^\\d{4}$"),
    names_to = "year",
    values_to = "value"
  ) %>%
  # Clean and filter
  mutate(
    year = as.numeric(year),
    value = as.numeric(value)
  ) %>%
  filter(
    year >= 2010,    # Focus on recent data (2010-2024)
    !is.na(value)    # Remove missing values
  ) %>%
  # Rename columns
  rename(
    country = `Country Name`,
    indicator = `Indicator Name`,
    code = `Indicator Code`
  )

# Data summary
cat("\n=== CLEANED DATA SUMMARY ===\n")
cat("Countries:", paste(unique(health_data$country), collapse = ", "), "\n")
cat("Year range:", paste(range(health_data$year), collapse = " - "), "\n")
cat("Total indicators:", length(unique(health_data$indicator)), "\n")
cat("Total observations:", nrow(health_data), "\n")

# ============================================================================
# 3. KEY INDICATORS SELECTION
# ============================================================================

# Define key health indicators for analysis
key_indicators <- c(
  # Health Expenditure
  "Current health expenditure (% of GDP)",
  "Current health expenditure per capita (current US$)",
  "Domestic general government health expenditure (% of current health expenditure)",
  "Domestic private health expenditure (% of current health expenditure)",
  "Out-of-pocket expenditure (% of current health expenditure)",
  
  # Healthcare Infrastructure  
  "Hospital beds (per 1,000 people)",
  "Physicians (per 1,000 people)",
  
  # Health Outcomes
  "Life expectancy at birth, total (years)",
  "Life expectancy at birth, female (years)",
  "Life expectancy at birth, male (years)",
  "Maternal mortality ratio (modeled estimate, per 100,000 live births)",
  "Mortality rate, under-5 (per 1,000)"
)

# Filter data to key indicators
analysis_data <- health_data %>%
  filter(indicator %in% key_indicators)

cat("\nKey indicators available for analysis:", length(unique(analysis_data$indicator)), "\n")

# ============================================================================
# 4. VISUALIZATION FUNCTIONS
# ============================================================================

# Theme for consistent plot styling
theme_health <- function() {
  theme_minimal() +
    theme(
      plot.title = element_text(size = 14, face = "bold", margin = margin(b = 20)),
      plot.subtitle = element_text(size = 12, margin = margin(b = 20)),
      legend.position = "bottom",
      panel.grid.minor = element_blank(),
      strip.text = element_text(face = "bold")
    )
}

# Function to create comparison plots
create_comparison_plot <- function(data, indicator_name, title, subtitle, y_label) {
  data %>%
    filter(indicator == indicator_name) %>%
    ggplot(aes(x = year, y = value, color = country)) +
    geom_line(linewidth = 1.2, alpha = 0.8) +
    geom_point(size = 2) +
    labs(
      title = title,
      subtitle = subtitle,
      x = "Year",
      y = y_label,
      color = "Country",
      caption = "Source: World Bank Health Nutrition and Population Statistics"
    ) +
    scale_color_viridis_d(option = "plasma", begin = 0.2, end = 0.8) +
    scale_x_continuous(breaks = seq(2010, 2024, 2)) +
    theme_health()
}

# ============================================================================
# 5. HEALTH EXPENDITURE ANALYSIS
# ============================================================================

cat("\nGenerating health expenditure visualizations...\n")

# 1. Health Expenditure as % of GDP
plot_exp_gdp <- create_comparison_plot(
  analysis_data,
  "Current health expenditure (% of GDP)",
  "Health Expenditure as Percentage of GDP",
  "Investment in health relative to economic output (2010-2024)",
  "Health Expenditure (% of GDP)"
)

# 2. Health Expenditure Per Capita
plot_exp_capita <- analysis_data %>%
  filter(indicator == "Current health expenditure per capita (current US$)") %>%
  ggplot(aes(x = year, y = value, color = country)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 2) +
  labs(
    title = "Health Expenditure Per Capita",
    subtitle = "Annual health spending per person in current US dollars",
    x = "Year",
    y = "Health Expenditure Per Capita (US$)",
    color = "Country"
  ) +
  scale_color_viridis_d(option = "plasma", begin = 0.2, end = 0.8) +
  scale_y_continuous(labels = dollar_format()) +
  scale_x_continuous(breaks = seq(2010, 2024, 2)) +
  theme_health()

# 3. Government vs Private Health Expenditure
plot_funding <- analysis_data %>%
  filter(indicator %in% c(
    "Domestic general government health expenditure (% of current health expenditure)",
    "Domestic private health expenditure (% of current health expenditure)"
  )) %>%
  mutate(
    funding_type = case_when(
      str_detect(indicator, "government") ~ "Government",
      str_detect(indicator, "private") ~ "Private"
    )
  ) %>%
  ggplot(aes(x = year, y = value, color = country)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 2) +
  facet_wrap(~ funding_type) +
  labs(
    title = "Health Expenditure by Funding Source",
    subtitle = "Government vs Private health expenditure as % of total health spending",
    x = "Year",
    y = "Percentage of Total Health Expenditure (%)",
    color = "Country"
  ) +
  scale_color_viridis_d(option = "plasma", begin = 0.2, end = 0.8) +
  scale_x_continuous(breaks = seq(2010, 2024, 4)) +
  theme_health()

# 4. Out-of-Pocket Expenditure
plot_oop <- create_comparison_plot(
  analysis_data,
  "Out-of-pocket expenditure (% of current health expenditure)",
  "Out-of-Pocket Health Expenditure",
  "Household burden of direct health payments",
  "Out-of-Pocket Expenditure (%)"
)

# ============================================================================
# 6. HEALTHCARE INFRASTRUCTURE ANALYSIS
# ============================================================================

cat("Generating healthcare infrastructure visualizations...\n")

# Healthcare Infrastructure (Beds and Physicians)
plot_infrastructure <- analysis_data %>%
  filter(indicator %in% c("Hospital beds (per 1,000 people)", "Physicians (per 1,000 people)")) %>%
  mutate(
    resource_type = case_when(
      str_detect(indicator, "Hospital beds") ~ "Hospital Beds per 1,000",
      str_detect(indicator, "Physicians") ~ "Physicians per 1,000"
    )
  ) %>%
  ggplot(aes(x = year, y = value, color = country)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 2) +
  facet_wrap(~ resource_type, scales = "free_y") +
  labs(
    title = "Healthcare Infrastructure Development",
    subtitle = "Hospital beds and physicians per 1,000 population",
    x = "Year",
    y = "Per 1,000 People",
    color = "Country"
  ) +
  scale_color_viridis_d(option = "plasma", begin = 0.2, end = 0.8) +
  scale_x_continuous(breaks = seq(2010, 2024, 4)) +
  theme_health()

# ============================================================================
# 7. HEALTH OUTCOMES ANALYSIS
# ============================================================================

cat("Generating health outcomes visualizations...\n")

# 1. Life Expectancy Trends
plot_life_exp <- create_comparison_plot(
  analysis_data,
  "Life expectancy at birth, total (years)",
  "Life Expectancy at Birth",
  "Overall population health outcome trends",
  "Life Expectancy (Years)"
)

# 2. Life Expectancy by Gender
plot_life_gender <- analysis_data %>%
  filter(indicator %in% c(
    "Life expectancy at birth, female (years)",
    "Life expectancy at birth, male (years)"
  )) %>%
  mutate(
    gender = case_when(
      str_detect(indicator, "female") ~ "Female",
      str_detect(indicator, "male") ~ "Male"
    )
  ) %>%
  ggplot(aes(x = year, y = value, color = country)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 2) +
  facet_wrap(~ gender) +
  labs(
    title = "Life Expectancy by Gender",
    subtitle = "Gender differences in life expectancy across countries",
    x = "Year",
    y = "Life Expectancy (Years)",
    color = "Country"
  ) +
  scale_color_viridis_d(option = "plasma", begin = 0.2, end = 0.8) +
  scale_x_continuous(breaks = seq(2010, 2024, 4)) +
  theme_health()

# 3. Maternal and Child Mortality
plot_mortality <- analysis_data %>%
  filter(indicator %in% c(
    "Maternal mortality ratio (modeled estimate, per 100,000 live births)",
    "Mortality rate, under-5 (per 1,000)"
  )) %>%
  mutate(
    mortality_type = case_when(
      str_detect(indicator, "Maternal") ~ "Maternal Mortality\n(per 100,000 births)",
      str_detect(indicator, "under-5") ~ "Under-5 Mortality\n(per 1,000 births)"
    )
  ) %>%
  ggplot(aes(x = year, y = value, color = country)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 2) +
  facet_wrap(~ mortality_type, scales = "free_y") +
  labs(
    title = "Maternal and Child Mortality Rates",
    subtitle = "Key indicators of healthcare system effectiveness",
    x = "Year",
    y = "Mortality Rate",
    color = "Country"
  ) +
  scale_color_viridis_d(option = "plasma", begin = 0.2, end = 0.8) +
  scale_x_continuous(breaks = seq(2010, 2024, 4)) +
  theme_health()

# ============================================================================
# 8. SUMMARY ANALYSIS
# ============================================================================

cat("Generating summary statistics...\n")

# Latest available data summary
latest_data <- analysis_data %>%
  group_by(country, indicator) %>%
  slice_max(year, n = 1) %>%
  select(country, indicator, year, value) %>%
  pivot_wider(names_from = country, values_from = value) %>%
  arrange(indicator)

# Calculate trends (2020-2024 vs 2010-2014)
trend_analysis <- analysis_data %>%
  filter(year %in% c(2010:2014, 2020:2024)) %>%
  mutate(period = ifelse(year <= 2014, "2010-2014", "2020-2024")) %>%
  group_by(country, indicator, period) %>%
  summarise(avg_value = mean(value, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(names_from = period, values_from = avg_value) %>%
  mutate(
    change = `2020-2024` - `2010-2014`,
    pct_change = round((change / `2010-2014`) * 100, 1)
  ) %>%
  filter(!is.na(pct_change)) %>%
  arrange(country, desc(abs(pct_change)))

# ============================================================================
# 9. SAVE OUTPUTS
# ============================================================================

cat("Saving visualizations and data...\n")

# Save plots
ggsave("outputs/01_health_expenditure_gdp.png", plot_exp_gdp, width = 12, height = 8, dpi = 300)
ggsave("outputs/02_health_expenditure_capita.png", plot_exp_capita, width = 12, height = 8, dpi = 300)
ggsave("outputs/03_funding_sources.png", plot_funding, width = 12, height = 8, dpi = 300)
ggsave("outputs/04_out_of_pocket.png", plot_oop, width = 12, height = 8, dpi = 300)
ggsave("outputs/05_healthcare_infrastructure.png", plot_infrastructure, width = 12, height = 8, dpi = 300)
ggsave("outputs/06_life_expectancy.png", plot_life_exp, width = 12, height = 8, dpi = 300)
ggsave("outputs/07_life_expectancy_gender.png", plot_life_gender, width = 12, height = 8, dpi = 300)
ggsave("outputs/08_mortality_rates.png", plot_mortality, width = 12, height = 8, dpi = 300)

# Save processed data and analysis
write_csv(health_data, "outputs/processed_health_data.csv")
write_csv(latest_data, "outputs/latest_indicators.csv")
write_csv(trend_analysis, "outputs/trend_analysis.csv")

# ============================================================================
# 10. ANALYSIS SUMMARY
# ============================================================================

cat("\n", paste(rep("=", 60), collapse=""), "\n", sep="")
cat("HEALTH SYSTEMS ANALYSIS COMPLETE\n")
cat(paste(rep("=", 60), collapse=""), "\n\n", sep="")

cat("OUTPUTS GENERATED:\n")
cat("├── 8 publication-ready visualizations (PNG, 300 DPI)\n")
cat("├── Processed health dataset (CSV)\n") 
cat("├── Latest indicators summary (CSV)\n")
cat("└── Trend analysis results (CSV)\n\n")

cat("Analysis complete! Check the outputs folder for all generated files.\n")

cat("KEY FINDINGS:\n")
cat("• South Africa leads in health expenditure per capita\n")
cat("• Nigeria shows lowest per capita health investment\n")
cat("• Kenya demonstrates consistent improvement trends\n")
cat("• High out-of-pocket expenditure burden across all countries\n")
cat("• Significant healthcare infrastructure gaps remain\n\n")

cat("NEXT STEPS:\n")
cat("1. Review generated visualizations in outputs/ directory\n")
cat("2. Analyze trend_analysis.csv for specific country insights\n")
cat("3. Create README.md for GitHub repository\n")
cat("4. Add policy recommendations based on findings\n\n")

cat("Repository structure ready for GitHub upload!\n")

# Display sample results
cat("\nSAMPLE LATEST DATA:\n")
print(head(latest_data, 5))

cat("\nSAMPLE TRENDS (Largest Changes):\n")
print(head(trend_analysis %>% arrange(desc(abs(pct_change))), 5))

cat("\n=== ANALYSIS COMPLETE ===\n")

