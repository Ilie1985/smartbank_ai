import hashlib
import pandas as pd


HASH_COLUMNS = [
    "date",
    "description",
    "amount",
    "transaction_type",
    "category",
    "account_name",
    "location",
    "payment_method",
]


def normalise_hash_value(column_name: str, value) -> str:
    """
    Convert values into a consistent text format before hashing.

    This is important because values like dates and amounts can look different
    after being saved and loaded from SQLite.
    """

    if pd.isna(value):
        return "Unknown"

    if column_name == "date":
        date_value = pd.to_datetime(value, errors="coerce")

        if pd.isna(date_value):
            return "Unknown"

        return date_value.strftime("%Y-%m-%d")

    if column_name == "amount":
        try:
            return f"{float(value):.2f}"
        except Exception:
            return "0.00"

    return str(value).strip().title()


def create_transaction_hash(row) -> str:
    """
    Create a SHA-256 hash for a transaction.

    Only stable transaction fields are used.
    Fields such as transaction_hash, hash_valid, manual_id, and data_source
    are not used because they can change after the transaction is saved.
    """

    values = []

    for column in HASH_COLUMNS:
        value = row[column] if column in row.index else "Unknown"
        normalised_value = normalise_hash_value(column, value)
        values.append(normalised_value)

    transaction_string = "|".join(values)

    return hashlib.sha256(transaction_string.encode("utf-8")).hexdigest()


def add_transaction_hashes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add SHA-256 hashes to transactions.
    """

    data = df.copy()

    data["transaction_hash"] = data.apply(
        create_transaction_hash,
        axis=1,
    )

    return data


def verify_transaction_hash(row) -> bool:
    """
    Check whether the saved transaction hash still matches the transaction data.
    """

    if "transaction_hash" not in row.index:
        return False

    saved_hash = str(row["transaction_hash"]).strip()
    current_hash = create_transaction_hash(row)

    return saved_hash == current_hash


def refresh_transaction_hashes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recalculate hashes for all transactions.

    Use this when the hash logic has changed and existing hashes need to be updated.
    """

    data = df.copy()

    data["transaction_hash"] = data.apply(
        create_transaction_hash,
        axis=1,
    )

    return data