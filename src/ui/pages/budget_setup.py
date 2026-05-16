import pandas as pd
import streamlit as st

from src.ui.pages.data_input import (
    manual_budget_entry_section,
    edit_manual_budget_section,
)
from src.user_database import (
    load_user_income,
    add_or_update_user_income,
    delete_user_income,
)
from src.ui.display import safe_dataframe


def budget_setup_page():
    st.header("Budget Setup")

    st.write(
        "Use this page to set your monthly income and create budget categories. "
        "Your income is stored separately from your budget categories."
    )

    option = st.radio(
        "What would you like to do?",
        [
            "Set Monthly Income",
            "Enter Budget Manually",
            "View or Edit Manual Budget",
            "View or Edit Monthly Income",
        ],
    )

    if option == "Set Monthly Income":
        monthly_income_section()

    elif option == "Enter Budget Manually":
        manual_budget_entry_section()

    elif option == "View or Edit Manual Budget":
        edit_manual_budget_section()

    elif option == "View or Edit Monthly Income":
        edit_monthly_income_section()


def monthly_income_section():
    st.subheader("Set Monthly Income")

    st.write(
        "Enter your income for a specific month. "
        "The Budget Tracker will use this to calculate how much income remains after spending."
    )

    with st.form("monthly_income_form"):
        selected_date = st.date_input("Select month")
        income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            step=50.0,
        )

        submitted = st.form_submit_button("Save Monthly Income")

        if submitted:
            month = pd.to_datetime(selected_date).strftime("%Y-%m")

            updated_income = add_or_update_user_income(month, income)

            st.success(f"Monthly income for {month} saved successfully.")
            safe_dataframe(updated_income, width="stretch")


def edit_monthly_income_section():
    st.subheader("View or Edit Monthly Income")

    income_df = load_user_income()

    if income_df.empty:
        st.info("No monthly income has been saved yet.")
        return

    st.write("Saved Monthly Income")
    safe_dataframe(income_df, width="stretch")

    selected_month = st.selectbox(
        "Select month to edit or delete",
        income_df["month"].tolist(),
    )

    selected_row = income_df[income_df["month"] == selected_month].iloc[0]

    with st.form("edit_monthly_income_form"):
        month = st.text_input(
            "Month",
            value=str(selected_row.get("month", "")),
        )

        income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            step=50.0,
            value=float(selected_row.get("income", 0)),
        )

        update_button = st.form_submit_button("Update Monthly Income")

        if update_button:
            add_or_update_user_income(month, income)

            st.success("Monthly income updated successfully.")
            st.rerun()

    if st.button("Delete Selected Monthly Income"):
        delete_user_income(selected_month)

        st.success("Monthly income deleted successfully.")
        st.rerun()