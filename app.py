# import os
# from datetime import datetime

# import pandas as pd
# import streamlit as st
# import plotly.express as px

# from src.validate import (
#     validate_transaction_columns,
#     validate_budget_columns,
#     check_empty_data
# )
# from src.clean import clean_transactions, clean_budget
# from src.database import save_to_database, load_transactions, load_budget
# from src.analytics import (
#     calculate_summary,
#     spending_by_category,
#     monthly_spending,
#     monthly_income,
#     yearly_summary,
#     spending_by_account,
#     top_descriptions
# )
# from src.budget_analysis import compare_budget_to_actual
# from src.ml_model import train_spending_model, predict_next_month
# from src.fraud_detection import detect_unusual_transactions
# from src.blockchain_audit import add_transaction_hashes, verify_transaction_hash
# from src.insights import generate_financial_insights


# st.set_page_config(
#     page_title="SmartBank AI",
#     page_icon="🏦",
#     layout="wide"
# )


# def save_raw_file(uploaded_file, prefix):
#     """
#     Save uploaded CSV files to data/raw.
#     """

#     os.makedirs("data/raw", exist_ok=True)

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     file_path = f"data/raw/{prefix}_{timestamp}.csv"

#     with open(file_path, "wb") as file:
#         file.write(uploaded_file.getbuffer())

#     return file_path


# def main():
#     st.title("🏦 SmartBank AI")
#     st.write("Personal Finance and Budget Intelligence App")

#     menu = st.sidebar.radio(
#         "Navigation",
#         [
#             "Upload Data",
#             "Data Quality",
#             "Dashboard",
#             "Budget Tracker",
#             "Account Analysis",
#             "Spending Analysis",
#             "Prediction",
#             "Unusual Transactions",
#             "Blockchain Audit",
#             "AI Insights",
#             "About"
#         ]
#     )

#     if menu == "Upload Data":
#         upload_data_page()
#     elif menu == "Data Quality":
#         data_quality_page()
#     elif menu == "Dashboard":
#         dashboard_page()
#     elif menu == "Budget Tracker":
#         budget_tracker_page()
#     elif menu == "Account Analysis":
#         account_analysis_page()
#     elif menu == "Spending Analysis":
#         spending_analysis_page()
#     elif menu == "Prediction":
#         prediction_page()
#     elif menu == "Unusual Transactions":
#         unusual_transactions_page()
#     elif menu == "Blockchain Audit":
#         blockchain_audit_page()
#     elif menu == "AI Insights":
#         ai_insights_page()
#     elif menu == "About":
#         about_page()


# def upload_data_page():
#     st.header("Upload Data")

#     st.write("Upload both datasets: transactions and budget.")

#     transaction_file = st.file_uploader(
#         "Upload personal_transactions.csv",
#         type=["csv"],
#         key="transactions"
#     )

#     budget_file = st.file_uploader(
#         "Upload Budget.csv",
#         type=["csv"],
#         key="budget"
#     )

#     if transaction_file is not None and budget_file is not None:
#         transaction_path = save_raw_file(transaction_file, "transactions")
#         budget_path = save_raw_file(budget_file, "budget")

#         transactions_df = pd.read_csv(transaction_file)
#         budget_df = pd.read_csv(budget_file)

#         st.subheader("Raw Transactions Preview")
#         st.dataframe(transactions_df.head())

#         st.subheader("Raw Budget Preview")
#         st.dataframe(budget_df.head())

#         if not check_empty_data(transactions_df):
#             st.error("The transactions file is empty.")
#             return

#         if not check_empty_data(budget_df):
#             st.error("The budget file is empty.")
#             return

#         transactions_valid, transaction_missing = validate_transaction_columns(transactions_df)
#         budget_valid, budget_missing = validate_budget_columns(budget_df)

#         if not transactions_valid:
#             st.error("The transactions file is missing required columns.")
#             st.write(transaction_missing)
#             return

#         if not budget_valid:
#             st.error("The budget file is missing required columns.")
#             st.write(budget_missing)
#             return

