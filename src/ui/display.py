import pandas as pd
import streamlit as st


TRANSACTION_DISPLAY_COLUMNS = [
    "date",
    "description",
    "amount",
    "transaction_type",
    "category",
    "account_name",
    "location",
    "payment_method",
    "data_source",
    "manual_id",
]


def prepare_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare dataframe safely before showing it in Streamlit.

    This prevents pyarrow errors caused by mixed date/object types.
    """

    data = df.copy()

    for column in data.columns:
        if column == "date":
            data[column] = pd.to_datetime(data[column], errors="coerce")
            data[column] = data[column].dt.strftime("%Y-%m-%d")

        elif pd.api.types.is_datetime64_any_dtype(data[column]):
            data[column] = data[column].dt.strftime("%Y-%m-%d")

        elif data[column].dtype == "object":
            data[column] = data[column].apply(
                lambda value: str(value) if value is not None else ""
            )

    return data


def safe_dataframe(df: pd.DataFrame, *args, **kwargs):
    """
    Display a dataframe safely in Streamlit.
    """

    safe_df = prepare_for_display(df)
    st.dataframe(safe_df, *args, **kwargs)


def get_available_display_columns(df, extra_columns=None):
    """
    Return only the columns that exist in the dataframe.
    This prevents errors if optional columns are missing.
    """

    columns = TRANSACTION_DISPLAY_COLUMNS.copy()

    if extra_columns:
        columns.extend(extra_columns)

    return [column for column in columns if column in df.columns]