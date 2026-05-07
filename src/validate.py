TRANSACTION_COLUMNS = [
    "Date",
    "Description",
    "Amount",
    "Transaction Type",
    "Category",
    "Account Name"
]


BUDGET_COLUMNS = [
    "Category",
    "Budget"
]


def validate_transaction_columns(df):
    """
    Check if the transaction dataset contains all required columns.
    """

    missing_columns = []

    for column in TRANSACTION_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        return False, missing_columns

    return True, []


def validate_budget_columns(df):
    """
    Check if the budget dataset contains all required columns.
    """

    missing_columns = []

    for column in BUDGET_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        return False, missing_columns

    return True, []


def check_empty_data(df):
    """
    Check if the uploaded dataset is empty.
    """

    return not df.empty