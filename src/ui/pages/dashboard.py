import plotly.express as px
import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.analytics import (
    calculate_summary,
    spending_by_category,
    monthly_spending,
    monthly_income,
)


def dashboard_page():
    st.header("Financial Dashboard")

    try:
        transactions = load_transactions()
        summary = calculate_summary(transactions)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Income", f"£{summary['total_income']:,.2f}")
        col2.metric("Total Expenses", f"£{summary['total_expenses']:,.2f}")
        col3.metric("Net Savings", f"£{summary['net_savings']:,.2f}")
        col4.metric("Transactions", summary["transaction_count"])

        st.subheader("Spending by Category")

        category_df = spending_by_category(transactions)

        if category_df.empty:
            st.info("No expense data available for category analysis.")
        else:
            fig = px.pie(
                category_df,
                names="category",
                values="expense",
                title="Spending by Category",
            )

            st.plotly_chart(fig, width="stretch")

        st.subheader("Monthly Spending Trend")

        monthly_df = monthly_spending(transactions)

        if monthly_df.empty:
            st.info("No monthly spending data available.")
        else:
            fig2 = px.line(
                monthly_df,
                x="month",
                y="expense",
                markers=True,
                title="Monthly Spending",
            )

            st.plotly_chart(fig2, width="stretch")

        st.subheader("Monthly Income Trend")

        income_df = monthly_income(transactions)

        if income_df.empty:
            st.info("No monthly income data available.")
        else:
            fig3 = px.line(
                income_df,
                x="month",
                y="income",
                markers=True,
                title="Monthly Income",
            )

            st.plotly_chart(fig3, width="stretch")

    except Exception:
        st.warning("Please add or upload transaction data first.")