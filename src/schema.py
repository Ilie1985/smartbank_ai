STANDARD_TRANSACTION_COLUMNS = [
    "date",
    "description",
    "amount",
    "transaction_type",
    "category",
    "account_name",
    "location",
    "payment_method"
]


REQUIRED_TRANSACTION_COLUMNS = [
    "date",
    "description",
    "amount",
    "transaction_type",
    "category"
]


OPTIONAL_TRANSACTION_COLUMNS = [
    "account_name",
    "location",
    "payment_method"
]


STANDARD_BUDGET_COLUMNS = [
    "category",
    "budget"
]