#         cleaned_transactions = clean_transactions(transactions_df)
#         cleaned_transactions = add_transaction_hashes(cleaned_transactions)

#         cleaned_budget = clean_budget(budget_df)

#         os.makedirs("data/cleaned", exist_ok=True)

#         cleaned_transactions.to_csv(
#             "data/cleaned/cleaned_transactions.csv",
#             index=False
#         )

#         cleaned_budget.to_csv(
#             "data/cleaned/cleaned_budget.csv",
#             index=False
#         )

#         save_to_database(cleaned_transactions, "transactions")
#         save_to_database(cleaned_budget, "budget")

#         st.success("Both datasets were uploaded, cleaned, hashed, and stored successfully.")

#         st.write(f"Transactions raw file saved to: {transaction_path}")
#         st.write(f"Budget raw file saved to: {budget_path}")

#         st.subheader("Cleaned Transactions Preview")
#         st.dataframe(cleaned_transactions.head())

#         st.subheader("Cleaned Budget Preview")
#         st.dataframe(cleaned_budget.head())


# def data_quality_page():
#     st.header("Data Quality Report")

#     try:
#         transactions = load_transactions()
#         budget = load_budget()

#         st.subheader("Transactions Dataset")

#         col1, col2, col3 = st.columns(3)

#         col1.metric("Rows", len(transactions))
#         col2.metric("Columns", len(transactions.columns))
#         col3.metric("Duplicate Rows", transactions.duplicated().sum())

#         st.write("Missing Values")
#         missing_transactions = transactions.isnull().sum().reset_index()
#         missing_transactions.columns = ["Column", "Missing Values"]
#         st.dataframe(missing_transactions)

#         st.subheader("Budget Dataset")

#         col4, col5, col6 = st.columns(3)

#         col4.metric("Rows", len(budget))
#         col5.metric("Columns", len(budget.columns))
#         col6.metric("Duplicate Rows", budget.duplicated().sum())

#         st.write("Missing Values")
#         missing_budget = budget.isnull().sum().reset_index()
#         missing_budget.columns = ["Column", "Missing Values"]
#         st.dataframe(missing_budget)

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def dashboard_page():
#     st.header("Financial Dashboard")

#     try:
#         transactions = load_transactions()
#         summary = calculate_summary(transactions)

#         col1, col2, col3, col4 = st.columns(4)

#         col1.metric("Total Income", f"£{summary['total_income']:,.2f}")
#         col2.metric("Total Expenses", f"£{summary['total_expenses']:,.2f}")
#         col3.metric("Net Savings", f"£{summary['net_savings']:,.2f}")
#         col4.metric("Transactions", summary["transaction_count"])

#         st.subheader("Spending by Category")

#         category_df = spending_by_category(transactions)

#         fig = px.pie(
#             category_df,
#             names="category",
#             values="expense",
#             title="Spending by Category"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#         st.subheader("Monthly Spending Trend")

#         monthly_df = monthly_spending(transactions)

#         fig2 = px.line(
#             monthly_df,
#             x="month",
#             y="expense",
#             markers=True,
#             title="Monthly Spending"
#         )

#         st.plotly_chart(fig2, use_container_width=True)

#         st.subheader("Monthly Income Trend")

#         income_df = monthly_income(transactions)

#         fig3 = px.line(
#             income_df,
#             x="month",
#             y="income",
#             markers=True,
#             title="Monthly Income"
#         )

#         st.plotly_chart(fig3, use_container_width=True)

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def budget_tracker_page():
#     st.header("Budget Tracker")

#     try:
#         transactions = load_transactions()
#         budget = load_budget()

#         comparison = compare_budget_to_actual(transactions, budget)

#         over_budget_count = len(comparison[comparison["budget_status"] == "Over Budget"])
#         close_to_limit_count = len(comparison[comparison["budget_status"] == "Close to Limit"])
#         within_budget_count = len(comparison[comparison["budget_status"] == "Within Budget"])

#         col1, col2, col3 = st.columns(3)

