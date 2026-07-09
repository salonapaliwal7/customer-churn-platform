import sys
from pathlib import Path

import streamlit as st


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


from src.predict import predict_churn, get_risk_drivers


st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


st.title("Customer Churn Prediction Platform")

st.write(
    "Enter customer information to estimate the probability of churn."
)

st.divider()

with st.form("churn_prediction_form"):

    st.subheader("Customer Information")

    col1, col2, col3 = st.columns(3)

    # Demographics
    with col1:
        st.markdown("### Demographics")

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        senior_citizen = st.selectbox(
            "Senior Citizen",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

    # Account information
    with col2:
        st.markdown("### Account Information")

        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=72,
            value=12
        )

        contract = st.selectbox(
            "Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        paperless_billing = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    # Billing
    with col3:
        st.markdown("### Billing")

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=1000.0
        )

    # Services
    st.markdown("### Services")

    service_col1, service_col2, service_col3 = st.columns(3)

    with service_col1:

        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["No", "Yes", "No phone service"]
        )

        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

    with service_col2:

        online_security = st.selectbox(
            "Online Security",
            ["No", "Yes", "No internet service"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["No", "Yes", "No internet service"]
        )

        device_protection = st.selectbox(
            "Device Protection",
            ["No", "Yes", "No internet service"]
        )

    with service_col3:

        tech_support = st.selectbox(
            "Tech Support",
            ["No", "Yes", "No internet service"]
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["No", "Yes", "No internet service"]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["No", "Yes", "No internet service"]
        )

    # Submit button
    submitted = st.form_submit_button(
        "Predict Churn Risk",
        use_container_width=True
    )

if submitted:

    customer_data = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    result = predict_churn(customer_data)

    probability = result["churn_probability"]
    prediction = result["prediction"]


    st.divider()

    st.subheader("Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Churn Probability",
            value=f"{probability:.1%}"
        )

    with col2:
        if prediction == 1:
            st.error("High Churn Risk")
        else:
            st.success("Low Churn Risk")


    # Risk Drivers
    drivers = get_risk_drivers(customer_data)

    st.subheader("Key Prediction Drivers")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Factors Increasing Churn Risk")

        for driver in drivers["churn_drivers"]:
            feature = driver["feature"]
            contribution = driver["contribution"]

            st.write(
                f"• {feature}: +{contribution:.3f}"
            )

    with col2:
        st.markdown("#### Factors Reducing Churn Risk")

        for driver in drivers["retention_drivers"]:
            feature = driver["feature"]
            contribution = driver["contribution"]

            st.write(
                f"• {feature}: {contribution:.3f}"
            )