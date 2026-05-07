import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the personal transactions dataset.
    """

    data = df.copy()

    # Standardise column names
    data.columns = (
        data.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Convert date
    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    # Convert amount
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")

    # Remove rows with missing essential values
    data = data.dropna(
        subset=[
            "date",
            "description",
            "amount",
            "transaction_type",
            "category",
            "account_name"
        ]
    )

    # Standardise text fields
    data["description"] = data["description"].astype(str).str.strip().str.title()
    data["transaction_type"] = data["transaction_type"].astype(str).str.strip().str.lower()
    data["category"] = data["category"].astype(str).str.strip().str.title()
    data["account_name"] = data["account_name"].astype(str).str.strip().str.title()

    # Create date columns
    data["month"] = data["date"].dt.to_period("M").astype(str)
    data["year"] = data["date"].dt.year
    data["day"] = data["date"].dt.day

    # Create income and expense columns
    # debit = money going out
    # credit = money coming in
    data["income"] = data.apply(
        lambda row: row["amount"] if row["transaction_type"] == "credit" else 0,
        axis=1
    )

    data["expense"] = data.apply(
        lambda row: row["amount"] if row["transaction_type"] == "debit" else 0,
        axis=1
    )

    data["expense"] = data["expense"].abs()

    return data


def clean_budget(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the budget dataset.
    """

    data = df.copy()

    # Standardise column names
    data.columns = (
        data.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    # Remove duplicates
    data = data.drop_duplicates()

    # Convert budget to numeric
    data["budget"] = pd.to_numeric(data["budget"], errors="coerce")

    # Remove missing values
    data = data.dropna(subset=["category", "budget"])

    # Standardise category names
    data["category"] = data["category"].astype(str).str.strip().str.title()

    return data