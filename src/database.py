import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = "database/banking.db"


def create_database_folder():
    """
    Create the database folder if it does not exist.
    """

    Path("database").mkdir(exist_ok=True)


def prepare_dataframe_for_sqlite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare a DataFrame before saving it to SQLite.

    This converts date, datetime, Timestamp, and object values into SQLite-safe values.
    """

    data = df.copy()

    for column in data.columns:
        # Handle common date column
        if column == "date":
            data[column] = pd.to_datetime(data[column], errors="coerce")
            data[column] = data[column].dt.strftime("%Y-%m-%d")
            continue

        # Convert datetime columns to text
        if pd.api.types.is_datetime64_any_dtype(data[column]):
            data[column] = data[column].dt.strftime("%Y-%m-%d")
            continue

        # Convert object columns safely
        if data[column].dtype == "object":
            data[column] = data[column].apply(
                lambda value: str(value) if value is not None else ""
            )

    return data


def save_to_database(df: pd.DataFrame, table_name: str) -> None:
    """
    Save a DataFrame into SQLite.
    """

    create_database_folder()

    safe_df = prepare_dataframe_for_sqlite(df)

    conn = sqlite3.connect(DB_PATH)

    safe_df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


def load_table(table_name: str) -> pd.DataFrame:
    """
    Load a table from SQLite.
    """

    conn = sqlite3.connect(DB_PATH)

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
    Load transactions table.
    """

    return load_table("transactions")


def load_budget() -> pd.DataFrame:
    """
    Load budget table.
    """

    return load_table("budget")