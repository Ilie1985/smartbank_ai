import pandas as pd


def compare_budget_to_actual(
    transactions_df: pd.DataFrame,
    budget_df: pd.DataFrame,
    selected_month: str | None = None
) -> pd.DataFrame:
    """
    Compare actual spending against budget.

    If selected_month is provided, only spending from that month is used.
    Example selected_month: '2026-05'
    """

    transactions = transactions_df.copy()
    budget = budget_df.copy()

    # Standardise categories so matching works better
    transactions["category"] = transactions["category"].astype(str).str.strip().str.title()
    budget["category"] = budget["category"].astype(str).str.strip().str.title()

    # Convert numeric values safely
    transactions["expense"] = pd.to_numeric(transactions["expense"], errors="coerce").fillna(0)
    budget["budget"] = pd.to_numeric(budget["budget"], errors="coerce").fillna(0)

    # Filter by month if selected
    if selected_month is not None and selected_month != "All":
        transactions = transactions[transactions["month"] == selected_month]

    # Only debit transactions count as spending
    expenses = transactions[transactions["transaction_type"] == "debit"]

    actual_spending = (
        expenses.groupby("category")["expense"]
        .sum()
        .reset_index()
        .rename(columns={"expense": "actual_spending"})
    )

    comparison = pd.merge(
        budget,
        actual_spending,
        on="category",
        how="left"
    )

    comparison["actual_spending"] = comparison["actual_spending"].fillna(0)

    comparison["remaining_budget"] = comparison["budget"] - comparison["actual_spending"]

    comparison["percentage_used"] = comparison.apply(
        lambda row: (row["actual_spending"] / row["budget"]) * 100
        if row["budget"] > 0 else 0,
        axis=1
    )

    comparison["budget_status"] = comparison.apply(
        assign_budget_status,
        axis=1
    )

    comparison = comparison.sort_values(
        by="percentage_used",
        ascending=False
    )

    return comparison


def assign_budget_status(row):
    """
    Assign a budget status based on actual spending.
    """

    if row["budget"] == 0 and row["actual_spending"] > 0:
        return "No Budget Set"

    if row["actual_spending"] > row["budget"]:
        return "Over Budget"

    if row["percentage_used"] >= 80:
        return "Close to Limit"

    return "Within Budget"