#         col1.metric("Over Budget", over_budget_count)
#         col2.metric("Close to Limit", close_to_limit_count)
#         col3.metric("Within Budget", within_budget_count)

#         st.subheader("Budget Comparison Table")

#         st.dataframe(
#             comparison[
#                 [
#                     "category",
#                     "budget",
#                     "actual_spending",
#                     "remaining_budget",
#                     "percentage_used",
#                     "budget_status"
#                 ]
#             ]
#         )

#         st.subheader("Actual Spending vs Budget")

#         fig = px.bar(
#             comparison,
#             x="category",
#             y=["budget", "actual_spending"],
#             barmode="group",
#             title="Budget vs Actual Spending"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def account_analysis_page():
#     st.header("Account Analysis")

#     try:
#         transactions = load_transactions()

#         account_df = spending_by_account(transactions)

#         st.subheader("Spending by Account")

#         fig = px.bar(
#             account_df,
#             x="account_name",
#             y="expense",
#             title="Spending by Account or Card"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#         accounts = ["All"] + sorted(transactions["account_name"].unique().tolist())

#         selected_account = st.selectbox(
#             "Filter by account",
#             accounts
#         )

#         filtered_df = transactions.copy()

#         if selected_account != "All":
#             filtered_df = filtered_df[filtered_df["account_name"] == selected_account]

#         st.subheader("Transactions for Selected Account")
#         st.dataframe(
#             filtered_df[
#                 [
#                     "date",
#                     "description",
#                     "amount",
#                     "transaction_type",
#                     "category",
#                     "account_name"
#                 ]
#             ]
#         )

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def spending_analysis_page():
#     st.header("Spending Analysis")

#     try:
#         transactions = load_transactions()

#         categories = ["All"] + sorted(transactions["category"].unique().tolist())

#         selected_category = st.selectbox(
#             "Filter by category",
#             categories
#         )

#         filtered_df = transactions.copy()

#         if selected_category != "All":
#             filtered_df = filtered_df[filtered_df["category"] == selected_category]

#         st.subheader("Filtered Transactions")

#         st.dataframe(
#             filtered_df[
#                 [
#                     "date",
#                     "description",
#                     "amount",
#                     "transaction_type",
#                     "category",
#                     "account_name"
#                 ]
#             ]
#         )

#         st.subheader("Top Descriptions by Spending")

#         description_df = top_descriptions(filtered_df)

#         fig = px.bar(
#             description_df,
#             x="description",
#             y="expense",
#             title="Top Spending Descriptions"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#         st.subheader("Yearly Summary")

#         yearly_df = yearly_summary(filtered_df)

#         fig2 = px.bar(
#             yearly_df,
#             x="year",
#             y=["income", "expense"],
#             barmode="group",
#             title="Yearly Income vs Expense"
#         )

#         st.plotly_chart(fig2, use_container_width=True)

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def prediction_page():
#     st.header("Machine Learning Spending Prediction")

#     try:
#         transactions = load_transactions()

#         model, results, monthly = train_spending_model(transactions)
#         prediction = predict_next_month(model, monthly)

#         st.metric(
#             "Predicted Spending Next Month",
#             f"£{prediction:,.2f}"
#         )

#         st.subheader("Model Evaluation")
#         st.write(f"Mean Absolute Error: £{results['mae']:,.2f}")
#         st.write(f"R² Score: {results['r2_score']:.2f}")

#         st.subheader("Monthly Data Used by the Model")
#         st.dataframe(monthly)

#         fig = px.line(
#             monthly,
#             x="month",
#             y=["expense", "predicted_expense"],
#             markers=True,
#             title="Actual vs Predicted Monthly Spending"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def unusual_transactions_page():
#     st.header("Unusual Transaction Detection")

#     try:
#         transactions = load_transactions()

#         risk_df = detect_unusual_transactions(transactions)

#         suspicious = risk_df[risk_df["risk_status"] == "Suspicious"]

#         st.metric("Unusual Transactions Found", len(suspicious))

#         if len(suspicious) > 0:
#             st.warning("Some transactions are unusually high compared with normal spending.")

