import pandas as pd


def compare_budget_to_actual(transactions_df: pd.DataFrame, budget_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare actual spending by category against planned budget.
    """

    expenses = transactions_df[transactions_df["transaction_type"] == "debit"]

    actual_spending = (
        expenses.groupby("category")["expense"]
        .sum()
        .reset_index()
        .rename(columns={"expense": "actual_spending"})
    )

    comparison = pd.merge(
        budget_df,
        actual_spending,
        on="category",
        how="left"
    )

    comparison["actual_spending"] = comparison["actual_spending"].fillna(0)

    comparison["remaining_budget"] = comparison["budget"] - comparison["actual_spending"]

    comparison["percentage_used"] = comparison.apply(
        lambda row: (row["actual_spending"] / row["budget"]) * 100 if row["budget"] > 0 else 0,
        axis=1
    )

    comparison["budget_status"] = comparison.apply(
        assign_budget_status,
        axis=1
    )

    return comparison.sort_values(by="percentage_used", ascending=False)


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