import streamlit as st

from src.data_access import (
    load_app_transactions as load_transactions,
    load_app_budget as load_budget,
)
from src.ui.display import safe_dataframe


def data_quality_page():
    st.header("Data Quality Report")

    try:
        transactions = load_transactions()

        st.subheader("Transactions Dataset")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", len(transactions))
        col2.metric("Columns", len(transactions.columns))
        col3.metric("Duplicate Rows", transactions.duplicated().sum())

        st.write("Missing Values")
        missing_transactions = transactions.isnull().sum().reset_index()
        missing_transactions.columns = ["Column", "Missing Values"]
        safe_dataframe(missing_transactions)

    except Exception:
        st.warning("Please add or upload transaction data first.")

    try:
        budget = load_budget()

        st.subheader("Budget Dataset")

        col4, col5, col6 = st.columns(3)

        col4.metric("Rows", len(budget))
        col5.metric("Columns", len(budget.columns))
        col6.metric("Duplicate Rows", budget.duplicated().sum())

        st.write("Missing Values")
        missing_budget = budget.isnull().sum().reset_index()
        missing_budget.columns = ["Column", "Missing Values"]
        safe_dataframe(missing_budget)

    except Exception:
        st.info("No budget data found yet. Add a budget manually or upload Budget.csv.")