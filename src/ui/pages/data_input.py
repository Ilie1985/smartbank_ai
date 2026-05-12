import os

import pandas as pd
import streamlit as st


from src.demo_data import load_demo_data

from src.user_database import (
    load_user_transactions,
    load_user_budget,
    update_user_transaction,
    delete_user_transaction,
    add_or_update_user_budget,
    delete_user_budget,
)
from src.validate import (
    validate_transaction_columns,
    validate_budget_columns,
    check_empty_data,
)
from src.clean import clean_transactions, clean_budget
from src.database import save_to_database
from src.data_access import (
    load_app_budget as load_budget,
)
from src.blockchain_audit import add_transaction_hashes
from src.column_mapper import map_uploaded_columns
from src.manual_entry import add_manual_transaction, add_manual_budget

from src.utils.file_helpers import save_raw_file
from src.ui.display import safe_dataframe


def data_input_page():
    st.header("Data Input")

    st.write(
        "Choose how you want to provide your financial data. "
        "You can upload datasets, map different CSV columns, enter transactions manually, "
        "or edit your saved manual inputs."
    )

    input_method = st.radio(
        "Choose input method",
        [
            "Upload Original Transactions and Budget Files",
            "Upload Different Transaction CSV With Column Mapping",
            "Quick Add Expense",
            "Enter Transaction Manually",
            "Enter Budget Manually",
            "View or Edit Manual Transactions",
            "View or Edit Manual Budget",
            "Load Demo Data",
        ],
    )

    if input_method == "Upload Original Transactions and Budget Files":
        upload_data_page()

    elif input_method == "Upload Different Transaction CSV With Column Mapping":
        flexible_csv_upload_section()

    elif input_method == "Quick Add Expense":
        quick_add_expense_section()

    elif input_method == "Enter Transaction Manually":
        manual_transaction_entry_section()

    elif input_method == "Enter Budget Manually":
        manual_budget_entry_section()

    elif input_method == "View or Edit Manual Transactions":
        edit_manual_transactions_section()

    elif input_method == "View or Edit Manual Budget":
        edit_manual_budget_section()

    elif input_method == "Load Demo Data":
        load_demo_data_section()


def upload_data_page():
    st.subheader("Upload Original Transactions and Budget Files")

    st.write(
        "Use this option when your files have the expected columns: "
        "`personal_transactions.csv` and `Budget.csv`."
    )

    transaction_file = st.file_uploader(
        "Upload personal_transactions.csv",
        type=["csv"],
        key="transactions",
    )

    budget_file = st.file_uploader(
        "Upload Budget.csv",
        type=["csv"],
        key="budget",
    )

    if transaction_file is not None and budget_file is not None:
        transaction_path = save_raw_file(transaction_file, "transactions")
        budget_path = save_raw_file(budget_file, "budget")

        transactions_df = pd.read_csv(transaction_file)
        budget_df = pd.read_csv(budget_file)

        st.subheader("Raw Transactions Preview")
        safe_dataframe(transactions_df.head())

        st.subheader("Raw Budget Preview")
        safe_dataframe(budget_df.head())

        if not check_empty_data(transactions_df):
            st.error("The transactions file is empty.")
            return

        if not check_empty_data(budget_df):
            st.error("The budget file is empty.")
            return

        transactions_valid, transaction_missing = validate_transaction_columns(
            transactions_df
        )
        budget_valid, budget_missing = validate_budget_columns(budget_df)

        if not transactions_valid:
            st.error("The transactions file is missing required columns.")
            st.write(transaction_missing)
            return

        if not budget_valid:
            st.error("The budget file is missing required columns.")
            st.write(budget_missing)
            return

        cleaned_transactions = clean_transactions(transactions_df)
        cleaned_transactions = add_transaction_hashes(cleaned_transactions)

        cleaned_budget = clean_budget(budget_df)

        os.makedirs("data/cleaned", exist_ok=True)

        cleaned_transactions.to_csv(
            "data/cleaned/cleaned_transactions.csv",
            index=False,
        )

        cleaned_budget.to_csv(
            "data/cleaned/cleaned_budget.csv",
            index=False,
        )

        save_to_database(cleaned_transactions, "transactions")
        save_to_database(cleaned_budget, "budget")

        st.success(
            "Both datasets were uploaded, cleaned, hashed, and stored successfully."
        )

        st.write(f"Transactions raw file saved to: {transaction_path}")
        st.write(f"Budget raw file saved to: {budget_path}")

        st.subheader("Cleaned Transactions Preview")
        safe_dataframe(cleaned_transactions.head())

        st.subheader("Cleaned Budget Preview")
        safe_dataframe(cleaned_budget.head())


