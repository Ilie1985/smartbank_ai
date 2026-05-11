import plotly.express as px
import streamlit as st

from src.data_access import (
    load_app_transactions as load_transactions,
    load_app_budget as load_budget,
)
from src.budget_analysis import compare_budget_to_actual
from src.ui.display import safe_dataframe


def budget_tracker_page():
    st.header("Budget Tracker")

    try:
        transactions = load_transactions()
        budget = load_budget()

        if transactions.empty:
            st.warning("No transaction data found.")
            return

        if budget.empty:
            st.warning(
                "No budget data found. Please enter or upload budget categories first."
            )
            return

        st.write(
            "This page compares your actual spending against your budget. "
            "Select a month to see how much you have spent and how much budget remains."
        )

        available_months = ["All"] + sorted(
            transactions["month"].dropna().unique().tolist()
        )

        selected_month = st.selectbox(
            "Select month for budget comparison",
            available_months,
        )

        comparison = compare_budget_to_actual(
            transactions,
            budget,
            selected_month=selected_month,
        )

        total_budget = comparison["budget"].sum()
        total_spent = comparison["actual_spending"].sum()
        total_remaining = total_budget - total_spent

        over_budget_count = len(
            comparison[comparison["budget_status"] == "Over Budget"]
        )
        close_to_limit_count = len(
            comparison[comparison["budget_status"] == "Close to Limit"]
        )
        within_budget_count = len(
            comparison[comparison["budget_status"] == "Within Budget"]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Budget", f"£{total_budget:,.2f}")
        col2.metric("Actual Spending", f"£{total_spent:,.2f}")
        col3.metric("Remaining Budget", f"£{total_remaining:,.2f}")

        col4, col5, col6 = st.columns(3)

        col4.metric("Over Budget", over_budget_count)
        col5.metric("Close to Limit", close_to_limit_count)
        col6.metric("Within Budget", within_budget_count)

        if total_remaining < 0:
            st.error(f"You are over your total budget by £{abs(total_remaining):,.2f}.")
        else:
            st.success(
                f"You still have £{total_remaining:,.2f} remaining in your budget."
            )

        st.subheader("Budget Comparison Table")

        display_comparison = comparison.copy()
        display_comparison["budget"] = display_comparison["budget"].round(2)
        display_comparison["actual_spending"] = display_comparison[
            "actual_spending"
        ].round(2)
        display_comparison["remaining_budget"] = display_comparison[
            "remaining_budget"
        ].round(2)
        display_comparison["percentage_used"] = display_comparison[
            "percentage_used"
        ].round(2)

        safe_dataframe(
            display_comparison[
                [
                    "category",
                    "budget",
                    "actual_spending",
                    "remaining_budget",
                    "percentage_used",
                    "budget_status",
                ]
            ],
            width="stretch",
        )

        st.subheader("Actual Spending vs Budget")

        fig = px.bar(
            comparison,
            x="category",
            y=["budget", "actual_spending"],
            barmode="group",
            title="Budget vs Actual Spending",
        )

        st.plotly_chart(fig, width="stretch")

        st.subheader("Remaining Budget by Category")

        fig2 = px.bar(
            comparison,
            x="category",
            y="remaining_budget",
            title="Remaining Budget by Category",
        )

        st.plotly_chart(fig2, width="stretch")

    except Exception as error:
        st.warning(
            "Please add both transaction data and budget data first. "
            "You can upload files or enter data manually."
        )
        st.write(error)