Health and Population EDA: Kenya, South Africa, and Nigeria
Overview
This project explores and analyzes key health and population indicators for three African countries: Kenya, South Africa, and Nigeria. The focus is on understanding trends and distributions of life expectancy, health expenditure, overweight prevalence, and population growth using data from the Health, Nutrition, and Population Statistics (HNP) dataset.

The primary goal is to conduct an Exploratory Data Analysis (EDA) to uncover patterns and insights that can inform public health strategies and economic planning for these countries.

Key Indicators
The analysis focuses on the following key health indicators:

Life Expectancy at Birth (years): A critical measure of overall health and longevity.
Current Health Expenditure (% of GDP): An indicator of the amount spent on healthcare relative to the national economy.
Prevalence of Overweight (% of Adults): A measure of the percentage of adults who are classified as overweight, indicating nutrition and lifestyle trends.
Population Growth (Annual %): The annual rate of population growth, a demographic measure with wide-reaching implications.
Dataset
The data is sourced from the World Bank Health, Nutrition, and Population Statistics. The dataset contains historical health and population indicators for various countries.

Dataset Structure:
Country Name: The country the data is associated with (Kenya, South Africa, Nigeria).
Indicator Name: The health or population indicator being measured.
Year: The year the data point was recorded.
Value: The value of the indicator for a given year.
Project Structure
The project is organized into several key sections:

Data Wrangling: Cleaning and transforming the dataset for analysis.
Exploratory Data Analysis (EDA):
Trend Analysis: Visualization of trends over time for life expectancy and health expenditure.
Distribution Analysis: Histogram plots of life expectancy to observe country-wise distribution patterns.
Population Growth Trends: Line plots showing population growth over time.
Statistical Summary: Calculation of mean and standard deviation for each key indicator, giving a statistical overview of the dataset.
Correlation Analysis (Optional): Exploration of relationships between health expenditure, life expectancy, and population growth.
Visualizations
Trend Plots: Show how life expectancy and health expenditure have evolved over time in the three countries.
Distribution Plots: Display the distribution of life expectancy for Kenya, South Africa, and Nigeria.
Population Growth Trends: Illustrate the yearly growth in population for each country.
Installation & Usage
To run this project, ensure you have the following dependencies installed:

dplyr
ggplot2
tidyr
reshape2
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/health-population-eda.git
cd health-population-eda
Install required packages in R:

r
Copy code
install.packages(c("dplyr", "ggplot2", "tidyr", "reshape2"))
Running the Analysis
To run the analysis, open the R script in your R environment or IDE and run the commands step by step. The generated visualizations and statistical summaries will provide insights into the health indicators across the three countries.

Results
The analysis reveals several key insights:

Life Expectancy: South Africa has had the highest life expectancy, followed by Kenya and Nigeria.
Health Expenditure: South Africa consistently spends a higher percentage of its GDP on health compared to Kenya and Nigeria.
Population Growth: Nigeria shows a consistently higher population growth rate compared to Kenya and South Africa.
