import pandas as pd
import streamlit as st

from src.data_access import load_app_budget as load_budget
from src.manual_entry import add_manual_transaction
from src.ui.display import safe_dataframe


def quick_add_expense_page():
    st.header("Quick Add Expense")

    st.write(
        "Use this page to quickly record everyday spending. "
        "The app automatically uses today's date, marks it as a debit transaction, "
        "and saves it to the manual transactions database."
    )

    try:
        existing_budget = load_budget()
        budget_categories = sorted(
            existing_budget["category"].dropna().unique().tolist()
        )
    except Exception:
        budget_categories = []

    with st.form("quick_add_expense_form"):
        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=0.01,
        )

        description = st.text_input(
            "Description",
            value="Quick Expense",
        )

        if budget_categories:
            category = st.selectbox(
                "Category",
                budget_categories + ["Other"],
            )
        else:
            category = st.text_input(
                "Category",
                value="Other",
            )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Debit Card",
                "Credit Card",
                "Cash",
                "Bank Transfer",
                "Online Payment",
                "Other",
            ],
        )

        location = st.text_input(
            "Location",
            value="Unknown",
        )

        submitted = st.form_submit_button("Save Expense")

        if submitted:
            if amount <= 0:
                st.error("Please enter an amount greater than 0.")
                return

            if description.strip() == "":
                st.error("Please enter a description.")
                return

            if category.strip() == "":
                st.error("Please enter a category.")
                return

            transaction = {
                "date": pd.Timestamp.today().date(),
                "description": description,
                "amount": amount,
                "transaction_type": "debit",
                "category": category,
                "account_name": "Main Account",
                "location": location,
                "payment_method": payment_method,
            }

            updated_transactions = add_manual_transaction(transaction)

            st.success("Expense saved successfully.")

            st.subheader("Latest Manual Transactions")
            safe_dataframe(
                updated_transactions.tail(),
                width="stretch",
            )