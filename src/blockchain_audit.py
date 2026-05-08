import hashlib
import pandas as pd


def create_transaction_hash(row) -> str:
    """
    Create a SHA-256 hash for a transaction row.
    """

    transaction_string = (
        str(row["date"])
        + str(row["description"])
        + str(row["amount"])
        + str(row["transaction_type"])
        + str(row["category"])
        + str(row.get("account_name", "Unknown"))
        + str(row.get("location", "Unknown"))
        + str(row.get("payment_method", "Unknown"))
    )

    return hashlib.sha256(transaction_string.encode()).hexdigest()


def add_transaction_hashes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add blockchain-style hash values to transactions.
    """

    data = df.copy()

    data["transaction_hash"] = data.apply(
        create_transaction_hash,
        axis=1
    )

    return data


def verify_transaction_hash(row) -> bool:
    """
    Verify that the transaction hash still matches the transaction row.
    """

    current_hash = create_transaction_hash(row)

    return current_hash == row["transaction_hash"]