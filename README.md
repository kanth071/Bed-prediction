# 🏥 Hospital Bed Demand Forecasting

## Project Overview

This project forecasts hospital bed demand across **three sectors** — ICU, Emergency, and General Ward — using machine learning models. It includes a complete data preprocessing pipeline, three forecasting models, and an interactive Streamlit dashboard.

---

## 📁 Project Structure

```
Hospital-Bed-Demand-Forecasting/
│
├── data/
│   ├── raw/                          # Raw CSV datasets
│   ├── processed/                    # Cleaned & merged dataset
│   └── predictions/                  # Model forecast outputs
│
├── models/
│   ├── icu_xgboost.pkl              # Trained ICU XGBoost model
│   ├── emergency_prophet.pkl         # Trained Emergency Prophet model
│   └── general_randomforest.pkl      # Trained General Random Forest model
│
├── notebooks/
│   ├── preprocessing.ipynb           # Data preprocessing notebook
│   ├── eda.ipynb                     # Exploratory Data Analysis
│   ├── icu_model.ipynb              # ICU model training notebook
│   ├── emergency_model.ipynb         # Emergency model training notebook
│   └── general_model.ipynb           # General model training notebook
│
├── dashboard/
│   ├── app.py                        # Streamlit dashboard main app
│   ├── charts.py                     # Plotly chart functions
│   ├── sidebar.py                    # Sidebar filter components
│   └── utils.py                      # Utility/helper functions
│
├── pipeline/
│   ├── preprocessing_pipeline.py     # Data preprocessing pipeline
│   ├── forecasting_pipeline.py       # Model training pipeline
│   └── master_pipeline.py            # Master orchestration pipeline
│
├── reports/
│   └── project_report.pdf            # Final project report
│
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── main.py                          # Main entry point
```

---

## 🔧 Installation

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Place Raw Data

Place the following CSV files in `data/raw/`:
- `hospital_insights_summary.csv`
- `healthcare_analytics_patient_flow_data.csv`
- `dataset3.csv`

### 2. Run Preprocessing Pipeline

```bash
python -m pipeline.preprocessing_pipeline
```

### 3. Run Full Pipeline (Preprocessing + Model Training)

```bash
python main.py
```

### 4. Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 🤖 Models

| Model | Sector | Algorithm | Key Metric |
|-------|--------|-----------|------------|
| ICU Model | ICU | XGBRegressor | R² Score |
| Emergency Model | Emergency | Prophet | MAPE |
| General Model | General Ward | Random Forest | R² Score + OOB Score |

---

## 📊 Dashboard Features

- **Key Metrics**: Total admissions, avg bed occupancy, staff count, avg stay
- **Admissions Trend**: Line chart showing daily admissions
- **Bed Occupancy**: Area chart of occupancy over time
- **Sector Demand**: Grouped bar chart comparing ICU, Emergency, General demands
- **14-Day Forecast**: Emergency demand forecast with confidence intervals
- **Filters**: Sector selection and date range filtering

---

## 📦 Datasets Used

1. **Hospital Insights Summary** — Weekly hospital service data
2. **Healthcare Analytics Patient Flow** — Patient admission records
3. **Dataset 3** — Hourly hospital metrics (admissions, discharges, flu cases)

---

## 👤 Author

Pulipaka Lakshmi Kanth

---
