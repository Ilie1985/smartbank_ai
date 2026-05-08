import pandas as pd

from src.database import load_transactions, load_budget, save_to_database
from src.clean import clean_transactions, clean_budget
from src.blockchain_audit import add_transaction_hashes


def add_manual_transaction(transaction: dict) -> pd.DataFrame:
    """
    Add one manually entered transaction to the existing transactions table.
    """

    new_transaction_df = pd.DataFrame([transaction])

    cleaned_new_transaction = clean_transactions(new_transaction_df)
    cleaned_new_transaction = add_transaction_hashes(cleaned_new_transaction)

    try:
        existing_transactions = load_transactions()
        updated_transactions = pd.concat(
            [existing_transactions, cleaned_new_transaction],
            ignore_index=True
        )
    except Exception:
        updated_transactions = cleaned_new_transaction

    save_to_database(updated_transactions, "transactions")

    return updated_transactions


def add_manual_budget(category: str, budget: float) -> pd.DataFrame:
    """
    Add or update a manually entered budget category.
    """

    new_budget_df = pd.DataFrame(
        [
            {
                "category": category,
                "budget": budget
            }
        ]
    )

    cleaned_new_budget = clean_budget(new_budget_df)

    try:
        existing_budget = load_budget()

        updated_budget = pd.concat(
            [existing_budget, cleaned_new_budget],
            ignore_index=True
        )

        updated_budget = (
            updated_budget.groupby("category")["budget"]
            .sum()
            .reset_index()
        )

    except Exception:
        updated_budget = cleaned_new_budget

    save_to_database(updated_budget, "budget")

    return updated_budget