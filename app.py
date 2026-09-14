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

# =========================================================
# MEMORY-OPTIMIZED MODEL PREDICTION
# =========================================================
# Community Cloud has a finite memory limit. The two trained
# Random Forest models are therefore loaded one at a time
# instead of keeping both large model objects in memory.

def predict_sales(input_data):
    import gc

    model = joblib.load(
        "models/rossmann_random_forest_20260909_084440.joblib"
    )
    prediction = model.predict(input_data)[0]
    del model
    gc.collect()
    return prediction


def predict_customers(input_data):
    import gc

    model = joblib.load(
        "models/rossmann_customer_random_forest_20260909_105310.joblib"
    )
    prediction = model.predict(input_data)[0]
    del model
    gc.collect()
    return prediction

# =========================================================
# APPLICATION HEADER
# =========================================================

st.title("📊 Rossmann Sales Forecasting")

st.write(
    "Use the trained Random Forest models to forecast Sales and "
    "Customer numbers for Rossmann stores."
)

st.info(
    "The application supports both manual single-store prediction "
    "and CSV-based batch prediction."
)

# =========================================================
# PREDICTION MODE
# =========================================================

prediction_mode = st.radio(
    "Choose Prediction Method",
    ["📝 Manual Prediction", "📂 CSV Batch Prediction"],
    horizontal=True
)

# =========================================================
# MANUAL SINGLE-STORE PREDICTION
# =========================================================

if prediction_mode == "📝 Manual Prediction":

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

    st.subheader("📢 Promo2 Information")

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

    if st.button("🔮 Predict Sales & Customers", type="primary"):

        # Calendar features
        date = pd.Timestamp(prediction_date)
        year = date.year
        month = date.month
        day = date.day
        week_of_year = int(date.isocalendar().week)
        day_of_week = date.dayofweek + 1
        is_weekend = int(day_of_week in [6, 7])

        # Model input
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
            "CompetitionDistance": [competition_distance],
            "CompetitionOpenSinceMonth": [competition_open_month],
            "CompetitionOpenSinceYear": [competition_open_year],
            "Promo2": [promo2],
            "Promo2SinceWeek": [
                promo2_since_week if promo2 == 1 else None
            ],
            "Promo2SinceYear": [
                promo2_since_year if promo2 == 1 else None
            ],
            "PromoInterval": [
                promo_interval if promo2 == 1 else None
            ]
        })

        # Predictions
        predicted_sales = max(0, predict_sales(input_data))
        predicted_customers = max(0, predict_customers(input_data))

        st.success("Prediction completed successfully!")

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

        st.subheader("📋 Prediction Details")

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

        prediction_output = pd.DataFrame({
            "Store": [store],
            "Prediction Date": [str(prediction_date)],
            "Predicted Sales": [predicted_sales],
            "Predicted Customers": [predicted_customers]
        })

        st.download_button(
            label="📥 Download Prediction CSV",
            data=prediction_output.to_csv(index=False),
            file_name="rossmann_prediction.csv",
            mime="text/csv"
        )

# =========================================================
# CSV BATCH PREDICTION
# =========================================================

