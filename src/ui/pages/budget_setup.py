import streamlit as st

from src.ui.pages.data_input import (
    manual_budget_entry_section,
    edit_manual_budget_section,
)


def budget_setup_page():
    st.header("Budget Setup")

    st.write(
        "Use this page to create, update, or delete your budget categories. "
        "Budgets are used by the Budget Tracker to calculate remaining money, "
        "daily allowance, weekly allowance, and projected overspending."
    )

    option = st.radio(
        "What would you like to do?",
        [
            "Enter Budget Manually",
            "View or Edit Manual Budget",
        ],
    )

    if option == "Enter Budget Manually":
        manual_budget_entry_section()

    elif option == "View or Edit Manual Budget":
        edit_manual_budget_section()