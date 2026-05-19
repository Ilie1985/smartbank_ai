import pandas as pd

CATEGORY_RULES = {
    "Groceries": [
        "tesco",
        "sainsbury",
        "asda",
        "aldi",
        "lidl",
        "morrisons",
        "waitrose",
        "grocery",
        "groceries",
        "supermarket",
    ],
    "Restaurants": [
        "restaurant",
        "nando",
        "mcdonald",
        "kfc",
        "burger",
        "pizza",
        "cafe",
        "pret",
        "subway",
    ],
    "Coffee Shops": [
        "starbucks",
        "costa",
        "coffee",
        "nero",
    ],
    "Transport": [
        "uber",
        "bolt",
        "taxi",
        "train",
        "rail",
        "tfl",
        "bus",
        "transport",
        "travel",
    ],
    "Gas & Fuel": [
        "shell",
        "bp",
        "esso",
        "fuel",
        "petrol",
    ],
    "Shopping": [
        "amazon",
        "ebay",
        "argos",
        "shopping",
        "primark",
        "zara",
        "hm",
    ],
    "Entertainment": [
        "netflix",
        "spotify",
        "cinema",
        "odeon",
        "disney",
        "prime video",
    ],
    "Utilities": [
        "electric",
        "gas company",
        "water",
        "utility",
        "energy",
        "british gas",
        "edf",
    ],
    "Internet": [
        "internet",
        "broadband",
        "wifi",
        "virgin media",
        "bt",
        "sky",
    ],
    "Mobile Phone": [
        "vodafone",
        "ee",
        "o2",
        "three",
        "mobile",
        "phone",
    ],
    "Mortgage & Rent": [
        "rent",
        "mortgage",
        "landlord",
    ],
    "Income": [
        "salary",
        "payroll",
        "wages",
        "income",
        "faster payment in",
        "payment in",
    ],
}


def clean_money_value(value) -> float:
    """
    Convert money values such as '£2,300.00', '"£45.20"', blanks,
    or quoted values into floats.
    Empty values become 0.
    """

    if pd.isna(value):
        return 0.0

    value_as_text = str(value).strip()

    value_as_text = value_as_text.replace("£", "")
    value_as_text = value_as_text.replace(",", "")
    value_as_text = value_as_text.replace('"', "")
    value_as_text = value_as_text.replace("'", "")
    value_as_text = value_as_text.strip()

    if value_as_text == "":
        return 0.0

    try:
        return float(value_as_text)
    except Exception:
        return 0.0


def get_mapped_value(row, column_mapping, target_column, default_value=None):
    """
    Safely get a value from a mapped uploaded CSV column.
    """

    source_column = column_mapping.get(target_column)

    if source_column is None or source_column == "Not Available":
        return default_value

    if source_column not in row.index:
        return default_value

    value = row[source_column]

    if pd.isna(value):
        return default_value

    return value


def build_description(row, column_mapping) -> str:
    """
    Build a useful description.

    Some bank statements have one description column.
    Others have Payer / Payee and Reference columns.
    """

    description = get_mapped_value(
        row,
        column_mapping,
        "description",
        None,
    )

    payer_payee = get_mapped_value(
        row,
        column_mapping,
        "payer_payee",
        None,
    )

    reference = get_mapped_value(
        row,
        column_mapping,
        "reference",
        None,
    )

    description_parts = []

    if description not in [None, ""]:
        description_parts.append(str(description).strip())

    if payer_payee not in [None, ""]:
        description_parts.append(str(payer_payee).strip())

    if reference not in [None, ""]:
        description_parts.append(str(reference).strip())

    if not description_parts:
        return "Unknown Transaction"

    # Remove duplicate text while keeping order.
    unique_parts = []
    for part in description_parts:
        if part not in unique_parts:
            unique_parts.append(part)

    return " - ".join(unique_parts)


def infer_transaction_from_money_columns(money_in, money_out):
    """
    Infer transaction type and amount from Money In / Money Out columns.
    """

    money_in_value = clean_money_value(money_in)
    money_out_value = clean_money_value(money_out)

    if money_in_value > 0:
        return "credit", abs(money_in_value)

    if money_out_value > 0:
        return "debit", abs(money_out_value)

    return "debit", 0.0


