import sqlite3
from pathlib import Path

import pandas as pd


UPLOADED_TRANSACTIONS_DB_PATH = "database/uploaded_transactions.db"
UPLOADED_BUDGET_DB_PATH = "database/uploaded_budget.db"


def create_database_folder():
    """
    Create the database folder if it does not exist.
    """

    Path("database").mkdir(exist_ok=True)


def prepare_dataframe_for_sqlite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare a DataFrame before saving it to SQLite.
    """

    data = df.copy()

    for column in data.columns:
        if column == "date":
            data[column] = pd.to_datetime(data[column], errors="coerce")
            data[column] = data[column].dt.strftime("%Y-%m-%d")
            continue

        if pd.api.types.is_datetime64_any_dtype(data[column]):
            data[column] = data[column].dt.strftime("%Y-%m-%d")
            continue

        if data[column].dtype == "object":
            data[column] = data[column].apply(
                lambda value: str(value) if value is not None else ""
            )

    return data


def save_to_database(df: pd.DataFrame, table_name: str) -> None:
    """
    Save uploaded CSV data into the correct SQLite database.
    """

    create_database_folder()

    safe_df = prepare_dataframe_for_sqlite(df)

    if table_name == "transactions":
        db_path = UPLOADED_TRANSACTIONS_DB_PATH
    elif table_name == "budget":
        db_path = UPLOADED_BUDGET_DB_PATH
    else:
        raise ValueError(f"Unknown table name: {table_name}")

    conn = sqlite3.connect(db_path)

    safe_df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


def load_table(db_path: str, table_name: str) -> pd.DataFrame:
    """
    Load a table from SQLite.
    """

    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        conn,
    )

    conn.close()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df


def load_transactions() -> pd.DataFrame:
    """
    Load uploaded CSV transactions.
    """

    return load_table(
        UPLOADED_TRANSACTIONS_DB_PATH,
        "transactions",
    )


def load_budget() -> pd.DataFrame:
    """
    Load uploaded CSV budget.
    """

    return load_table(
        UPLOADED_BUDGET_DB_PATH,
        "budget",
    )