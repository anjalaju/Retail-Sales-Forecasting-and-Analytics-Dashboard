# Retail Sales Forecasting and Analytics Dashboard

A machine learning project that analyses historical retail sales,
predicts daily sales, and displays results in a Streamlit dashboard.

## Project Goal

Predict daily units sold for each store and item to support
inventory planning.

## Dataset

- Historical period: January 2013–December 2017
- Historical records: 913,000
- Stores: 10
- Items: 50
- Forecast period: January–March 2018
- Forecast records: 45,000

Historical columns: date, store, item, sales.
Test columns: id, date, store, item.

## Tools Used

- Python
- Pandas
- Matplotlib
- Scikit-learn
- Joblib
- Streamlit

## Project Workflow

1. Load and inspect the data.
2. Check missing values, duplicates, and date continuity.
3. Explore sales trends and patterns.
4. Create calendar and historical sales features.
5. Split historical data chronologically.
6. Evaluate a seasonal baseline.
7. Train and tune HistGradientBoostingRegressor.
8. Evaluate the selected model on untouched holdout data.
9. Retrain using all eligible historical records.
10. Predict January–March 2018 sales.
11. Save results and build the dashboard.

## Model Features

- store
- item
- year
- month
- day_of_week
- day_of_month
- is_weekend
- time_index
- lag_364
- past_year_mean_28

Historical features use sales available before the forecast period.

## Evaluation

Training records precede July 5, 2017.
Validation covers July 5–October 2, 2017.
Holdout evaluation covers October 3–December 31, 2017.

The baseline predicts sales using the same store and item's
sales from 364 days earlier.

| Method | Validation MAE | Holdout MAE |
|---|---:|---:|
| Seasonal baseline | 9.20 | 8.35 |
| Selected model: 200 rounds | 6.68 | 6.11 |

The selected model reduced holdout MAE by approximately 26.8%
compared with the baseline.

MAE measures the average absolute error in units per store-item-day.
Lower values indicate better predictions.

Holdout results were measured before final retraining.
Actual sales are unavailable in the provided 2018 test data,
so forecast-period accuracy cannot be calculated.

## Dashboard Features

- Store and item selection
- Historical sales charts
- Future sales forecasts
- Selected store/item sales summaries
- Holdout actual-versus-predicted comparisons
- Model and baseline MAE
- Forecast CSV downloads

## Required Dashboard Files

Place app.py and requirements.txt in the project folder.

Inside an outputs folder beside app.py, include:

- historical_sales.csv
- sales_forecasts.csv
- holdout_results.csv

The dashboard displays saved results and does not retrain the model.

## Run the Dashboard

Install dependencies:

    python -m pip install -r requirements.txt

Start the application:

    python -m streamlit run app.py

## Training Notebook

The notebook contains data analysis, feature engineering,
model training, evaluation, and forecast generation.

To run the notebook, its additional dependencies include
scikit-learn, matplotlib, and joblib, along with pandas.

## Limitations

- Forecasts are estimates, not guaranteed sales.
- The dataset does not include prices, promotions, or inventory.
- The dashboard's saved forecasts cover January–March 2018.
- Forecasting later periods requires updated historical data
  and newly generated features and predictions.