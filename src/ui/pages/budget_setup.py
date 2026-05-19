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


def format_month_label(month_value):
    """
    Convert YYYY-MM into a user-friendly month label.
    Example: 2026-05 becomes May 2026.
    """

    return pd.to_datetime(str(month_value) + "-01", errors="coerce").strftime("%B %Y")


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
        "The Budget Tracker will use this as your monthly budget pot."
    )

    current_year = pd.Timestamp.today().year

    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    col1, col2 = st.columns(2)

    with col1:
        selected_month_name = st.selectbox(
            "Select month",
            month_names,
            index=pd.Timestamp.today().month - 1,
        )

    with col2:
        year_options = list(range(2020, 2036))

        selected_year = st.selectbox(
            "Select year",
            year_options,
            index=year_options.index(current_year),
        )

    selected_month_number = month_names.index(selected_month_name) + 1
    month = f"{int(selected_year)}-{selected_month_number:02d}"

    st.info(
        f"You are setting income for **{selected_month_name} {int(selected_year)}**."
    )

    with st.form("monthly_income_form"):
        income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            step=50.0,
        )

        submitted = st.form_submit_button("Save Monthly Income")

        if submitted:
            updated_income = add_or_update_user_income(month, income)

            st.success(
                f"Monthly income for {selected_month_name} {int(selected_year)} saved successfully."
            )

            display_income = updated_income.copy()
            display_income["month"] = display_income["month"].apply(format_month_label)

            safe_dataframe(display_income, width="stretch")


def edit_monthly_income_section():
    st.subheader("View or Edit Monthly Income")

    income_df = load_user_income()

    if income_df.empty:
        st.info("No monthly income has been saved yet.")
        return

    st.write("Saved Monthly Income")

    display_income = income_df.copy()
    display_income["month"] = display_income["month"].apply(format_month_label)

    safe_dataframe(display_income, width="stretch")

    month_options = income_df["month"].tolist()

    month_labels = {month: format_month_label(month) for month in month_options}

    selected_month_label = st.selectbox(
        "Select month to edit or delete",
        list(month_labels.values()),
    )

    selected_month = [
        month for month, label in month_labels.items() if label == selected_month_label
    ][0]

    selected_row = income_df[income_df["month"] == selected_month].iloc[0]

    with st.form("edit_monthly_income_form"):
        st.text_input(
            "Month",
            value=format_month_label(selected_row.get("month", "")),
            disabled=True,
        )

        month = selected_month

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
