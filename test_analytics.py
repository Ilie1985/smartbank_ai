from src.database import load_transactions, load_budget
from src.analytics import (
    calculate_summary,
    spending_by_category,
    monthly_spending,
    monthly_income,
    yearly_summary,
    spending_by_account,
    top_descriptions
)
from src.budget_analysis import compare_budget_to_actual


transactions = load_transactions()
budget = load_budget()

print("Summary:")
print(calculate_summary(transactions))

print("Spending by category:")
print(spending_by_category(transactions).head())

print("Monthly spending:")
print(monthly_spending(transactions).head())

print("Monthly income:")
print(monthly_income(transactions).head())

print("Yearly summary:")
print(yearly_summary(transactions).head())

print("Spending by account:")
print(spending_by_account(transactions).head())

print("Top descriptions:")
print(top_descriptions(transactions).head())

print("Budget comparison:")
print(compare_budget_to_actual(transactions, budget).head())