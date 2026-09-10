import streamlit as st
import pandas as pd
import joblib


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Rossmann Sales Forecasting",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# LOAD TRAINED MODELS
# =========================================================

@st.cache_resource
def load_models():

    sales_model = joblib.load(
        "models/rossmann_random_forest_20260909_084440.joblib"
    )

    customer_model = joblib.load(
        "models/rossmann_customer_random_forest_20260909_105310.joblib"
    )

    return sales_model, customer_model


sales_model, customer_model = load_models()


# =========================================================
# APPLICATION TITLE
# =========================================================

st.title("📊 Rossmann Sales Forecasting")

st.write(
    "Enter the store and business conditions below to predict "
    "Sales and Customer numbers."
)

st.info(
    "The application uses trained Random Forest models for "
    "Sales and Customer prediction."
)


# =========================================================
# STORE & BUSINESS INFORMATION
# =========================================================

st.header("🏪 Store & Business Information")

col1, col2, col3 = st.columns(3)


with col1:

    store = st.number_input(
        "Store ID",
        min_value=1,
        max_value=1115,
        value=1,
        step=1
    )

    prediction_date = st.date_input(
        "Prediction Date",
         min_value=pd.Timestamp("2013-01-01").date(),
    max_value=pd.Timestamp("2015-09-30").date(),
    value=pd.Timestamp("2015-07-31").date()
    )

    open_status = st.selectbox(
        "Store Status",
        options=[1, 0],
        format_func=lambda x: "Open" if x == 1 else "Closed"
    )

    promo = st.selectbox(
        "Promotion",
        options=[0, 1],
        format_func=lambda x: "No Promotion" if x == 0 else "Promotion"
    )


with col2:

    state_holiday = st.selectbox(
        "State Holiday",
        options=["0", "a", "b", "c"],
        format_func=lambda x: {
            "0": "No State Holiday",
            "a": "Public Holiday",
            "b": "Easter Holiday",
            "c": "Christmas"
        }[x]
    )

    school_holiday = st.selectbox(
        "School Holiday",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )

    store_type = st.selectbox(
        "Store Type",
        options=["a", "b", "c", "d"]
    )

    assortment = st.selectbox(
        "Assortment",
        options=["a", "b", "c"]
    )


with col3:

    competition_distance = st.number_input(
        "Competition Distance",
        min_value=0.0,
        value=500.0,
        step=10.0
    )

    competition_open_month = st.number_input(
        "Competition Open Month",
        min_value=0,
        max_value=12,
        value=0,
        step=1
    )

    competition_open_year = st.number_input(
        "Competition Open Year",
        min_value=0,
        max_value=2030,
        value=0,
        step=1
    )

    promo2 = st.selectbox(
        "Promo2",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )


# =========================================================
# PROMO2 INFORMATION
# =========================================================

st.header("📢 Promo2 Information")

col4, col5, col6 = st.columns(3)


with col4:

    promo2_since_week = st.number_input(
        "Promo2 Since Week",
        min_value=0,
        max_value=52,
        value=0,
        step=1
    )


with col5:

    promo2_since_year = st.number_input(
        "Promo2 Since Year",
        min_value=0,
        max_value=2030,
        value=0,
        step=1
    )


with col6:

    promo_interval = st.selectbox(
        "Promo2 Interval",
        options=[
            "",
            "Jan,Apr,Jul,Oct",
            "Feb,May,Aug,Nov",
            "Mar,Jun,Sept,Dec"
        ]
    )


# =========================================================
# PREDICTION
# =========================================================

if st.button(
    "🔮 Predict Sales & Customers",
    type="primary"
):

    # -----------------------------------------------------
    # CREATE CALENDAR FEATURES
    # -----------------------------------------------------

    date = pd.Timestamp(prediction_date)

    year = date.year
    month = date.month
    day = date.day

    week_of_year = int(
        date.isocalendar().week
    )

    # Rossmann uses 1 = Monday ... 7 = Sunday
    day_of_week = date.dayofweek + 1

    is_weekend = int(
        day_of_week in [6, 7]
    )


    # -----------------------------------------------------
    # CREATE MODEL INPUT
    # -----------------------------------------------------

    input_data = pd.DataFrame({

        "Store": [store],

        "DayOfWeek": [day_of_week],

        "Open": [open_status],

        "Promo": [promo],

        "StateHoliday": [state_holiday],

        "SchoolHoliday": [school_holiday],

        "Year": [year],

        "Month": [month],

        "Day": [day],

        "WeekOfYear": [week_of_year],

        "IsWeekend": [is_weekend],

        "StoreType": [store_type],

        "Assortment": [assortment],

        "CompetitionDistance": [
            competition_distance
        ],

        "CompetitionOpenSinceMonth": [
            competition_open_month
        ],

        "CompetitionOpenSinceYear": [
            competition_open_year
        ],

        "Promo2": [promo2],

        "Promo2SinceWeek": [
            promo2_since_week if promo2 == 1 else None
        ],

        "Promo2SinceYear": [
            promo2_since_year if promo2 == 1 else None
        ],

        "PromoInterval": [
            promo_interval  if promo2 == 1 else None
        ]
    })


    # -----------------------------------------------------
    # GENERATE PREDICTIONS
    # -----------------------------------------------------

    predicted_sales = sales_model.predict(
        input_data
    )[0]

    predicted_customers = customer_model.predict(
        input_data
    )[0]


    # -----------------------------------------------------
    # PREVENT NEGATIVE PREDICTIONS
    # -----------------------------------------------------

    predicted_sales = max(
        0,
        predicted_sales
    )

    predicted_customers = max(
        0,
        predicted_customers
    )


    # -----------------------------------------------------
    # DISPLAY RESULTS
    # -----------------------------------------------------

    st.success(
        "Prediction completed successfully!"
    )

    result_col1, result_col2 = st.columns(2)


    with result_col1:

        st.metric(
            "📊 Predicted Sales",
            f"{predicted_sales:,.0f}"
        )


    with result_col2:

        st.metric(
            "👥 Predicted Customers",
            f"{predicted_customers:,.0f}"
        )


    # -----------------------------------------------------
    # PREDICTION DETAILS
    # -----------------------------------------------------

    st.subheader(
        "📋 Prediction Details"
    )

    result = pd.DataFrame({

        "Parameter": [
            "Store",
            "Prediction Date",
            "Day of Week",
            "Store Status",
            "Promotion",
            "State Holiday",
            "School Holiday",
            "Store Type",
            "Assortment"
        ],

        "Value": [
            store,
            str(prediction_date),
            day_of_week,
            "Open" if open_status == 1 else "Closed",
            "Yes" if promo == 1 else "No",
            state_holiday,
            "Yes" if school_holiday == 1 else "No",
            store_type,
            assortment
        ]
    })


    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

        # -----------------------------------------------------
    # DOWNLOAD PREDICTION
    # -----------------------------------------------------

    prediction_output = pd.DataFrame({
        "Store": [store],
        "Prediction Date": [str(prediction_date)],
        "Predicted Sales": [predicted_sales],
        "Predicted Customers": [predicted_customers]
    })

    csv_data = prediction_output.to_csv(index=False)

    st.download_button(
        label="📥 Download Prediction CSV",
        data=csv_data,
        file_name="rossmann_prediction.csv",
        mime="text/csv"
    )

    