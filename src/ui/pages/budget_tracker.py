import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_access import (
    load_app_transactions as load_transactions,
    load_app_budget as load_budget,
)
from src.user_database import load_user_budget, load_user_income
from src.budget_forecast import calculate_budget_forecast
from src.ui.display import safe_dataframe


def get_active_budget():
    """
    Decide which budget should be used on the Budget Tracker page.

    Priority:
    1. Manual budget created by the user
    2. Uploaded/demo budget if no manual budget exists
    """

    manual_budget = load_user_budget()

    if manual_budget is not None and not manual_budget.empty:
        return manual_budget, "Manual Budget"

    uploaded_budget = load_budget()

    return uploaded_budget, "Uploaded/Demo Budget"


def get_monthly_income(selected_month: str) -> float:
    """
    Get saved monthly income for the selected month.
    """

    income_df = load_user_income()

    if income_df.empty:
        return 0.0

    income_df["month"] = income_df["month"].astype(str)

    matching_income = income_df[income_df["month"] == selected_month]

    if matching_income.empty:
        return 0.0

    return float(matching_income.iloc[0]["income"])


def budget_tracker_page():
    st.header("Budget Tracker")

    try:
        transactions = load_transactions()
        budget, budget_source = get_active_budget()

        if transactions.empty:
            st.warning("No transaction data found.")
            return

        if budget.empty:
            st.warning(
                "No budget found. Please go to Budget Setup and create your budget first."
            )
            return

        st.write(
            "This page tracks your spending against your active budget. "
            "Expenses are deducted from budget categories when the transaction category matches the budget category."
        )

        st.info(
            f"Currently using: **{budget_source}**. "
            "Only categories inside this budget are shown below."
        )

        budget_categories = sorted(
            budget["category"].dropna().astype(str).str.strip().str.title().unique()
        )

        transactions = transactions.copy()
        transactions["category"] = (
            transactions["category"].astype(str).str.strip().str.title()
        )

        filtered_transactions = transactions[
            transactions["category"].isin(budget_categories)
        ]

        available_months = sorted(transactions["month"].dropna().unique().tolist())

        if not available_months:
            st.warning("No monthly transaction data available.")
            return

        month_labels = {
            month: pd.to_datetime(month + "-01").strftime("%B %Y")
            for month in available_months
        }

        selected_month_label = st.selectbox(
            "Select month",
            list(month_labels.values()),
            index=len(available_months) - 1,
        )

        selected_month = [
            month
            for month, label in month_labels.items()
            if label == selected_month_label
        ][0]

        comparison, summary = calculate_budget_forecast(
            filtered_transactions,
            budget,
            selected_month=selected_month,
        )

        monthly_income = get_monthly_income(selected_month)

        monthly_budget = monthly_income
        allocated_to_categories = summary["total_budget"]
        available_to_allocate = monthly_budget - allocated_to_categories
        remaining_monthly_budget = monthly_budget - summary["total_spent"]
        projected_month_end_balance = monthly_budget - summary["total_projected"]

        days_left = max(summary["days_left"], 1)

        if monthly_budget > 0:
            allowance_base = max(remaining_monthly_budget, 0)
        else:
            allowance_base = max(summary["total_remaining"], 0)

        daily_allowance = allowance_base / days_left
        weekly_allowance = min(daily_allowance * 7, allowance_base)

        days_left = max(summary["days_left"], 1)

        if monthly_budget > 0:
            allowance_base = max(remaining_monthly_budget, 0)
        else:
            allowance_base = max(summary["total_remaining"], 0)

        daily_allowance = allowance_base / days_left

        st.subheader("Monthly Money Overview")

        monthly_budget = monthly_income
        allocated_to_categories = allocated_to_categories
        available_to_allocate = monthly_budget - allocated_to_categories
        remaining_monthly_budget = monthly_budget - summary["total_spent"]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Monthly Budget", f"£{monthly_budget:,.2f}")
        col2.metric(
            "Allocated to Categories", f"        £{allocated_to_categories:,.2f}"
        )
        col3.metric("Budget Plan Difference", f"£{available_to_allocate:,.2f}")
        col4.metric("Budget Health Score", f"{summary['health_score']}/        100")

        col5, col6, col7, col8 = st.columns(4)

        col5.metric("Spent So Far", f"£{summary['total_spent']:,.2f}")
        col6.metric(
            "Remaining Monthly Budget", f"        £{remaining_monthly_budget:,.2f}"
        )
        col7.metric(
            "Projected Month-End Balance",
            f"        £{projected_month_end_balance:,.2f}",
        )
        col8.metric("Days Left", summary["days_left"])

        col9, col10 = st.columns(2)

        col9.metric("Safe Daily Spend", f"£{daily_allowance:,.2f}")
        col10.metric(
            "Projected Month-End Balance",
            f"£{projected_month_end_balance:,.2f}",
        )

        st.caption(
            "Safe Daily Spend is calculated from your remaining monthly budget divided by the number of days left in the month."
        )

        if monthly_income <= 0:
            st.warning(
                "No monthly income has been set for this month. "
                "Go to Budget Setup → Set Monthly Income to improve this summary."
            )
        else:
            if available_to_allocate < 0:
                st.warning(
                    f"Your monthly budget is £{monthly_budget:,.2f}, but              your category budgets "
                    f"add up to £{allocated_to_categories:,.2f}. "
                    f"This means your plan is £{abs(available_to_allocate)             :,.2f} above your available budget."
                )
            else:
                st.success(
                    f"You have £{available_to_allocate:,.2f} left to              assign to budget categories."
                )

            if projected_month_end_balance < 0:
                st.error(
                    f"At your current spending pace, you may end the month "
                    f"£{abs(projected_month_end_balance):,.2f} below your income."
                )
            else:
                st.success(
                    f"At your current spending pace, you may have "
                    f"£{projected_month_end_balance:,.2f} left from your income by month end."
                )

        if summary["health_score"] >= 80:
            st.success("Your budget health is good. You are mostly on track.")
        elif summary["health_score"] >= 50:
            st.warning(
                "Your budget health is moderate. Some categories need attention."
            )
        else:
            st.error("Your budget health is low. You may need to reduce spending.")

        st.subheader("Budget Categories")

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

        st.subheader("Matching Transactions")

        month_transactions = filtered_transactions[
            filtered_transactions["month"] == selected_month
        ]

        if month_transactions.empty:
            st.info(
                "No transactions found for the selected month that match your budget categories."
            )
        else:
            display_transaction_columns = [
                "date",
                "description",
                "amount",
                "transaction_type",
                "category",
                "account_name",
                "location",
                "payment_method",
                "data_source",
            ]

            available_columns = [
                column
                for column in display_transaction_columns
                if column in month_transactions.columns
            ]

            safe_dataframe(
                month_transactions[available_columns],
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

        st.subheader("Budget vs Projected Month-End Spending")

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
            "You can create a budget in Budget Setup and add expenses using Quick Add Expense."
        )
        st.write(error)