else:

    st.header("📂 CSV Upload & Batch Prediction")

    st.write(
        "Upload a CSV containing the 20 model input features. "
        "The application will generate Sales and Customer predictions "
        "for every row."
    )

    required_columns = [
        "Store",
        "DayOfWeek",
        "Open",
        "Promo",
        "StateHoliday",
        "SchoolHoliday",
        "Year",
        "Month",
        "Day",
        "WeekOfYear",
        "IsWeekend",
        "StoreType",
        "Assortment",
        "CompetitionDistance",
        "CompetitionOpenSinceMonth",
        "CompetitionOpenSinceYear",
        "Promo2",
        "Promo2SinceWeek",
        "Promo2SinceYear",
        "PromoInterval"
    ]

    # Independent template: no manual-form variables are used here.
    template_data = pd.DataFrame([{
        "Store": 1,
        "DayOfWeek": 5,
        "Open": 1,
        "Promo": 1,
        "StateHoliday": "0",
        "SchoolHoliday": 1,
        "Year": 2015,
        "Month": 7,
        "Day": 31,
        "WeekOfYear": 31,
        "IsWeekend": 0,
        "StoreType": "a",
        "Assortment": "a",
        "CompetitionDistance": 500.0,
        "CompetitionOpenSinceMonth": 0,
        "CompetitionOpenSinceYear": 0,
        "Promo2": 0,
        "Promo2SinceWeek": 0,
        "Promo2SinceYear": 0,
        "PromoInterval": ""
    }])

    st.download_button(
        label="📄 Download CSV Template",
        data=template_data.to_csv(index=False),
        file_name="rossmann_prediction_template.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader(
        "Upload prediction CSV",
        type=["csv"],
        help="Use the 20 columns provided in the downloadable template."
    )

    if uploaded_file is not None:

        try:
            batch_input = pd.read_csv(uploaded_file)

            missing_columns = [
                column
                for column in required_columns
                if column not in batch_input.columns
            ]

            if missing_columns:
                st.error(
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                )

            elif batch_input.empty:
                st.warning(
                    "The uploaded CSV is empty. Please upload a CSV containing data."
                )

            else:
                batch_input = batch_input[required_columns].copy()

                # Numeric conversion for fields that may contain blank CSV values.
                numeric_columns = [
                    "Store",
                    "DayOfWeek",
                    "Open",
                    "Promo",
                    "SchoolHoliday",
                    "Year",
                    "Month",
                    "Day",
                    "WeekOfYear",
                    "IsWeekend",
                    "CompetitionDistance",
                    "CompetitionOpenSinceMonth",
                    "CompetitionOpenSinceYear",
                    "Promo2",
                    "Promo2SinceWeek",
                    "Promo2SinceYear"
                ]

                for column in numeric_columns:
                    batch_input[column] = pd.to_numeric(
                        batch_input[column],
                        errors="coerce"
                    )

                # Load each model only for its prediction pass.
                # This avoids keeping both large Random Forest objects
                # in Community Cloud memory at the same time.
                import gc

                sales_model = joblib.load(
                    "models/rossmann_random_forest_20260909_084440.joblib"
                )
                sales_predictions = pd.Series(
                    sales_model.predict(batch_input)
                ).clip(lower=0)
                del sales_model
                gc.collect()

                customer_model = joblib.load(
                    "models/rossmann_customer_random_forest_20260909_105310.joblib"
                )
                customer_predictions = pd.Series(
                    customer_model.predict(batch_input)
                ).clip(lower=0)
                del customer_model
                gc.collect()

                batch_output = batch_input.copy()
                batch_output["Predicted Sales"] = sales_predictions.values
                batch_output["Predicted Customers"] = (
                    customer_predictions.values
                )

                st.success(
                    f"CSV prediction completed successfully for "
                    f"{len(batch_output):,} rows!"
                )

                metric_col1, metric_col2 = st.columns(2)

                with metric_col1:
                    st.metric(
                        "📊 Total Predicted Sales",
                        f"{batch_output['Predicted Sales'].sum():,.0f}"
                    )

                with metric_col2:
                    st.metric(
                        "👥 Total Predicted Customers",
                        f"{batch_output['Predicted Customers'].sum():,.0f}"
                    )

                # Dedicated charts for the two predicted outputs.
                st.subheader("📈 Predicted Sales")
                st.line_chart(
                    batch_output["Predicted Sales"],
                    height=300
                )

                st.subheader("👥 Predicted Customers")
                st.line_chart(
                    batch_output["Predicted Customers"],
                    height=300
                )

                st.subheader("📋 Batch Prediction Results")

                st.dataframe(
                    batch_output,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    label="📥 Download Batch Prediction CSV",
                    data=batch_output.to_csv(index=False),
                    file_name="rossmann_batch_predictions.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(
                f"Unable to process the uploaded CSV: {e}"
            )