#             st.dataframe(
#                 suspicious[
#                     [
#                         "date",
#                         "description",
#                         "amount",
#                         "transaction_type",
#                         "category",
#                         "account_name",
#                         "risk_status",
#                         "risk_reason"
#                     ]
#                 ]
#             )
#         else:
#             st.success("No unusual transactions detected.")

#         st.subheader("All Transactions with Risk Status")

#         st.dataframe(
#             risk_df[
#                 [
#                     "date",
#                     "description",
#                     "amount",
#                     "transaction_type",
#                     "category",
#                     "account_name",
#                     "risk_status",
#                     "risk_reason"
#                 ]
#             ]
#         )

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def blockchain_audit_page():
#     st.header("Blockchain-Style Transaction Audit")

#     try:
#         transactions = load_transactions()

#         st.write(
#             "This page uses SHA-256 hashing to create a tamper-evident record for each transaction."
#         )

#         if "transaction_hash" not in transactions.columns:
#             st.error("No transaction hash found. Please upload the transactions again.")
#             return

#         transactions["hash_valid"] = transactions.apply(
#             verify_transaction_hash,
#             axis=1
#         )

#         valid_count = transactions["hash_valid"].sum()
#         invalid_count = len(transactions) - valid_count

#         col1, col2 = st.columns(2)

#         col1.metric("Valid Hashes", valid_count)
#         col2.metric("Invalid Hashes", invalid_count)

#         st.dataframe(
#             transactions[
#                 [
#                     "date",
#                     "description",
#                     "amount",
#                     "transaction_type",
#                     "category",
#                     "account_name",
#                     "transaction_hash",
#                     "hash_valid"
#                 ]
#             ]
#         )

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def ai_insights_page():
#     st.header("AI-Style Financial Insights")

#     try:
#         transactions = load_transactions()
#         budget = load_budget()

#         insights = generate_financial_insights(transactions, budget)

#         for insight in insights:
#             st.info(insight)

#     except Exception:
#         st.warning("Please upload both datasets first.")


# def about_page():
#     st.header("About SmartBank AI")

#     st.write("""
#     SmartBank AI is a personal finance and banking analytics prototype built with Python.

#     The application uses two connected datasets:

#     1. personal_transactions.csv
#        - Date
#        - Description
#        - Amount
#        - Transaction Type
#        - Category
#        - Account Name

#     2. Budget.csv
#        - Category
#        - Budget

#     The system demonstrates:

#     - CSV data extraction
#     - Data validation
#     - Data cleaning
#     - SQLite local storage
#     - Financial dashboarding
#     - Budget tracking
#     - Account/card analysis
#     - Machine learning spending prediction
#     - Unusual transaction detection
#     - Blockchain-style SHA-256 transaction auditing
#     - AI-style personalised financial insights
#     - Interactive Streamlit user experience
#     """)


# if __name__ == "__main__":
#     main()


import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from src.validate import (
    validate_transaction_columns,
    validate_budget_columns,
    check_empty_data,
)
from src.clean import clean_transactions, clean_budget
from src.database import save_to_database, load_transactions, load_budget
from src.analytics import (
    calculate_summary,
    spending_by_category,
    monthly_spending,
    monthly_income,
    yearly_summary,
    spending_by_account,
    top_descriptions,
)
from src.budget_analysis import compare_budget_to_actual
from src.ml_model import train_spending_model, predict_next_month
from src.fraud_detection import detect_unusual_transactions
from src.blockchain_audit import add_transaction_hashes, verify_transaction_hash
from src.insights import generate_financial_insights
from src.column_mapper import map_uploaded_columns
from src.manual_entry import add_manual_transaction, add_manual_budget

st.set_page_config(
    page_title="SmartBank AI",
    page_icon="🏦",
    layout="wide",
)


TRANSACTION_DISPLAY_COLUMNS = [
    "date",
    "description",
    "amount",
    "transaction_type",
    "category",
    "account_name",
    "location",
    "payment_method",
]


