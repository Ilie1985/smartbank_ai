import sqlite3
import pandas as pd
from pathlib import Path


DB_PATH = "database/banking.db"


def create_database_folder():
    """
    Create the database folder if it does not exist.
    """

    Path("database").mkdir(exist_ok=True)


def prepare_dataframe_for_sqlite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare a DataFrame before saving it to SQLite.

    SQLite can sometimes fail when saving Python date, datetime,
    Timestamp, or complex object values. This function converts them
    into safe text or numeric values.
    """

    data = df.copy()

    for column in data.columns:
        # Convert datetime columns to string
        if pd.api.types.is_datetime64_any_dtype(data[column]):
            data[column] = data[column].astype(str)

        # Convert object columns safely
        elif data[column].dtype == "object":
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
        index=False
    )

    conn.close()


def load_table(table_name: str) -> pd.DataFrame:
    """
    Load a table from SQLite.
    """

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        conn
    )

    conn.close()

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