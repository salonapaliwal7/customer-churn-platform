from pathlib import Path

import joblib
import pandas as pd


ARTIFACT_PATH = (
    Path(__file__).resolve().parent.parent
    / "artifacts"
    / "model.pkl"
)

artifact = joblib.load(ARTIFACT_PATH)

model = artifact["model"]
preprocessor = artifact["preprocessor"]
threshold = artifact["threshold"]

feature_names = artifact["feature_names"]


def predict_churn(customer_data: dict):

    customer_df = pd.DataFrame([customer_data])

    customer_processed = preprocessor.transform(customer_df)

    churn_probability = model.predict_proba(
        customer_processed
    )[0, 1]

    prediction = int(churn_probability >= threshold)

    return {
        "prediction": prediction,
        "churn_probability": float(churn_probability),
        "threshold": threshold
    }

def clean_feature_name(feature_name):
    """
    Convert transformed feature names into readable labels.
    """

    # Remove preprocessing prefixes
    feature_name = feature_name.replace("num__", "")
    feature_name = feature_name.replace("cat__", "")

    # Replace underscores with spaces
    feature_name = feature_name.replace("_", " ")

    return feature_name

def get_risk_drivers(customer_data: dict, top_n=3):

    customer_df = pd.DataFrame([customer_data])

    customer_processed = preprocessor.transform(customer_df)

    # For Logistic Regression, contribution of each feature
    # is feature value × learned coefficient
    contributions = (
        customer_processed[0] * model.coef_[0]
    )

    driver_df = pd.DataFrame({
        "feature": [
            clean_feature_name(name)
            for name in feature_names
        ],
        "contribution": contributions
    })  

    # Strongest factors pushing toward churn
    churn_drivers = (
        driver_df[driver_df["contribution"] > 0]
        .sort_values("contribution", ascending=False)
        .head(top_n)
    )

    # Strongest factors pushing away from churn
    retention_drivers = (
        driver_df[driver_df["contribution"] < 0]
        .sort_values("contribution")
        .head(top_n)
    )

    return {
        "churn_drivers": churn_drivers.to_dict("records"),
        "retention_drivers": retention_drivers.to_dict("records")
    }