def save_raw_file(uploaded_file, prefix):
    """
    Save uploaded CSV files to data/raw.
    """

    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/raw/{prefix}_{timestamp}.csv"

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def get_available_display_columns(df, extra_columns=None):
    """
    Return only the columns that exist in the dataframe.
    This prevents errors if optional columns are missing.
    """

    columns = TRANSACTION_DISPLAY_COLUMNS.copy()

    if extra_columns:
        columns.extend(extra_columns)

    return [column for column in columns if column in df.columns]


def main():
    st.title("🏦 SmartBank AI")
    st.write("Personal Finance and Budget Intelligence App")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Data Input",
            "Data Quality",
            "Dashboard",
            "Budget Tracker",
            "Account Analysis",
            "Spending Analysis",
            "Prediction",
            "Unusual Transactions",
            "Blockchain Audit",
            "AI Insights",
            "About",
        ],
    )

    if menu == "Data Input":
        data_input_page()
    elif menu == "Data Quality":
        data_quality_page()
    elif menu == "Dashboard":
        dashboard_page()
    elif menu == "Budget Tracker":
        budget_tracker_page()
    elif menu == "Account Analysis":
        account_analysis_page()
    elif menu == "Spending Analysis":
        spending_analysis_page()
    elif menu == "Prediction":
        prediction_page()
    elif menu == "Unusual Transactions":
        unusual_transactions_page()
    elif menu == "Blockchain Audit":
        blockchain_audit_page()
    elif menu == "AI Insights":
        ai_insights_page()
    elif menu == "About":
        about_page()


def data_input_page():
    st.header("Data Input")

    st.write(
        "Choose how you want to provide your financial data. "
        "You can upload the original project datasets, upload a different CSV using column mapping, "
        "or enter transactions and budgets manually."
    )

    input_method = st.radio(
        "Choose input method",
        [
            "Upload Original Transactions and Budget Files",
            "Upload Different Transaction CSV With Column Mapping",
            "Enter Transaction Manually",
            "Enter Budget Manually",
        ],
    )

    if input_method == "Upload Original Transactions and Budget Files":
        upload_data_page()

    elif input_method == "Upload Different Transaction CSV With Column Mapping":
        flexible_csv_upload_section()

    elif input_method == "Enter Transaction Manually":
        manual_transaction_entry_section()

    elif input_method == "Enter Budget Manually":
        manual_budget_entry_section()


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
        st.dataframe(transactions_df.head())

        st.subheader("Raw Budget Preview")
        st.dataframe(budget_df.head())

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
        st.dataframe(cleaned_transactions.head())

        st.subheader("Cleaned Budget Preview")
        st.dataframe(cleaned_budget.head())


def flexible_csv_upload_section():
    st.subheader("Upload Different Transaction CSV With Column Mapping")

    st.write(
        "Use this option if your CSV has different column names. "
        "You will map your columns to the fields SmartBank AI needs."
    )

    uploaded_file = st.file_uploader(
        "Upload any transaction CSV file",
        type=["csv"],
        key="flexible_transaction_upload",
    )

    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)

        st.write("Uploaded Data Preview")
        st.dataframe(raw_df.head())

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
            st.dataframe(cleaned_df.head())

            st.info(
                "This option updates the transactions table only. "
                "To use the Budget Tracker, add budget data through the manual budget entry option "
                "or upload the original Budget.csv file."
            )


def manual_transaction_entry_section():
    st.subheader("Enter Transaction Manually")

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

        category = st.text_input(
            "Category",
            value="Other",
        )

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
            st.dataframe(updated_transactions.tail())


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
            st.dataframe(updated_budget)


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
        st.dataframe(missing_transactions)

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
        st.dataframe(missing_budget)

    except Exception:
        st.info("No budget data found yet. Add a budget manually or upload Budget.csv.")


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

            st.plotly_chart(fig, use_container_width=True)

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

            st.plotly_chart(fig2, use_container_width=True)

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

            st.plotly_chart(fig3, use_container_width=True)

    except Exception:
        st.warning("Please add or upload transaction data first.")


