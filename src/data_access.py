import os
import sqlite3

import pandas as pd
import streamlit as st


DATABASE_DIR = "database"

UPLOADED_TRANSACTIONS_DB = os.path.join(DATABASE_DIR, "uploaded_transactions.db")
UPLOADED_BUDGET_DB = os.path.join(DATABASE_DIR, "uploaded_budget.db")

MANUAL_TRANSACTIONS_DB = os.path.join(DATABASE_DIR, "manual_transactions.db")
MANUAL_BUDGET_DB = os.path.join(DATABASE_DIR, "manual_budget.db")

# Old fallback database, only used if your older functions still saved there.
USER_INPUTS_DB = os.path.join(DATABASE_DIR, "user_inputs.db")


TRANSACTION_COLUMNS = [
    "date",
    "description",
    "amount",
    "transaction_type",
    "category",
    "account_name",
    "location",
    "payment_method",
    "balance",
    "month",
    "year",
    "day",
    "income",
    "expense",
    "transaction_hash",
    "data_source",
    "manual_id",
]

BUDGET_COLUMNS = [
    "category",
    "budget",
]


def get_data_source_mode() -> str:
    """
    Get the selected data source mode from Streamlit session state.
    """

    return st.session_state.get("data_source_mode", "All data")


def read_table_from_db(db_path: str, table_name: str) -> pd.DataFrame:
    """
    Safely read a table from a SQLite database.
    If the database or table does not exist, return an empty dataframe.
    """

    if not os.path.exists(db_path):
        return pd.DataFrame()

    try:
        with sqlite3.connect(db_path) as connection:
            return pd.read_sql_query(
                f"SELECT * FROM {table_name}",
                connection,
            )
    except Exception:
        return pd.DataFrame()


def standardise_transaction_columns(df: pd.DataFrame, data_source: str) -> pd.DataFrame:
    """
    Make sure transaction data has the expected columns.
    """

    if df.empty:
        return pd.DataFrame(columns=TRANSACTION_COLUMNS)

    data = df.copy()

    if "data_source" not in data.columns:
        data["data_source"] = data_source

    for column in TRANSACTION_COLUMNS:
        if column not in data.columns:
            data[column] = None

    return data[TRANSACTION_COLUMNS]


def standardise_budget_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Make sure budget data has the expected columns.
    """

    if df.empty:
        return pd.DataFrame(columns=BUDGET_COLUMNS)

    data = df.copy()

    for column in BUDGET_COLUMNS:
        if column not in data.columns:
            data[column] = None

    return data[BUDGET_COLUMNS]


def load_uploaded_transactions() -> pd.DataFrame:
    """
    Load uploaded CSV transactions.
    """

    uploaded = read_table_from_db(
        UPLOADED_TRANSACTIONS_DB,
        "transactions",
    )

    # Fallback for older project versions that saved uploaded data into banking.db.
    if uploaded.empty:
        legacy_db = os.path.join(DATABASE_DIR, "banking.db")
        uploaded = read_table_from_db(legacy_db, "transactions")

    return standardise_transaction_columns(uploaded, "Uploaded CSV")


def load_manual_transactions() -> pd.DataFrame:
    """
    Load manually entered transactions.
    """

    manual = read_table_from_db(
        MANUAL_TRANSACTIONS_DB,
        "manual_transactions",
    )

    # Fallback for older project versions.
    if manual.empty:
        manual = read_table_from_db(
            USER_INPUTS_DB,
            "manual_transactions",
        )

    return standardise_transaction_columns(manual, "Manual Entry")


def load_uploaded_budget() -> pd.DataFrame:
    """
    Load uploaded budget data.
    """

    uploaded_budget = read_table_from_db(
        UPLOADED_BUDGET_DB,
        "budget",
    )

    # Fallback for older project versions that saved budget into banking.db.
    if uploaded_budget.empty:
        legacy_db = os.path.join(DATABASE_DIR, "banking.db")
        uploaded_budget = read_table_from_db(legacy_db, "budget")

    return standardise_budget_columns(uploaded_budget)


def load_manual_budget() -> pd.DataFrame:
    """
    Load manually entered budget data.
    """

    manual_budget = read_table_from_db(
        MANUAL_BUDGET_DB,
        "manual_budget",
    )

    # Fallback for older project versions.
    if manual_budget.empty:
        manual_budget = read_table_from_db(
            USER_INPUTS_DB,
            "manual_budget",
        )

    return standardise_budget_columns(manual_budget)


def load_app_transactions() -> pd.DataFrame:
    """
    Load transactions according to the selected data source mode.

    Modes:
    - All data
    - Manual data only
    - Uploaded CSV data only
    """

    mode = get_data_source_mode()

    uploaded = load_uploaded_transactions()
    manual = load_manual_transactions()

    if mode == "Manual data only":
        return manual

    if mode == "Uploaded CSV data only":
        return uploaded

    combined = pd.concat(
        [uploaded, manual],
        ignore_index=True,
    )

    return combined


def load_app_budget() -> pd.DataFrame:
    """
    Load budget according to the selected data source mode.

    Manual budgets are preferred in All data mode because they represent
    the user's active budget plan.
    """

    mode = get_data_source_mode()

    manual_budget = load_manual_budget()
    uploaded_budget = load_uploaded_budget()

    if mode == "Manual data only":
        return manual_budget

    if mode == "Uploaded CSV data only":
        return uploaded_budget

    # In All data mode, prefer manual budget if it exists.
    if not manual_budget.empty:
        return manual_budget

    return uploaded_budget