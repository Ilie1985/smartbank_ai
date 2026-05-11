import plotly.express as px
import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.analytics import monthly_spending
from src.ml_model import train_spending_model, predict_next_month
from src.ui.display import safe_dataframe


def prediction_page():
    st.header("Machine Learning Spending Prediction")

    try:
        transactions = load_transactions()

        monthly_check = monthly_spending(transactions)

        if len(monthly_check) < 6:
            st.warning(
                "Not enough historical data for reliable prediction. "
                "Please add at least 6 months of transactions for better forecasting."
            )

            st.write(
                "You can still use the dashboard, budget tracker, spending analysis, "
                "unusual transaction detection, blockchain audit, and AI insights."
            )

            st.subheader("Current Monthly Spending Data")
            safe_dataframe(monthly_check)

            if not monthly_check.empty:
                fig = px.line(
                    monthly_check,
                    x="month",
                    y="expense",
                    markers=True,
                    title="Current Monthly Spending",
                )

                st.plotly_chart(fig, width="stretch")

            return

        model, results, monthly = train_spending_model(transactions)
        prediction = predict_next_month(model, monthly)

        st.metric(
            "Predicted Spending Next Month",
            f"£{prediction:,.2f}",
        )

        st.subheader("Model Evaluation")
        st.write(f"Mean Absolute Error: £{results['mae']:,.2f}")
        st.write(f"R² Score: {results['r2_score']:.2f}")

        if results["r2_score"] < 0.3:
            st.info(
                "The R² score is low, which suggests that the spending pattern is not strongly linear. "
                "The prediction should be treated as a prototype estimate, not a guaranteed forecast."
            )

        st.subheader("Monthly Data Used by the Model")
        safe_dataframe(monthly)

        fig = px.line(
            monthly,
            x="month",
            y=["expense", "predicted_expense"],
            markers=True,
            title="Actual vs Predicted Monthly Spending",
        )

        st.plotly_chart(fig, width="stretch")

    except Exception:
        st.warning("Please add or upload transaction data first.")