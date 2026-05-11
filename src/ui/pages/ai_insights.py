import pandas as pd
import streamlit as st

from src.data_access import (
    load_app_transactions as load_transactions,
    load_app_budget as load_budget,
)
from src.insights import generate_financial_insights


def ai_insights_page():
    st.header("AI-Style Financial Insights")

    try:
        transactions = load_transactions()

        try:
            budget = load_budget()
        except Exception:
            budget = pd.DataFrame(columns=["category", "budget"])

        if budget.empty:
            st.info(
                "No budget data found. Add budget categories to receive budget-related insights."
            )

        insights = generate_financial_insights(transactions, budget)

        for insight in insights:
            st.info(insight)

    except Exception:
        st.warning("Please add or upload transaction data first.")