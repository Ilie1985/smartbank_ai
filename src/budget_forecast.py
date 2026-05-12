import calendar
from datetime import datetime

import pandas as pd


def get_selected_month_details(selected_month: str | None = None):
    """
    Return useful month information for budget forecasting.
    """

    today = datetime.today()

    if selected_month is None or selected_month == "Current Month":
        year = today.year
        month = today.month
    else:
        year, month = selected_month.split("-")
        year = int(year)
        month = int(month)

    days_in_month = calendar.monthrange(year, month)[1]

    if year == today.year and month == today.month:
        days_passed = today.day
    else:
        days_passed = days_in_month

    days_left = max(days_in_month - days_passed, 0)

    month_label = f"{year}-{month:02d}"

    return {
        "month": month_label,
        "days_in_month": days_in_month,
        "days_passed": days_passed,
        "days_left": days_left,
    }


def prepare_transactions(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare transaction data for budget forecasting.
    """

    transactions = transactions_df.copy()

    transactions["date"] = pd.to_datetime(transactions["date"], errors="coerce")
    transactions["month"] = transactions["date"].dt.to_period("M").astype(str)

    transactions["amount"] = pd.to_numeric(
        transactions["amount"],
        errors="coerce"
    ).fillna(0)

    transactions["category"] = (
        transactions["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    transactions["transaction_type"] = (
        transactions["transaction_type"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    transactions["expense"] = transactions.apply(
        lambda row: abs(row["amount"])
        if row["transaction_type"] == "debit"
        else 0,
        axis=1,
    )

    return transactions


def prepare_budget(budget_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare budget data for budget forecasting.
    """

    budget = budget_df.copy()

    budget["category"] = (
        budget["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    budget["budget"] = pd.to_numeric(
        budget["budget"],
        errors="coerce"
    ).fillna(0)

    return budget


def calculate_budget_forecast(
    transactions_df: pd.DataFrame,
    budget_df: pd.DataFrame,
    selected_month: str | None = None,
) -> tuple[pd.DataFrame, dict]:
    """
    Calculate budget usage, remaining budget, daily/weekly allowance,
    and projected month-end spending.
    """

    month_info = get_selected_month_details(selected_month)

    transactions = prepare_transactions(transactions_df)
    budget = prepare_budget(budget_df)

    month_transactions = transactions[
        transactions["month"] == month_info["month"]
    ]

    actual_spending = (
        month_transactions[month_transactions["transaction_type"] == "debit"]
        .groupby("category")["expense"]
        .sum()
        .reset_index()
        .rename(columns={"expense": "actual_spending"})
    )

    comparison = pd.merge(
        budget,
        actual_spending,
        on="category",
        how="left",
    )

    comparison["actual_spending"] = comparison["actual_spending"].fillna(0)

    comparison["remaining_budget"] = (
        comparison["budget"] - comparison["actual_spending"]
    )

    comparison["percentage_used"] = comparison.apply(
        lambda row: (row["actual_spending"] / row["budget"]) * 100
        if row["budget"] > 0 else 0,
        axis=1,
    )

    days_passed = max(month_info["days_passed"], 1)
    days_in_month = month_info["days_in_month"]
    days_left = month_info["days_left"]

    comparison["projected_month_end_spending"] = (
        comparison["actual_spending"] / days_passed
    ) * days_in_month

    comparison["projected_remaining"] = (
        comparison["budget"] - comparison["projected_month_end_spending"]
    )

    comparison["daily_remaining_allowance"] = comparison.apply(
        lambda row: row["remaining_budget"] / days_left
        if days_left > 0 else row["remaining_budget"],
        axis=1,
    )

    comparison["weekly_remaining_allowance"] = (
        comparison["daily_remaining_allowance"] * 7
    )

    comparison["budget_status"] = comparison.apply(
        assign_budget_status,
        axis=1,
    )

    comparison["pace_status"] = comparison.apply(
        assign_pace_status,
        axis=1,
    )

    comparison = comparison.sort_values(
        by="percentage_used",
        ascending=False,
    )

    summary = calculate_budget_summary(comparison, month_info)

    return comparison, summary


def assign_budget_status(row):
    """
    Assign current budget status.
    """

    if row["budget"] == 0 and row["actual_spending"] > 0:
        return "No Budget Set"

    if row["actual_spending"] > row["budget"]:
        return "Over Budget"

    if row["percentage_used"] >= 80:
        return "Close to Limit"

    return "Within Budget"


def assign_pace_status(row):
    """
    Assign projected spending pace status.
    """

    if row["budget"] == 0 and row["actual_spending"] > 0:
        return "No Budget Set"

    if row["projected_month_end_spending"] > row["budget"]:
        return "At Risk"

    if row["percentage_used"] >= 80:
        return "Watch Closely"

    return "On Track"


def calculate_budget_summary(comparison: pd.DataFrame, month_info: dict) -> dict:
    """
    Calculate summary metrics for the budget tracker.
    """

    total_budget = comparison["budget"].sum()
    total_spent = comparison["actual_spending"].sum()
    total_remaining = total_budget - total_spent

    total_projected = comparison["projected_month_end_spending"].sum()
    projected_remaining = total_budget - total_projected

    days_left = month_info["days_left"]

    if days_left > 0:
        daily_allowance = total_remaining / days_left
    else:
        daily_allowance = total_remaining

    weekly_allowance = daily_allowance * 7

    over_budget_count = len(
        comparison[comparison["budget_status"] == "Over Budget"]
    )

    at_risk_count = len(
        comparison[comparison["pace_status"] == "At Risk"]
    )

    health_score = calculate_budget_health_score(
        total_budget=total_budget,
        total_spent=total_spent,
        total_projected=total_projected,
        over_budget_count=over_budget_count,
        at_risk_count=at_risk_count,
    )

    return {
        "month": month_info["month"],
        "days_in_month": month_info["days_in_month"],
        "days_passed": month_info["days_passed"],
        "days_left": month_info["days_left"],
        "total_budget": total_budget,
        "total_spent": total_spent,
        "total_remaining": total_remaining,
        "total_projected": total_projected,
        "projected_remaining": projected_remaining,
        "daily_allowance": daily_allowance,
        "weekly_allowance": weekly_allowance,
        "over_budget_count": over_budget_count,
        "at_risk_count": at_risk_count,
        "health_score": health_score,
    }


def calculate_budget_health_score(
    total_budget: float,
    total_spent: float,
    total_projected: float,
    over_budget_count: int,
    at_risk_count: int,
) -> int:
    """
    Calculate a simple budget health score from 0 to 100.
    """

    if total_budget <= 0:
        return 0

    score = 100

    percentage_used = (total_spent / total_budget) * 100
    projected_percentage = (total_projected / total_budget) * 100

    if percentage_used > 100:
        score -= 35
    elif percentage_used > 80:
        score -= 20
    elif percentage_used > 60:
        score -= 10

    if projected_percentage > 100:
        score -= 25
    elif projected_percentage > 90:
        score -= 15

    score -= over_budget_count * 5
    score -= at_risk_count * 3

    return max(0, min(100, int(score)))