def flexible_csv_upload_section():
    st.subheader("Upload Different Transaction CSV With Column Mapping")

    st.write(
        "Use this option if your CSV has different column names. "
        "You will map your columns to the fields SmartBank AI needs."
    )

    st.info(
        "Tip: Many banks allow you to download transactions as a CSV file. "
        "Log in to online banking, go to statements or transactions, export as CSV, "
        "then upload the file here and map the columns."
    )

    uploaded_file = st.file_uploader(
        "Upload any transaction CSV file",
        type=["csv"],
        key="flexible_transaction_upload",
    )

    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)

        st.write("Uploaded Data Preview")
        safe_dataframe(raw_df.head())

        available_columns = ["Not Available"] + list(raw_df.columns)

        st.write("Map your CSV columns to the app's required fields.")

        date_col = st.selectbox(
            "Which column contains the transaction date?",
            available_columns,
        )

        description_col = st.selectbox(
            "Which column contains the description?",
            available_columns,
        )

        amount_col = st.selectbox(
            "Which column contains the amount?",
            available_columns,
        )

        type_col = st.selectbox(
            "Which column contains the transaction type?",
            available_columns,
        )

        category_col = st.selectbox(
            "Which column contains the category?",
            available_columns,
        )

        st.write("Optional fields")

        account_col = st.selectbox(
            "Which column contains the account name?",
            available_columns,
        )

        location_col = st.selectbox(
            "Which column contains the location?",
            available_columns,
        )

        payment_method_col = st.selectbox(
            "Which column contains the payment method?",
            available_columns,
        )

        if st.button("Process Uploaded Dataset"):
            required_selections = [
                date_col,
                description_col,
                amount_col,
                type_col,
                category_col,
            ]

            if "Not Available" in required_selections:
                st.error("Please map all required fields before processing.")
                return

            column_mapping = {
                "date": date_col,
                "description": description_col,
                "amount": amount_col,
                "transaction_type": type_col,
                "category": category_col,
                "account_name": account_col,
                "location": location_col,
                "payment_method": payment_method_col,
            }

            mapped_df = map_uploaded_columns(raw_df, column_mapping)

            cleaned_df = clean_transactions(mapped_df)
            cleaned_df = add_transaction_hashes(cleaned_df)

            os.makedirs("data/cleaned", exist_ok=True)

            cleaned_df.to_csv(
                "data/cleaned/cleaned_transactions.csv",
                index=False,
            )

            save_to_database(cleaned_df, "transactions")

            st.success(
                "Uploaded dataset has been mapped, cleaned, hashed, and saved successfully."
            )

            st.write("Cleaned Data Preview")
            safe_dataframe(cleaned_df.head())

            st.info(
                "This option updates the transactions table only. "
                "To use the Budget Tracker, add budget data through the manual budget entry option "
                "or upload the original Budget.csv file."
            )


def manual_transaction_entry_section():
    st.subheader("Enter Transaction Manually")

    st.info(
        "Tip: Choose a category that matches your budget category. "
        "For example, if your budget category is 'Food And Treats', "
        "use the same category for related transactions."
    )

    st.write(
        "Use this form if you do not have a CSV file. "
        "Each transaction you add will be cleaned, hashed, stored, and used by the dashboard."
    )

    with st.form("manual_transaction_form"):
        date = st.date_input("Transaction Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)

        transaction_type = st.selectbox(
            "Transaction Type",
            ["debit", "credit"],
        )

        try:
            existing_budget = load_budget()
            budget_categories = sorted(
                existing_budget["category"].dropna().unique().tolist()
            )
        except Exception:
            budget_categories = []

        if budget_categories:
            category = st.selectbox("Category", budget_categories + ["Other"])
        else:
            category = st.text_input("Category", value="Other")

        account_name = st.text_input(
            "Account Name",
            value="Main Account",
        )

        location = st.text_input(
            "Location",
            value="Unknown",
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Debit Card",
                "Credit Card",
                "Bank Transfer",
                "Cash",
                "Direct Debit",
                "Online Payment",
                "Other",
            ],
        )

        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            if description.strip() == "":
                st.error("Please enter a transaction description.")
                return

            if category.strip() == "":
                st.error("Please enter a category.")
                return

            transaction = {
                "date": date,
                "description": description,
                "amount": amount,
                "transaction_type": transaction_type,
                "category": category,
                "account_name": account_name,
                "location": location,
                "payment_method": payment_method,
            }

            updated_transactions = add_manual_transaction(transaction)

            st.success("Transaction added successfully.")
            st.subheader("Latest Transactions")
            safe_dataframe(updated_transactions.tail())


