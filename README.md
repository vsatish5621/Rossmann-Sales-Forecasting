
# Rossmann Sales Forecasting

## Project Overview

An end-to-end machine learning project for forecasting Rossmann store sales and customer demand. The project combines exploratory data analysis, machine learning, deep learning, experiment tracking, data versioning, business intelligence, and a Streamlit prediction interface.

## Business Objective

Build a forecasting solution capable of predicting daily store sales up to six weeks ahead while considering factors such as promotions, competition, holidays, seasonality, store characteristics, and locality-related information.

## Dataset

The project uses the Rossmann dataset containing:
- train.csv
- test.csv
- store.csv
- sample_submission.csv

Training data contains 1,017,209 records and store data contains 1,115 stores.

## Project Workflow

1. Data loading and cleaning
2. Exploratory Data Analysis
3. Feature engineering
4. Random Forest sales prediction
5. Prediction interval estimation
6. LSTM time-series forecasting
7. Customer prediction
8. MLflow experiment tracking and model registry
9. DVC data versioning
10. Power BI dashboard
11. Streamlit prediction application

## Exploratory Data Analysis

The analysis examines:
- Sales and customer distributions
- Promotion effects
- Holiday effects
- Seasonal behavior
- Sales versus customers
- Store opening and closing behavior
- Store types and assortment
- Competition distance
- Competition-related information
- Weekend and weekday behavior

A strong positive relationship was observed between Sales and Customers, with correlation approximately 0.895.

## Machine Learning — Random Forest

A scikit-learn Pipeline was implemented with:
- Median imputation for numerical variables
- Most-frequent imputation for categorical variables
- One-hot encoding for categorical variables
- Random Forest Regressor

Chronological validation was used:
- Training: January 2013 to June 2015
- Validation: July 2015

### Sales Model Results

- MAE: 809.24
- RMSE: 1218.28
- R²: 0.8859

The model's strongest feature importance was associated with store operating status, followed by competition distance, promotion, and store information.

An approximate model-based prediction interval was also estimated using the variation among individual Random Forest trees. This is treated as an approximate uncertainty range rather than a formally calibrated confidence interval.

## Customer Prediction

A separate Random Forest model was developed to predict customer numbers.

Validation results:
- MAE: 60.23
- RMSE: 91.12
- R²: 0.9562

## Deep Learning — LSTM

Daily store sales were aggregated into a time series.

Stationarity was evaluated using the Augmented Dickey-Fuller test. The observed p-value was below 0.05, so first-order differencing was not required for this series.

ACF/PACF analysis showed clear weekly seasonality. A 28-day sliding window was therefore selected to cover approximately four weekly cycles.

### Multivariate LSTM

The improved LSTM used:
- Historical Sales
- Number of Open Stores
- Day of Week

Architecture:

Input sequence → LSTM(64) → Dropout(0.2) → Dense(1)

Training used:
- Adam optimizer
- Mean Squared Error loss
- Batch size: 32
- Maximum epochs: 30
- Early stopping
- Shuffle disabled for time-series ordering

### LSTM Results

- MAE: 504,875.09
- RMSE: 669,092.44
- R²: 0.9451

The LSTM validation results are based on daily aggregated sales, while the Random Forest sales model operates at store-day level; therefore, the metrics should not be interpreted as a direct apples-to-apples model comparison.

## MLflow

MLflow was used for experiment tracking and model management.

Experiment:
`Rossmann_Sales_Forecasting`

Tracked components include:
- Model parameters
- Validation metrics
- Random Forest model artifact
- LSTM model artifacts
- Customer model
- Inference validation

Registered model:
`Rossmann_Sales_Forecasting_RF`

Multiple registry versions were created for the validated Random Forest artifact. Registry Version 2 represents a second model registry release and does not imply retraining.

## DVC

DVC was used for dataset version control.

Documented data versions:
- Version 1 — original Rossmann datasets
- Version 2 — prepared training dataset

The Git history and DVC metadata demonstrate that `train.csv` changed between the two versions.

## Power BI

A Power BI dashboard was developed using a star-schema approach with:
- FactSales
- DimDate
- DimStore

The dashboard includes sales, customers, store counts, average sales per customer, time analysis, store-type analysis, and interactive slicers.

## Streamlit Application

A Streamlit web interface was developed for interactive predictions.

Inputs include:
- Store ID
- Prediction date
- Store status
- Promotion
- State holiday
- School holiday
- Store type
- Assortment
- Competition distance
- Competition opening information
- Promo2 information

The application predicts:
- Sales
- Customers

It also provides prediction details and CSV download functionality.

## Project Structure

```text
Rossmann-Sales-Forecasting/
├── .dvc/
├── .dvcignore
├── .gitignore
├── app.py
├── train.csv.dvc
├── test.csv.dvc
├── store.csv.dvc
├── sample_submission.csv.dvc
└── LICENSE