def budget_tracker_page():
    st.header("Budget Tracker")

    try:
        transactions = load_transactions()
        budget = load_budget()

        comparison = compare_budget_to_actual(transactions, budget)

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

        col1.metric("Over Budget", over_budget_count)
        col2.metric("Close to Limit", close_to_limit_count)
        col3.metric("Within Budget", within_budget_count)

        st.subheader("Budget Comparison Table")

        st.dataframe(
            comparison[
                [
                    "category",
                    "budget",
                    "actual_spending",
                    "remaining_budget",
                    "percentage_used",
                    "budget_status",
                ]
            ]
        )

        st.subheader("Actual Spending vs Budget")

        fig = px.bar(
            comparison,
            x="category",
            y=["budget", "actual_spending"],
            barmode="group",
            title="Budget vs Actual Spending",
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception:
        st.warning(
            "Please add both transaction data and budget data first. "
            "You can upload files or enter budget categories manually."
        )


def account_analysis_page():
    st.header("Account Analysis")

    try:
        transactions = load_transactions()

        if "account_name" not in transactions.columns:
            st.warning("No account name column found.")
            return

        account_df = spending_by_account(transactions)

        st.subheader("Spending by Account")

        if account_df.empty:
            st.info("No account spending data available.")
        else:
            fig = px.bar(
                account_df,
                x="account_name",
                y="expense",
                title="Spending by Account or Card",
            )

            st.plotly_chart(fig, use_container_width=True)

        accounts = ["All"] + sorted(
            transactions["account_name"].dropna().unique().tolist()
        )

        selected_account = st.selectbox(
            "Filter by account",
            accounts,
        )

        filtered_df = transactions.copy()

        if selected_account != "All":
            filtered_df = filtered_df[filtered_df["account_name"] == selected_account]

        st.subheader("Transactions for Selected Account")
        st.dataframe(filtered_df[get_available_display_columns(filtered_df)])

    except Exception:
        st.warning("Please add or upload transaction data first.")


def spending_analysis_page():
    st.header("Spending Analysis")

    try:
        transactions = load_transactions()

        categories = ["All"] + sorted(
            transactions["category"].dropna().unique().tolist()
        )

        selected_category = st.selectbox(
            "Filter by category",
            categories,
        )

        filtered_df = transactions.copy()

        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]

        st.subheader("Filtered Transactions")

        st.dataframe(filtered_df[get_available_display_columns(filtered_df)])

        st.subheader("Top Descriptions by Spending")

        description_df = top_descriptions(filtered_df)

        if description_df.empty:
            st.info("No description spending data available.")
        else:
            fig = px.bar(
                description_df,
                x="description",
                y="expense",
                title="Top Spending Descriptions",
            )

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Yearly Summary")

        yearly_df = yearly_summary(filtered_df)

        if yearly_df.empty:
            st.info("No yearly data available.")
        else:
            fig2 = px.bar(
                yearly_df,
                x="year",
                y=["income", "expense"],
                barmode="group",
                title="Yearly Income vs Expense",
            )

            st.plotly_chart(fig2, use_container_width=True)

    except Exception:
        st.warning("Please add or upload transaction data first.")


