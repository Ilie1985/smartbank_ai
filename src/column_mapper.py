import pandas as pd
from src.schema import STANDARD_TRANSACTION_COLUMNS


def map_uploaded_columns(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """
    Convert user-uploaded CSV columns into the app's standard column names.

    Example mapping:
    {
        "date": "Transaction Date",
        "description": "Details",
        "amount": "Value",
        "transaction_type": "Type",
        "category": "Category"
    }
    """

    mapped_data = pd.DataFrame()

    for standard_column in STANDARD_TRANSACTION_COLUMNS:
        uploaded_column = column_mapping.get(standard_column)

        if uploaded_column and uploaded_column != "Not Available":
            mapped_data[standard_column] = df[uploaded_column]
        else:
            mapped_data[standard_column] = "Unknown"

    return mapped_data