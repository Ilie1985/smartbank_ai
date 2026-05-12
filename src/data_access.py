import pandas as pd

from src.database import load_transactions, load_budget
from src.user_database import load_user_transactions, load_user_budget


def standardise_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise combined uploaded and manual transaction data.
    """

    data = df.copy()

    if "date" in data.columns:
        date_values = pd.to_datetime(data["date"], errors="coerce")
        data["date"] = date_values.dt.strftime("%Y-%m-%d")

        data["month"] = date_values.dt.to_period("M").astype(str)
        data["year"] = date_values.dt.year
        data["day"] = date_values.dt.day

    if "amount" in data.columns:
        data["amount"] = pd.to_numeric(data["amount"], errors="coerce").fillna(0)

    if "income" not in data.columns and "transaction_type" in data.columns:
        data["income"] = data.apply(
            lambda row: abs(row["amount"])
            if str(row["transaction_type"]).lower() == "credit"
            else 0,
            axis=1,
        )

    if "expense" not in data.columns and "transaction_type" in data.columns:
        data["expense"] = data.apply(
            lambda row: abs(row["amount"])
            if str(row["transaction_type"]).lower() == "debit"
            else 0,
            axis=1,
        )

    optional_columns = ["account_name", "location", "payment_method"]

    for column in optional_columns:
        if column not in data.columns:
            data[column] = "Unknown"

    return data


def load_app_transactions() -> pd.DataFrame:
    """
    Load all transaction data used by the app.

    This combines:
    - uploaded CSV transactions from banking.db
    - manual transactions from user_inputs.db
    """

    frames = []

    try:
        uploaded_transactions = load_transactions()

        if not uploaded_transactions.empty:
            uploaded_transactions["data_source"] = "Uploaded CSV"
            frames.append(uploaded_transactions)

    except Exception:
        pass

    try:
        manual_transactions = load_user_transactions()

        if not manual_transactions.empty:
            manual_transactions["data_source"] = "Manual Entry"
            frames.append(manual_transactions)

    except Exception:
        pass

    if not frames:
        raise FileNotFoundError("No transaction data found.")

    combined = pd.concat(
        frames,
        ignore_index=True,
        sort=False,
    )

    combined = standardise_transactions(combined)

    return combined


def load_app_budget() -> pd.DataFrame:
    """
    Load all budget data used by the app.

    This combines:
    - uploaded CSV budget from banking.db
    - manual budget from user_inputs.db

    If a category exists in both places, the manual budget overrides the uploaded one.
    """

    frames = []

    try:
        uploaded_budget = load_budget()

        if not uploaded_budget.empty:
            uploaded_budget["data_source"] = "Uploaded CSV"
            frames.append(uploaded_budget)

    except Exception:
        pass

    try:
        manual_budget = load_user_budget()

        if not manual_budget.empty:
            manual_budget["data_source"] = "Manual Entry"
            frames.append(manual_budget)

    except Exception:
        pass

    if not frames:
        raise FileNotFoundError("No budget data found.")

    combined = pd.concat(
        frames,
        ignore_index=True,
        sort=False,
    )

    combined["category"] = combined["category"].astype(str).str.strip().str.title()
    combined["budget"] = pd.to_numeric(combined["budget"], errors="coerce")
    combined = combined.dropna(subset=["category", "budget"])

    combined = combined.drop_duplicates(
        subset=["category"],
        keep="last",
    )

    return combined