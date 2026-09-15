# Rossmann Sales Forecasting — Project 6 Final Submission

**Submitted by:** Satish Vonteddu  
**Program:** Data Analytics Internship — NextHikes IT Solutions  
**Batch:** L-110226-W2PM-B15  
**Submission Date:** 15 September 2026

## 🚀 Start Here

This repository contains the complete final submission for **Project 6 — Rossmann Sales Forecasting**.

### 🌐 Live Streamlit Application

https://rossmann-sales-forecasting-3ajs4nefpwuhytnxunnisq.streamlit.app

The application supports:

- Manual single-store prediction
- CSV-based batch prediction
- Predicted Sales
- Predicted Customers
- Prediction visualizations
- Batch prediction CSV download

---

## 📦 Final Submission

All evaluator-facing deliverables are available in:

`Final_Submission/`

### 📄 Documentation

- Final Professional PDF
- Final Professional DOCX

Location:

`Final_Submission/Documentation/`

### 📊 Presentation

Final 25-slide professional presentation.

Location:

`Final_Submission/Presentation/`

### 📓 Notebooks

The project includes five organized notebooks:

1. Data Loading & Cleaning
2. Exploratory Data Analysis
3. Machine Learning Sales Prediction
4. LSTM Time Series
5. MLflow Final Prediction

Location:

`Final_Submission/Notebooks/`

### 📈 Power BI

Final Power BI dashboard file:

`Final_Submission/PowerBI/Rossmann_Sales_Forecasting.pbix`

Dashboard evidence:

`Final_Submission/Evidence/PowerBI_Final_Dashboard_Evidence.png`

### 📁 Prediction Outputs

Final prediction files:

`Final_Submission/Predictions/`

### 🖼️ Evidence

Project implementation evidence includes:

- Power BI dashboard
- MLflow model versions
- Streamlit manual prediction
- Streamlit CSV batch prediction
- Prediction details

Location:

`Final_Submission/Evidence/`

### 📋 Official Project Brief

Location:

`Final_Submission/Project_Brief/`

---

## 📊 Project Overview

This project develops an end-to-end **Rossmann Sales Forecasting** solution covering:

- Exploratory Data Analysis
- Data cleaning and preprocessing
- Feature engineering
- Random Forest sales forecasting
- Customer-demand forecasting
- LSTM time-series forecasting
- MLflow experiment tracking and model serialization
- DVC data versioning
- Git and Git LFS
- Power BI business intelligence
- Streamlit deployment

---

## 🧠 Machine Learning Results

### Random Forest — Sales Forecasting

- **MAE:** 809.24
- **RMSE:** 1218.28
- **R²:** 0.8859

### Random Forest — Customer Forecasting

- **MAE:** 60.23
- **RMSE:** 91.12
- **R²:** 0.9562

### Multivariate LSTM — Daily Sales Forecasting

- **MAE:** 504,875.09
- **RMSE:** 669,092.44
- **R²:** 0.9451

### Final Test Predictions

**41,088 test records** were processed for the final prediction output.

> The Random Forest and LSTM metrics use different modelling granularities and should not be treated as a direct model-to-model comparison.

---

## 🔬 Exploratory Data Analysis

The EDA covers the major business questions specified in the project brief, including:

- Sales and customer purchasing behaviour
- Train/test distribution comparison
- Promotion impact
- Holiday and seasonal behaviour
- Christmas/Easter seasonality
- Sales and customer correlation
- Store opening/closing behaviour
- Weekday and weekend patterns
- Assortment impact
- Competition distance
- Competition-related data patterns

---

## 🤖 Deep Learning — LSTM

A dedicated time-series workflow was implemented using daily aggregated Rossmann sales.

The workflow includes:

- Stationarity testing
- ADF test
- ACF/PACF analysis
- Sliding-window creation
- Min-Max scaling
- LSTM regression
- Early stopping
- Multivariate time-series improvement using operational and day-of-week features

The final multivariate LSTM captured weekly sales patterns and Sunday trough behaviour more effectively than the initial univariate approach.

---

## ⚙️ MLOps

### MLflow

MLflow was used for:

- Experiment tracking
- Parameter logging
- Metric logging
- Model artifact logging
- Model loading for inference
- Model Registry versioning

Evidence:

`Final_Submission/Evidence/MLflow_Multiple_Model_Versions.png`

> MLflow Registry Version 2 represents a second registry release of the validated artifact; it is not presented as a newly retrained model.

### DVC

DVC was used for dataset versioning, including multiple versions of the training data.

### Git / Git LFS

GitHub is used for project version control, while Git LFS is used for large model artifacts.

---

## 📈 Power BI

A Power BI dashboard was created as the business intelligence layer of the project.

It includes:

- Sales KPIs
- Customer KPIs
- Store analysis
- Date analysis
- Store Type analysis
- Interactive slicers
- Business-oriented visualizations

Power BI file:

`Final_Submission/PowerBI/Rossmann_Sales_Forecasting.pbix`

---

## 🚀 Streamlit Deployment

The deployed application provides an end-to-end prediction interface.

### Live Application

https://rossmann-sales-forecasting-3ajs4nefpwuhytnxunnisq.streamlit.app

The application supports:

1. **Manual Prediction**
2. **CSV Batch Prediction**

The batch workflow provides:

- Input CSV upload
- Sales prediction
- Customer prediction
- Prediction charts
- Results table
- Downloadable prediction CSV

Application source:

`app.py`

---

## 📁 Repository Structure

```text
Rossmann-Sales-Forecasting/
│
├── README.md
├── app.py
├── requirements.txt
│
├── models/
├── notebooks/
│
├── .dvc/
├── .dvcignore
├── .gitattributes
├── .gitignore
│
└── Final_Submission/
    │
    ├── Documentation/
    ├── Presentation/
    ├── Notebooks/
    ├── PowerBI/
    ├── Predictions/
    ├── Evidence/
    └── Project_Brief/