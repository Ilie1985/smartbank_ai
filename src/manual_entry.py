import pandas as pd

from src.clean import clean_transactions
from src.blockchain_audit import add_transaction_hashes
from src.user_database import (
    add_user_transaction,
    add_or_update_user_budget,
)


def add_manual_transaction(transaction: dict) -> pd.DataFrame:
    """
    Clean, hash, and save one manually entered transaction
    into the separate user_inputs.db database.
    """

    new_transaction_df = pd.DataFrame([transaction])

    cleaned_new_transaction = clean_transactions(new_transaction_df)
    cleaned_new_transaction = add_transaction_hashes(cleaned_new_transaction)

    updated_transactions = add_user_transaction(cleaned_new_transaction)

    return updated_transactions


def add_manual_budget(category: str, budget: float) -> pd.DataFrame:
    """
    Save one manually entered budget category into user_inputs.db.
    """

    updated_budget = add_or_update_user_budget(category, budget)

    return updated_budget