def prediction_page():
    st.header("Machine Learning Spending Prediction")

    try:
        transactions = load_transactions()

        monthly_check = monthly_spending(transactions)

        if len(monthly_check) < 6:
            st.warning(
                "Not enough historical data for reliable prediction. "
                "Please add at least 6 months of transactions for better forecasting."
            )

            st.write(
                "You can still use the dashboard, budget tracker, spending analysis, "
                "unusual transaction detection, blockchain audit, and AI insights."
            )

            st.subheader("Current Monthly Spending Data")
            st.dataframe(monthly_check)

            if not monthly_check.empty:
                fig = px.line(
                    monthly_check,
                    x="month",
                    y="expense",
                    markers=True,
                    title="Current Monthly Spending",
                )

                st.plotly_chart(fig, use_container_width=True)

            return

        model, results, monthly = train_spending_model(transactions)
        prediction = predict_next_month(model, monthly)

        st.metric(
            "Predicted Spending Next Month",
            f"£{prediction:,.2f}",
        )

        st.subheader("Model Evaluation")
        st.write(f"Mean Absolute Error: £{results['mae']:,.2f}")
        st.write(f"R² Score: {results['r2_score']:.2f}")

        if results["r2_score"] < 0.3:
            st.info(
                "The R² score is low, which suggests that the spending pattern is not strongly linear. "
                "The prediction should be treated as a prototype estimate, not a guaranteed forecast."
            )

        st.subheader("Monthly Data Used by the Model")
        st.dataframe(monthly)

        fig = px.line(
            monthly,
            x="month",
            y=["expense", "predicted_expense"],
            markers=True,
            title="Actual vs Predicted Monthly Spending",
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception:
        st.warning("Please add or upload transaction data first.")


def unusual_transactions_page():
    st.header("Unusual Transaction Detection")

    try:
        transactions = load_transactions()

        risk_df = detect_unusual_transactions(transactions)

        suspicious = risk_df[risk_df["risk_status"] == "Suspicious"]

        st.metric("Unusual Transactions Found", len(suspicious))

        risk_columns = get_available_display_columns(
            risk_df,
            extra_columns=["risk_status", "risk_reason"],
        )

        if len(suspicious) > 0:
            st.warning(
                "Some transactions are unusually high compared with normal spending."
            )

            st.dataframe(suspicious[risk_columns])
        else:
            st.success("No unusual transactions detected.")

        st.subheader("All Transactions with Risk Status")

        st.dataframe(risk_df[risk_columns])

    except Exception:
        st.warning("Please add or upload transaction data first.")


def blockchain_audit_page():
    st.header("Blockchain-Style Transaction Audit")

    try:
        transactions = load_transactions()

        st.write(
            "This page uses SHA-256 hashing to create a tamper-evident record for each transaction."
        )

        if "transaction_hash" not in transactions.columns:
            st.error(
                "No transaction hash found. Please upload or add transactions again."
            )
            return

        transactions["hash_valid"] = transactions.apply(
            verify_transaction_hash,
            axis=1,
        )

        valid_count = transactions["hash_valid"].sum()
        invalid_count = len(transactions) - valid_count

        col1, col2 = st.columns(2)

        col1.metric("Valid Hashes", valid_count)
        col2.metric("Invalid Hashes", invalid_count)

        audit_columns = get_available_display_columns(
            transactions,
            extra_columns=["transaction_hash", "hash_valid"],
        )

        st.dataframe(transactions[audit_columns])

    except Exception:
        st.warning("Please add or upload transaction data first.")


def ai_insights_page():
    st.header("AI-Style Financial Insights")

    try:
        transactions = load_transactions()

        try:
            budget = load_budget()
        except Exception:
            budget = pd.DataFrame(columns=["category", "budget"])

        if budget.empty:
            st.info(
                "No budget data found. Add budget categories to receive budget-related insights."
            )

        insights = generate_financial_insights(transactions, budget)

        for insight in insights:
            st.info(insight)

    except Exception:
        st.warning("Please add or upload transaction data first.")


def about_page():
    st.header("About SmartBank AI")

    st.write("""
        SmartBank AI is a personal finance and banking analytics prototype built with Python.

        The application supports multiple data input methods:

        1. Upload the original project datasets
           - personal_transactions.csv
           - Budget.csv

        2. Upload a different transaction CSV using column mapping

        3. Enter transactions manually

        4. Enter budget categories manually

        The system demonstrates:

        - CSV data extraction
        - Flexible data input
        - Column mapping
        - Manual transaction entry
        - Manual budget entry
        - Data validation
        - Data cleaning
        - SQLite local storage
        - Financial dashboarding
        - Budget tracking
        - Account/card analysis
        - Machine learning spending prediction
        - Unusual transaction detection
        - Blockchain-style SHA-256 transaction auditing
        - AI-style personalised financial insights
        - Interactive Streamlit user experience
        """)


if __name__ == "__main__":
    main()
