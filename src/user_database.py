import sqlite3
import uuid
from pathlib import Path

import pandas as pd

MANUAL_TRANSACTIONS_DB_PATH = "database/manual_transactions.db"
MANUAL_BUDGET_DB_PATH = "database/manual_budget.db"

MANUAL_INCOME_DB_PATH = "database/manual_income.db"


def create_user_database_folder():
    """
    Create database folder if it does not exist.
    """

    Path("database").mkdir(exist_ok=True)


def prepare_dataframe_for_sqlite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert dataframe values into SQLite-safe values.
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


def table_exists(db_path: str, table_name: str) -> bool:
    """
    Check if a table exists in a database file.
    """

    create_user_database_folder()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
        """,
        (table_name,),
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def load_user_transactions() -> pd.DataFrame:
    """
    Load manually entered transactions from manual_transactions.db.
    """

    create_user_database_folder()

    if not table_exists(MANUAL_TRANSACTIONS_DB_PATH, "manual_transactions"):
        return pd.DataFrame()

    conn = sqlite3.connect(MANUAL_TRANSACTIONS_DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM manual_transactions",
        conn,
    )

    conn.close()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df


def save_user_transactions(df: pd.DataFrame) -> None:
    """
    Save manually entered transactions to manual_transactions.db.
    """

    create_user_database_folder()

    safe_df = prepare_dataframe_for_sqlite(df)

    conn = sqlite3.connect(MANUAL_TRANSACTIONS_DB_PATH)

    safe_df.to_sql(
        "manual_transactions",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


def add_user_transaction(transaction_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add cleaned manual transactions to the manual_transactions table.
    """

    data = transaction_df.copy()

    if "manual_id" not in data.columns:
        data["manual_id"] = [str(uuid.uuid4()) for _ in range(len(data))]

    existing = load_user_transactions()

    if existing.empty:
        updated = data
    else:
        updated = pd.concat(
            [existing, data],
            ignore_index=True,
            sort=False,
        )

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
    Load manually entered budget data from manual_budget.db.
    """

    create_user_database_folder()

    if not table_exists(MANUAL_BUDGET_DB_PATH, "manual_budget"):
        return pd.DataFrame()

    conn = sqlite3.connect(MANUAL_BUDGET_DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM manual_budget",
        conn,
    )

    conn.close()

    return df


def save_user_budget(df: pd.DataFrame) -> None:
    """
    Save manually entered budget data to manual_budget.db.
    """

    create_user_database_folder()

    safe_df = prepare_dataframe_for_sqlite(df)

    conn = sqlite3.connect(MANUAL_BUDGET_DB_PATH)

    safe_df.to_sql(
        "manual_budget",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


def add_or_update_user_budget(category: str, budget: float) -> pd.DataFrame:
    """
    Add or update one manual budget category.
    """

    existing = load_user_budget()

    new_row = pd.DataFrame(
        [
            {
                "category": str(category).strip().title(),
                "budget": float(budget),
            }
        ]
    )

    if existing.empty:
        updated = new_row
    else:
        existing["category"] = existing["category"].astype(str).str.strip().str.title()
        existing = existing[existing["category"] != str(category).strip().title()]

        updated = pd.concat(
            [existing, new_row],
            ignore_index=True,
            sort=False,
        )

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


def list_user_tables() -> dict:
    """
    List tables from the manual transaction and manual budget databases.
    Useful for debugging.
    """

    database_files = {
        "manual_transactions_db": MANUAL_TRANSACTIONS_DB_PATH,
        "manual_budget_db": MANUAL_BUDGET_DB_PATH,
    }

    result = {}

    for database_name, database_path in database_files.items():
        create_user_database_folder()

        conn = sqlite3.connect(database_path)

        tables = pd.read_sql_query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
            """,
            conn,
        )

        conn.close()

        result[database_name] = tables["name"].tolist()

    return result


def load_user_income() -> pd.DataFrame:
    """
    Load manually entered monthly income from manual_income.db.
    """

    create_user_database_folder()

    if not table_exists(MANUAL_INCOME_DB_PATH, "manual_income"):
        return pd.DataFrame(columns=["month", "income"])

    conn = sqlite3.connect(MANUAL_INCOME_DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM manual_income",
        conn,
    )

    conn.close()

    return df


def save_user_income(df: pd.DataFrame) -> None:
    """
    Save manually entered monthly income to manual_income.db.
    """

    create_user_database_folder()

    safe_df = prepare_dataframe_for_sqlite(df)

    conn = sqlite3.connect(MANUAL_INCOME_DB_PATH)

    safe_df.to_sql(
        "manual_income",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


def add_or_update_user_income(month: str, income: float) -> pd.DataFrame:
    """
    Add or update income for a selected month.
    """

    existing = load_user_income()

    new_row = pd.DataFrame(
        [
            {
                "month": str(month),
                "income": float(income),
            }
        ]
    )

    if existing.empty:
        updated = new_row
    else:
        existing["month"] = existing["month"].astype(str)
        existing = existing[existing["month"] != str(month)]

        updated = pd.concat(
            [existing, new_row],
            ignore_index=True,
            sort=False,
        )

    save_user_income(updated)

    return updated


def delete_user_income(month: str) -> pd.DataFrame:
    """
    Delete income for a selected month.
    """

    df = load_user_income()

    if df.empty:
        return df

    df["month"] = df["month"].astype(str)
    df = df[df["month"] != str(month)]

    save_user_income(df)

    return df
