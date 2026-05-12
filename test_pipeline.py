from src.extract import extract_csv
from src.validate import (
    validate_transaction_columns,
    validate_budget_columns,
    check_empty_data
)
from src.clean import clean_transactions, clean_budget
from src.blockchain_audit import add_transaction_hashes
from src.database import save_to_database, load_transactions, load_budget


transactions_df = extract_csv("data/raw/personal_transactions.csv")
budget_df = extract_csv("data/raw/Budget.csv")


print("Transactions not empty:", check_empty_data(transactions_df))
print("Budget not empty:", check_empty_data(budget_df))

transactions_valid, transaction_missing = validate_transaction_columns(transactions_df)
budget_valid, budget_missing = validate_budget_columns(budget_df)

print("Transactions valid:", transactions_valid)
print("Missing transaction columns:", transaction_missing)

print("Budget valid:", budget_valid)
print("Missing budget columns:", budget_missing)

cleaned_transactions = clean_transactions(transactions_df)
cleaned_transactions = add_transaction_hashes(cleaned_transactions)

cleaned_budget = clean_budget(budget_df)

save_to_database(cleaned_transactions, "transactions")
save_to_database(cleaned_budget, "budget")

loaded_transactions = load_transactions()
loaded_budget = load_budget()

print("Loaded transactions:")
print(loaded_transactions.head())

print("Loaded budget:")
print(loaded_budget.head())