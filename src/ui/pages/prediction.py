import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.analytics import monthly_spending
from src.ml_model import train_spending_model, predict_next_month
from src.ui.display import safe_dataframe


def prediction_page():
    st.header("AI Spending Forecast")

    st.write(
        "This page uses machine learning to forecast future monthly spending. "
        "The model learns from previous monthly spending patterns and estimates "
        "how much may be spent next month."
    )

    try:
        transactions = load_transactions()

        if transactions.empty:
            st.warning(
                "No transaction data found. Please upload or enter transactions first."
            )
            return

        monthly_check = monthly_spending(transactions)

        if monthly_check.empty:
            st.warning("No monthly spending data is available yet.")
            return

        training_months = len(monthly_check)

        st.subheader("Machine Learning Status")

        status_col1, status_col2, status_col3 = st.columns(3)

        status_col1.metric("Training Months Available", training_months)
        status_col2.metric("Minimum Months Needed", 6)

        if training_months >= 6:
            status_col3.metric("ML Status", "Ready")
            st.success(
                "The machine learning model has enough historical monthly data to produce a forecast."
            )
        else:
            status_col3.metric("ML Status", "Not Ready")
            st.warning(
                "Not enough historical data for reliable machine learning forecasting. "
                "Please add at least 6 months of transactions."
            )

            st.info(
                "You can still use Budget Tracker, Quick Add Expense, Dashboard, "
                "Spending Analysis, Unusual Transactions, Blockchain Audit, and AI Insights."
            )

            st.subheader("Current Monthly Spending Data")

            display_monthly_check = monthly_check.copy()

            display_monthly_check["month"] = pd.to_datetime(
                display_monthly_check["month"] + "-01",
                errors="coerce",
            ).dt.strftime("%B %Y")

            safe_dataframe(display_monthly_check, width="stretch")

            chart_monthly_check = monthly_check.copy()

            chart_monthly_check["month"] = pd.to_datetime(
                chart_monthly_check["month"] + "-01",
                errors="coerce",
            ).dt.strftime("%B %Y")

            fig = px.line(
                chart_monthly_check,
                x="month",
                y="expense",
                markers=True,
                title="Current Monthly Spending",
            )

            st.plotly_chart(fig, width="stretch")

            st.subheader("Plain-English Recommendation")
            st.info(
                "At the moment, the app can track spending and budgets, but it needs more monthly history "
                "before the ML model can identify a useful spending trend. Keep adding expenses or upload "
                "bank CSV data to improve the forecast."
            )

            return

        model, results, monthly = train_spending_model(transactions)
        prediction = predict_next_month(model, monthly)

        st.subheader("Forecast Result")

        forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

        forecast_col1.metric(
            "Predicted Spending Next Month",
            f"£{prediction:,.2f}",
        )

        latest_actual_spending = monthly["expense"].iloc[-1]

        spending_change = prediction - latest_actual_spending

        forecast_col2.metric(
            "Latest Actual Monthly Spending",
            f"£{latest_actual_spending:,.2f}",
        )

        forecast_col3.metric(
            "Predicted Change",
            f"£{spending_change:,.2f}",
        )

        st.subheader("Model Evaluation")

        eval_col1, eval_col2 = st.columns(2)

        eval_col1.metric(
            "Mean Absolute Error",
            f"£{results['mae']:,.2f}",
        )

        eval_col2.metric(
            "R² Score",
            f"{results['r2_score']:.2f}",
        )

        st.caption(
            "Mean Absolute Error shows the average prediction error in pounds. "
            "R² Score shows how well the model explains the spending pattern. "
            "A higher R² score usually means the model has found a stronger trend."
        )

        if results["r2_score"] < 0.3:
            st.warning(
                "The R² score is low, so the spending pattern may not be strongly predictable. "
                "Treat this forecast as an early estimate, not a guaranteed result."
            )
        elif results["r2_score"] < 0.6:
            st.info(
                "The model has found some spending pattern, but the forecast should still be used carefully."
            )
        else:
            st.success(
                "The model has found a stronger spending pattern in the historical data."
            )

        st.subheader("Actual vs Predicted Monthly Spending")

        fig = px.line(
            monthly,
            x="month",
            y=["expense", "predicted_expense"],
            markers=True,
            title="Actual vs Predicted Monthly Spending",
        )

        st.plotly_chart(fig, width="stretch")

        st.subheader("Monthly Data Used by the Model")

        display_monthly = monthly.copy()

        display_monthly["month"] = pd.to_datetime(
            display_monthly["month"] + "-01",
            errors="coerce",
        ).dt.strftime("%B %Y")

        safe_dataframe(display_monthly, width="stretch")

        st.subheader("Plain-English Recommendation")

        recommendation = generate_prediction_recommendation(
            prediction=prediction,
            latest_actual_spending=latest_actual_spending,
            spending_change=spending_change,
            mae=results["mae"],
            r2_score=results["r2_score"],
        )

        st.info(recommendation)

        st.subheader("How the Machine Learning Works")

        st.write("""
            The app converts individual transactions into monthly spending totals.
            These monthly totals are used to train a Linear Regression model.
            The model learns the spending trend over time and predicts the next month's spending.
            """)

        st.markdown("""
            **Machine learning pipeline used by this page:**

            1. Load transactions from the app databases  
            2. Clean and prepare monthly spending data  
            3. Train a Linear Regression model  
            4. Predict next month's spending  
            5. Evaluate the model using MAE and R² score  
            6. Show the result as a user-friendly forecast  
            """)

    except Exception as error:
        st.warning(
            "Please add or upload transaction data first. "
            "The AI Spending Forecast needs transaction history before it can run."
        )
        st.write(error)


def generate_prediction_recommendation(
    prediction: float,
    latest_actual_spending: float,
    spending_change: float,
    mae: float,
    r2_score: float,
) -> str:
    """
    Generate a simple user-friendly recommendation from the ML forecast.
    """

    if spending_change > 0:
        direction_message = (
            f"The model predicts that next month's spending may increase by "
            f"about £{spending_change:,.2f} compared with the latest month."
        )
    elif spending_change < 0:
        direction_message = (
            f"The model predicts that next month's spending may decrease by "
            f"about £{abs(spending_change):,.2f} compared with the latest month."
        )
    else:
        direction_message = (
            "The model predicts that next month's spending may stay about the same "
            "as the latest month."
        )

    if r2_score < 0.3:
        confidence_message = (
            "However, the model confidence is low because the historical spending pattern "
            "is not strongly predictable. Use this as a guide only."
        )
    elif r2_score < 0.6:
        confidence_message = (
            "The model has moderate confidence. It can help with planning, but the result "
            "should still be checked against your budget."
        )
    else:
        confidence_message = (
            "The model has found a stronger trend in your spending history, so this forecast "
            "may be more useful for planning."
        )

    action_message = (
        f"The average model error is about £{mae:,.2f}. "
        "To use this forecast practically, compare the predicted spending with your monthly budget. "
        "If the prediction is higher than expected, consider reducing flexible spending categories "
        "such as shopping, restaurants, entertainment, or travel."
    )

    return f"{direction_message} {confidence_message} {action_message}"
