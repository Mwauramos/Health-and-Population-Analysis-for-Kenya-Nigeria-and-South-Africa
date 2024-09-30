# Load necessary libraries
library(dplyr)
library(ggplot2)
library(tidyr)
library(reshape2)

# Define countries of interest
countries <- c("Kenya", "South Africa", "Nigeria")

# Filter the dataset for the selected countries
regr <- filter(HNP, `Country Name` %in% countries)

# Select relevant indicators for the analysis
regr <- regr %>%
  filter(`Indicator Name` %in% c("Life expectancy at birth, total (years)", 
                                 "Prevalence of overweight (% of adults)", 
                                 "Current health expenditure (% of GDP)", 
                                 "Population growth (annual %)"))

# Reshape data into long format for easier analysis
regr_long <- regr %>%
  gather(key = "Year", value = "Value", -c(`Country Name`, `Indicator Name`, `Country Code`, `Indicator Code`))

# Convert the Year column to numeric
regr_long$Year <- as.numeric(regr_long$Year)

# Summarize data for life expectancy and health expenditure
summary_stats <- regr_long %>%
  filter(`Indicator Name` %in% c("Life expectancy at birth, total (years)", 
                                 "Current health expenditure (% of GDP)")) %>%
  group_by(`Country Name`, `Indicator Name`) %>%
  summarise(mean_value = mean(Value, na.rm = TRUE),
            sd_value = sd(Value, na.rm = TRUE), .groups = "drop")

# View summary statistics
print(summary_stats)

# Plot trends over time for life expectancy and health expenditure
regr_trend <- regr_long %>%
  filter(`Indicator Name` %in% c("Life expectancy at birth, total (years)", 
                                 "Current health expenditure (% of GDP)")) %>%
  filter(!is.na(Value))

# Trends over time for life expectancy and health expenditure
ggplot(regr_trend, aes(x = Year, y = Value, color = `Country Name`)) +
  geom_line(size = 1.2) +
  facet_wrap(~ `Indicator Name`, scales = "free_y") +
  theme_minimal(base_size = 14) +
  labs(title = "Trends of Life Expectancy and Health Expenditure Over Time",
       y = "Value", x = "Year") +
  theme(legend.position = "bottom", plot.title = element_text(hjust = 0.5))

# Define life expectancy data for distribution plot
life_exp_data <- regr_long %>%
  filter(`Indicator Name` == "Life expectancy at birth, total (years)") %>%
  filter(!is.na(Value))

# Plot distribution of Life Expectancy
ggplot(life_exp_data, aes(x = Value, fill = `Country Name`)) +
  geom_histogram(binwidth = 1, position = "dodge") +
  theme_minimal(base_size = 14) +
  labs(title = "Distribution of Life Expectancy in Kenya, South Africa, and Nigeria", 
       x = "Life Expectancy (Years)", y = "Count") +
  theme(legend.position = "bottom", plot.title = element_text(hjust = 0.5))

# Population growth trend plot
pop_growth_trend <- regr_long %>%
  filter(`Indicator Name` == "Population growth (annual %)") %>%
  filter(!is.na(Value))

# Plot Population Growth Trends
ggplot(pop_growth_trend, aes(x = Year, y = Value, color = `Country Name`)) +
  geom_line(size = 1.2) +
  theme_minimal(base_size = 14) +
  labs(title = "Population Growth Trend (Annual %)", 
       y = "Population Growth (%)", x = "Year") +
  theme(legend.position = "bottom", plot.title = element_text(hjust = 0.5))
