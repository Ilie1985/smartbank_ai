import sqlite3
import uuid
from pathlib import Path

import pandas as pd

USER_DB_PATH = "database/user_inputs.db"


def create_user_database_folder():
    """
    Create database folder if it does not exist.
    """

    Path("database").mkdir(exist_ok=True)


def prepare_dataframe_for_sqlite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date/object columns into SQLite-safe values.
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


def load_user_transactions() -> pd.DataFrame:
    """
    Load manually entered transactions from user_inputs.db.
    """

    create_user_database_folder()

    conn = sqlite3.connect(USER_DB_PATH)

    try:
        df = pd.read_sql_query("SELECT * FROM manual_transactions", conn)
    except Exception:
        df = pd.DataFrame()

    conn.close()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df


def save_user_transactions(df: pd.DataFrame) -> None:
    """
    Save manually entered transactions to user_inputs.db.
    """

    create_user_database_folder()

    safe_df = prepare_dataframe_for_sqlite(df)

    conn = sqlite3.connect(USER_DB_PATH)

    safe_df.to_sql("manual_transactions", conn, if_exists="replace", index=False)

    conn.close()


def add_user_transaction(transaction_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a cleaned manual transaction to the manual transactions table.
    """

    data = transaction_df.copy()

    if "manual_id" not in data.columns:
        data["manual_id"] = [str(uuid.uuid4()) for _ in range(len(data))]

    existing = load_user_transactions()

    if existing.empty:
        updated = data
    else:
        updated = pd.concat([existing, data], ignore_index=True)

    save_user_transactions(updated)

    return updated


def update_user_transaction(manual_id: str, updated_values: dict) -> pd.DataFrame:
    """
    Update one manually entered transaction.
    """

    df = load_user_transactions()

    if df.empty:
        return df

    for column, value in updated_values.items():
        if column in df.columns:
            df.loc[df["manual_id"] == manual_id, column] = value

    save_user_transactions(df)

    return df


def delete_user_transaction(manual_id: str) -> pd.DataFrame:
    """
    Delete one manually entered transaction.
    """

    df = load_user_transactions()

    if df.empty:
        return df

    df = df[df["manual_id"] != manual_id]

    save_user_transactions(df)

    return df


def load_user_budget() -> pd.DataFrame:
    """
    Load manually entered budget data.
    """

    create_user_database_folder()

    conn = sqlite3.connect(USER_DB_PATH)

    try:
        df = pd.read_sql_query("SELECT * FROM manual_budget", conn)
    except Exception:
        df = pd.DataFrame()

    conn.close()

    return df


def save_user_budget(df: pd.DataFrame) -> None:
    """
    Save manually entered budget data.
    """

    create_user_database_folder()

    safe_df = prepare_dataframe_for_sqlite(df)

    conn = sqlite3.connect(USER_DB_PATH)

    safe_df.to_sql("manual_budget", conn, if_exists="replace", index=False)

    conn.close()


def add_or_update_user_budget(category: str, budget: float) -> pd.DataFrame:
    """
    Add or update one manual budget category.
    """

    existing = load_user_budget()

    new_row = pd.DataFrame(
        [{"category": str(category).strip().title(), "budget": float(budget)}]
    )

    if existing.empty:
        updated = new_row
    else:
        existing["category"] = existing["category"].astype(str).str.strip().str.title()

        existing = existing[existing["category"] != str(category).strip().title()]

        updated = pd.concat([existing, new_row], ignore_index=True)

    save_user_budget(updated)

    return updated


def delete_user_budget(category: str) -> pd.DataFrame:
    """
    Delete one manual budget category.
    """

    df = load_user_budget()

    if df.empty:
        return df

    df["category"] = df["category"].astype(str).str.strip().str.title()

    df = df[df["category"] != str(category).strip().title()]

    save_user_budget(df)

    return df