def infer_transaction_from_single_amount(amount):
    """
    Infer transaction type and amount from a single amount column.
    Negative amount means debit.
    Positive amount means credit.
    """

    amount_value = clean_money_value(amount)

    if amount_value < 0:
        return "debit", abs(amount_value)

    return "credit", abs(amount_value)


def normalise_transaction_type(value, amount=None) -> str:
    """
    Standardise transaction type to debit or credit.
    """

    if value is None:
        if amount is None:
            return "debit"

        inferred_type, _ = infer_transaction_from_single_amount(amount)
        return inferred_type

    text = str(value).lower().strip()

    credit_keywords = [
        "credit",
        "income",
        "money in",
        "payment in",
        "faster payment in",
        "deposit",
        "salary",
    ]

    debit_keywords = [
        "debit",
        "expense",
        "money out",
        "payment out",
        "faster payment out",
        "card payment",
        "direct debit",
        "withdrawal",
    ]

    for keyword in credit_keywords:
        if keyword in text:
            return "credit"

    for keyword in debit_keywords:
        if keyword in text:
            return "debit"

    if amount is not None:
        inferred_type, _ = infer_transaction_from_single_amount(amount)
        return inferred_type

    return "debit"


def infer_category(description: str, transaction_type: str) -> str:
    """
    Guess category from transaction description.
    """

    if transaction_type == "credit":
        return "Income"

    description_lower = str(description).lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category

    return "Other"


def map_uploaded_columns(raw_df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """
    Convert an uploaded bank CSV into the SmartBank AI transaction schema.

    Supports two common formats:

    1. Single amount column:
       Date, Description, Amount

    2. Bank statement columns:
       Booking Date, Payer / Payee, Reference, Money In, Money Out, Balance
    """

    mapped_rows = []

    for _, row in raw_df.iterrows():
        date = get_mapped_value(
            row,
            column_mapping,
            "date",
            None,
        )

        if date is not None:
            date = str(date).replace('"', "").replace("'", "").strip()

        description = build_description(row, column_mapping)

        money_in = get_mapped_value(
            row,
            column_mapping,
            "money_in",
            None,
        )

        money_out = get_mapped_value(
            row,
            column_mapping,
            "money_out",
            None,
        )

        amount_value = get_mapped_value(
            row,
            column_mapping,
            "amount",
            None,
        )

        # Prefer Money In / Money Out if either is mapped.
        if money_in is not None or money_out is not None:
            transaction_type, amount = infer_transaction_from_money_columns(
                money_in,
                money_out,
            )
        else:
            transaction_type, amount = infer_transaction_from_single_amount(
                amount_value,
            )

        mapped_transaction_type = get_mapped_value(
            row,
            column_mapping,
            "transaction_type",
            None,
        )

        if mapped_transaction_type is not None:
            transaction_type = normalise_transaction_type(
                mapped_transaction_type,
                amount=amount_value,
            )

        category = get_mapped_value(
            row,
            column_mapping,
            "category",
            None,
        )

        if category is None or str(category).strip() == "":
            category = infer_category(description, transaction_type)

        payment_method = get_mapped_value(
            row,
            column_mapping,
            "payment_method",
            None,
        )

        if payment_method is None:
            payment_method = get_mapped_value(
                row,
                column_mapping,
                "transaction_method",
                "Bank Transfer",
            )

        balance = get_mapped_value(
            row,
            column_mapping,
            "balance",
            None,
        )

        mapped_rows.append(
            {
                "Date": date,
                "Description": description,
                "Amount": amount,
                "Transaction Type": transaction_type,
                "Category": category,
                "Account Name": get_mapped_value(
                    row,
                    column_mapping,
                    "account_name",
                    "Uploaded Bank Account",
                ),
                "Location": get_mapped_value(
                    row,
                    column_mapping,
                    "location",
                    "Unknown",
                ),
                "Payment Method": payment_method,
                "Balance": clean_money_value(balance) if balance is not None else None,
            }
        )

    return pd.DataFrame(mapped_rows)
