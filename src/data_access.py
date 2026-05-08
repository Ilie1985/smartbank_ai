import pandas as pd

from src.database import load_transactions, load_budget
from src.user_database import load_user_transactions, load_user_budget


def load_app_transactions() -> pd.DataFrame:
    """
    Load all transaction data used by the app.

    This combines:
    - uploaded CSV transactions from banking.db
    - manually entered transactions from user_inputs.db
    """

    frames = []

    try:
        uploaded_transactions = load_transactions()

        if not uploaded_transactions.empty:
            frames.append(uploaded_transactions)

    except Exception:
        pass

    try:
        manual_transactions = load_user_transactions()

        if not manual_transactions.empty:
            frames.append(manual_transactions)

    except Exception:
        pass

    if not frames:
        raise FileNotFoundError("No transaction data found.")

    combined = pd.concat(
        frames,
        ignore_index=True,
        sort=False
    )

    return combined


def load_app_budget() -> pd.DataFrame:
    """
    Load all budget data used by the app.

    This combines:
    - uploaded CSV budget from banking.db
    - manually entered budget from user_inputs.db

    If a category appears in both, the manual budget overrides the uploaded budget.
    """

    frames = []

    try:
        uploaded_budget = load_budget()

        if not uploaded_budget.empty:
            frames.append(uploaded_budget)

    except Exception:
        pass

    try:
        manual_budget = load_user_budget()

        if not manual_budget.empty:
            frames.append(manual_budget)

    except Exception:
        pass

    if not frames:
        raise FileNotFoundError("No budget data found.")

    combined = pd.concat(
        frames,
        ignore_index=True,
        sort=False
    )

    combined["category"] = combined["category"].astype(str).str.strip().str.title()
    combined["budget"] = pd.to_numeric(combined["budget"], errors="coerce")
    combined = combined.dropna(subset=["category", "budget"])

    # Manual/user-entered duplicate categories override earlier uploaded ones
    combined = combined.drop_duplicates(
        subset=["category"],
        keep="last"
    )

    return combined