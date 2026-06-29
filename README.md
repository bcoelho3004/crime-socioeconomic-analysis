# Socioeconomic Predictors of Urban Crime in Europe (2008–2023)

## Overview

This project investigates the relationship between socioeconomic conditions and urban crime rates across six European countries: Portugal, Spain, France, Germany, Italy, and the Netherlands.

Using panel data from Eurostat and the World Bank, statistical methods are applied to examine whether economic inequality, unemployment, GDP per capita, and urban density can explain variations in crime rates over time.

The study adopts a comparative, data-driven approach grounded in computational social science and policy analytics.

## Research Question

To what extent do socioeconomic factors explain variations in crime rates across European countries over time?

## Hypotheses

- H1: Higher unemployment is associated with higher crime rates
- H2: Higher inequality (Gini index) predicts higher crime
- H3: Higher GDP per capita is associated with lower crime
- H4: Urban density increases crime concentration

## Data Sources

| Variable | Source |
|---|---|
| Crime rate (intentional homicide per 100,000) | Eurostat |
| Unemployment rate (%) | Eurostat |
| GDP per capita (current US$) | World Bank |
| Gini index (inequality) | World Bank / OECD |
| Urban population (%) | World Bank |

## Countries Included

Portugal, Spain, France, Germany, Italy, Netherlands

**Time period:** 2008–2023 (varies by indicator availability)

## Methodology

1. Data collection and cleaning — construction of a harmonized panel dataset (country × year), handling missing values via interpolation
2. Exploratory Data Analysis (EDA) — correlation matrices, time series visualization, distribution analysis
3. Statistical modeling — multiple linear regression (OLS), with planned extension to fixed-effects panel models
4. Machine learning (optional extension) — Random Forest regression with feature importance analysis

## Tools

- Python (pandas, numpy, matplotlib, seaborn)
- Statsmodels (regression analysis)
- Scikit-learn (machine learning)
- Streamlit (interactive dashboard)

## Project Structure

The repository is organized as follows:

- `data/raw/` — Original datasets from Eurostat and World Bank
- `data/processed/` — Cleaned and merged datasets ready for analysis
- `notebooks/` — Jupyter notebooks for data collection, EDA, and modeling
- `src/` — Reusable Python functions for data processing and modeling
- `figures/` — Saved plots and visualizations
- `dashboard/` — Streamlit dashboard application
- `README.md` — Project documentation
- `requirements.txt` — Python dependencies


## Current Status

- [ ] Data collection and cleaning
- [ ] Exploratory data analysis
- [ ] Regression model
- [ ] Dashboard deployment

## Limitations

- Crime definitions vary across countries
- Missing data for certain years, particularly the Gini index
- Correlation does not imply causation
- National-level data may mask within-country variation

## Future Work

- Expand the analysis to Eastern European countries
- Add spatial regression models (GIS integration)
- Include social media sentiment as a predictor variable
- Deploy an interactive Streamlit dashboard
- Apply causal inference methods (e.g., Difference-in-Differences)

## Author

Undergraduate research project in Sociology, with a focus on computational social science, quantitative methods, and policy analytics.

*Part of a portfolio developed for MSc applications in Social Data Science.*
