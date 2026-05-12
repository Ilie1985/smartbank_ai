import plotly.express as px
import streamlit as st

from src.data_access import (
    load_app_transactions as load_transactions,
    load_app_budget as load_budget,
)
from src.budget_forecast import calculate_budget_forecast
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
            "Track your spending against your budget, see your remaining balance, "
            "and forecast whether you are likely to stay within budget this month."
        )

        available_months = sorted(
            transactions["month"].dropna().unique().tolist()
        )

        if not available_months:
            st.warning("No monthly transaction data available.")
            return

        selected_month = st.selectbox(
            "Select month",
            available_months,
            index=len(available_months) - 1,
        )

        comparison, summary = calculate_budget_forecast(
            transactions,
            budget,
            selected_month=selected_month,
        )

        st.subheader("Budget Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Budget", f"£{summary['total_budget']:,.2f}")
        col2.metric("Spent So Far", f"£{summary['total_spent']:,.2f}")
        col3.metric("Remaining Budget", f"£{summary['total_remaining']:,.2f}")
        col4.metric("Budget Health Score", f"{summary['health_score']}/100")

        col5, col6, col7, col8 = st.columns(4)

        col5.metric("Daily Allowance", f"£{summary['daily_allowance']:,.2f}")
        col6.metric("Weekly Allowance", f"£{summary['weekly_allowance']:,.2f}")
        col7.metric("Projected Month-End Spend", f"£{summary['total_projected']:,.2f}")
        col8.metric("Days Left", summary["days_left"])

        if summary["projected_remaining"] < 0:
            st.error(
                f"At your current spending pace, you may exceed your budget by "
                f"£{abs(summary['projected_remaining']):,.2f} this month."
            )
        else:
            st.success(
                f"At your current spending pace, you may have "
                f"£{summary['projected_remaining']:,.2f} left by the end of the month."
            )

        if summary["health_score"] >= 80:
            st.success("Your budget health is good. You are mostly on track.")
        elif summary["health_score"] >= 50:
            st.warning("Your budget health is moderate. Some categories need attention.")
        else:
            st.error("Your budget health is low. You may need to reduce spending.")

        st.subheader("Budget Forecast by Category")

        display_comparison = comparison.copy()

        money_columns = [
            "budget",
            "actual_spending",
            "remaining_budget",
            "projected_month_end_spending",
            "projected_remaining",
            "daily_remaining_allowance",
            "weekly_remaining_allowance",
        ]

        for column in money_columns:
            if column in display_comparison.columns:
                display_comparison[column] = display_comparison[column].round(2)

        display_comparison["percentage_used"] = (
            display_comparison["percentage_used"].round(2)
        )

        safe_dataframe(
            display_comparison[
                [
                    "category",
                    "budget",
                    "actual_spending",
                    "remaining_budget",
                    "percentage_used",
                    "projected_month_end_spending",
                    "projected_remaining",
                    "daily_remaining_allowance",
                    "weekly_remaining_allowance",
                    "budget_status",
                    "pace_status",
                ]
            ],
            width="stretch",
        )

        st.subheader("Budget vs Actual Spending")

        fig = px.bar(
            comparison,
            x="category",
            y=["budget", "actual_spending"],
            barmode="group",
            title="Budget vs Actual Spending",
        )

        st.plotly_chart(fig, width="stretch")

        st.subheader("Projected Month-End Spending")

        fig2 = px.bar(
            comparison,
            x="category",
            y=["budget", "projected_month_end_spending"],
            barmode="group",
            title="Budget vs Projected Month-End Spending",
        )

        st.plotly_chart(fig2, width="stretch")

    except Exception as error:
        st.warning(
            "Please add both transaction data and budget data first. "
            "You can upload files or enter data manually."
        )
        st.write(error)