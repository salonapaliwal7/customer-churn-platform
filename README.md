# Customer Churn Prediction Platform

An end-to-end machine learning application that predicts customer churn risk for telecom customers and provides interpretable prediction drivers through an interactive web dashboard.

🔗 **Live Demo:** https://customer-churn-platform-pfleh3svqhzauxuujx9w6l.streamlit.app/

---

## Project Overview

Customer churn is a critical business problem for subscription-based companies. Identifying customers who are likely to leave allows businesses to proactively take retention actions.

This project builds an end-to-end machine learning pipeline that:

- Analyzes customer demographics, services, contracts, and billing information.
- Predicts the probability that a customer will churn.
- Optimizes the classification threshold based on the business objective.
- Provides global and customer-level model explainability.
- Serves predictions through an interactive Streamlit dashboard.
- Deploys the complete application for real-time inference.

---

## Architecture

```text
Raw Customer Data
        ↓
Exploratory Data Analysis
        ↓
Data Preprocessing
  ├── Missing value handling
  ├── Feature scaling
  └── One-hot encoding
        ↓
Model Training & Comparison
  ├── Logistic Regression
  ├── Decision Tree
  ├── Random Forest
  └── XGBoost
        ↓
Threshold Optimization
        ↓
Final Logistic Regression Model
        ↓
SHAP Explainability
        ↓
Serialized Model Artifact (.pkl)
        ↓
Reusable Prediction Layer
        ↓
Streamlit Dashboard
        ↓
Public Cloud Deployment