def edit_manual_transactions_section():
    st.subheader("View or Edit Manual Transactions")

    manual_transactions = load_user_transactions()

    if manual_transactions.empty:
        st.info("No manual transactions have been saved yet.")
        return

    st.write("Saved Manual Transactions")
    safe_dataframe(manual_transactions)

    if "manual_id" not in manual_transactions.columns:
        st.warning(
            "Manual transaction IDs were not found. Add a new manual transaction first."
        )
        return

    selected_id = st.selectbox(
        "Select a transaction to edit or delete",
        manual_transactions["manual_id"].tolist(),
    )

    selected_row = manual_transactions[
        manual_transactions["manual_id"] == selected_id
    ].iloc[0]

    with st.form("edit_manual_transaction_form"):
        date = st.text_input("Date", value=str(selected_row.get("date", "")))

        description = st.text_input(
            "Description", value=str(selected_row.get("description", ""))
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=0.01,
            value=float(selected_row.get("amount", 0)),
        )

        transaction_type = st.selectbox(
            "Transaction Type",
            ["debit", "credit"],
            index=(
                0
                if str(selected_row.get("transaction_type", "debit")) == "debit"
                else 1
            ),
        )

        category = st.text_input(
            "Category", value=str(selected_row.get("category", "Other"))
        )

        account_name = st.text_input(
            "Account Name", value=str(selected_row.get("account_name", "Main Account"))
        )

        location = st.text_input(
            "Location", value=str(selected_row.get("location", "Unknown"))
        )

        payment_method = st.text_input(
            "Payment Method", value=str(selected_row.get("payment_method", "Other"))
        )

        update_button = st.form_submit_button("Update Transaction")

        if update_button:
            updated_values = {
                "date": date,
                "description": description,
                "amount": amount,
                "transaction_type": transaction_type,
                "category": category,
                "account_name": account_name,
                "location": location,
                "payment_method": payment_method,
            }

            update_user_transaction(selected_id, updated_values)

            st.success("Manual transaction updated successfully.")
            st.rerun()

    if st.button("Delete Selected Transaction"):
        delete_user_transaction(selected_id)

        st.success("Manual transaction deleted successfully.")
        st.rerun()


def manual_budget_entry_section():
    st.subheader("Enter Budget Manually")

    st.write(
        "Use this form to create or update budget categories. "
        "These budget values will be used in the Budget Tracker page."
    )

    with st.form("manual_budget_form"):
        category = st.text_input("Budget Category")
        budget = st.number_input("Budget Amount", min_value=0.0, step=1.0)

        submitted = st.form_submit_button("Add Budget Category")

        if submitted:
            if category.strip() == "":
                st.error("Please enter a budget category.")
                return

            updated_budget = add_manual_budget(category, budget)

            st.success("Budget category added successfully.")
            safe_dataframe(updated_budget)


def edit_manual_budget_section():
    st.subheader("View or Edit Manual Budget")

    manual_budget = load_user_budget()

    if manual_budget.empty:
        st.info("No manual budget categories have been saved yet.")
        return

    st.write("Saved Manual Budget")
    safe_dataframe(manual_budget)

    selected_category = st.selectbox(
        "Select a budget category to edit or delete",
        manual_budget["category"].tolist(),
    )

    selected_row = manual_budget[manual_budget["category"] == selected_category].iloc[0]

    with st.form("edit_manual_budget_form"):
        category = st.text_input(
            "Category", value=str(selected_row.get("category", ""))
        )

        budget = st.number_input(
            "Budget",
            min_value=0.0,
            step=1.0,
            value=float(selected_row.get("budget", 0)),
        )

        update_button = st.form_submit_button("Update Budget Category")

        if update_button:
            add_or_update_user_budget(category, budget)

            st.success("Manual budget category updated successfully.")
            st.rerun()

    if st.button("Delete Selected Budget Category"):
        delete_user_budget(selected_category)

        st.success("Manual budget category deleted successfully.")
        st.rerun()


def quick_add_expense_section():
    st.subheader("Quick Add Expense")

    st.write(
        "Use this form for fast daily spending tracking. "
        "Only the key details are required."
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

        submitted = st.form_submit_button("Save Expense")

        if submitted:
            if amount <= 0:
                st.error("Please enter an amount greater than 0.")
                return

            transaction = {
                "date": pd.Timestamp.today().date(),
                "description": description,
                "amount": amount,
                "transaction_type": "debit",
                "category": category,
                "account_name": "Main Account",
                "location": "Unknown",
                "payment_method": payment_method,
            }

            updated_transactions = add_manual_transaction(transaction)

            st.success("Expense saved successfully.")
            st.subheader("Latest Manual Transactions")
            safe_dataframe(updated_transactions.tail(), width="stretch")


def load_demo_data_section():
    st.subheader("Load Demo Data")

    st.write(
        "Use demo data to test the full application immediately, including "
        "dashboard, budget tracker, prediction, unusual transactions, and blockchain audit."
    )

    st.warning(
        "Demo data is for testing only. It will replace the current uploaded CSV data, "
        "but it will not delete manually entered transactions or budgets."
    )

    if st.button("Load 12 Months of Demo Data"):
        transactions, budget = load_demo_data()

        st.success("Demo data loaded successfully.")

        st.subheader("Demo Transactions Preview")
        safe_dataframe(transactions.head(), width="stretch")

        st.subheader("Demo Budget Preview")
        safe_dataframe(budget.head(), width="stretch")
