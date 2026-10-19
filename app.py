
#Create a file named

from pathlib import Path

import pandas as pd
import streamlit as st

# Set up the dashboard page
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Retail Sales Forecasting and Analytics Dashboard")

# Find the outputs folder beside this app.py file
output_folder = Path(__file__).resolve().parent / "outputs"

# Check that the dashboard data files exist
required_files = [
    "historical_sales.csv",
    "sales_forecasts.csv",
    "holdout_results.csv"
]

missing_files = [
    name
    for name in required_files
    if not (output_folder / name).exists()
]

if missing_files:
    st.error("Missing files: " + ", ".join(missing_files))
    st.info("Complete Step 14 and place the outputs folder beside app.py.")
    st.stop()


# Cache the data so it does not reload on every interaction
@st.cache_data
def load_data(folder):
    history = pd.read_csv(
        folder / "historical_sales.csv",
        parse_dates=["date"]
    )

    forecast = pd.read_csv(
        folder / "sales_forecasts.csv",
        parse_dates=["date"]
    )

    holdout = pd.read_csv(
        folder / "holdout_results.csv",
        parse_dates=["date"]
    )

    return history, forecast, holdout


history, forecast, holdout = load_data(output_folder)

st.success("Dashboard data loaded successfully!")

# Display summary numbers
col1, col2, col3 = st.columns(3)

col1.metric("Number of stores", history["store"].nunique())
col2.metric("Number of items", history["item"].nunique())
col3.metric("Forecast records", f"{len(forecast):,}")

st.subheader("Forecast preview")
st.dataframe(forecast.head(10))












#Add store/item filters and sales graphs

# Sidebar filters
st.sidebar.header("Select store and item")

selected_store = st.sidebar.selectbox(
    "Store",
    sorted(history["store"].unique())
)

selected_item = st.sidebar.selectbox(
    "Item",
    sorted(history["item"].unique())
)

# Get historical sales for the selected store and item
filtered_history = history[
    (history["store"] == selected_store) &
    (history["item"] == selected_item)
].sort_values("date")

# Get forecasts for the same store and item
filtered_forecast = forecast[
    (forecast["store"] == selected_store) &
    (forecast["item"] == selected_item)
].sort_values("date")

st.subheader(
    f"Store {selected_store} — Item {selected_item}"
)

# Summary for the selected store and item
col1, col2 = st.columns(2)

col1.metric(
    "Historical units sold (2013–2017)",
    f"{filtered_history['sales'].sum():,.0f}"
)

col2.metric(
    "Forecast units (Jan–Mar 2018)",
    f"{filtered_forecast['predicted_sales'].sum():,.1f}"
)

# Historical sales graph
st.subheader("Historical daily sales")
st.caption("Actual units sold for the selected store and item.")

st.line_chart(
    filtered_history.set_index("date")[["sales"]]
)

# Future sales graph
st.subheader("Forecast daily sales: January–March 2018")
st.caption("Predicted units; actual sales for this period are unavailable.")

st.line_chart(
    filtered_forecast.set_index("date")[["predicted_sales"]]
)

# Forecast table
st.subheader("Forecast details")

st.dataframe(
    filtered_forecast[
        ["date", "store", "item", "predicted_sales"]
    ].reset_index(drop=True)
)




















#Show model performance in the dashboard

st.subheader("Model performance: October–December 2017")

st.caption(
    "Results from the holdout evaluation before final retraining. "
    "Lower MAE means better predictions."
)

# Select holdout records for the chosen store and item
filtered_holdout = holdout[
    (holdout["store"] == selected_store) &
    (holdout["item"] == selected_item)
].sort_values("date")

# Calculate average absolute errors
selected_model_mae = (
    filtered_holdout["actual_sales"]
    - filtered_holdout["predicted_sales"]
).abs().mean()

selected_baseline_mae = (
    filtered_holdout["actual_sales"]
    - filtered_holdout["baseline_sales"]
).abs().mean()

# Display the errors
col1, col2 = st.columns(2)

col1.metric(
    "Selected store/item: Model MAE",
    f"{selected_model_mae:.2f}"
)

col2.metric(
    "Selected store/item: Baseline MAE",
    f"{selected_baseline_mae:.2f}"
)

# Compare actual sales with both predictions
st.line_chart(
    filtered_holdout.set_index("date")[
        ["actual_sales", "predicted_sales", "baseline_sales"]
    ]
)














#Add a forecast download button
st.subheader("Download selected forecasts")

# Prepare the selected store and item's forecast table
download_data = filtered_forecast[
    ["date", "store", "item", "predicted_sales"]
].copy()

# Convert the table into CSV format
csv_data = download_data.to_csv(
    index=False,
    date_format="%Y-%m-%d"
).encode("utf-8")

# Display a download button
st.download_button(
    label="Download forecasts as CSV",
    data=csv_data,
    file_name=(
        f"forecast_store_{selected_store}"
        f"_item_{selected_item}.csv"
    ),
    mime="text/csv"
)