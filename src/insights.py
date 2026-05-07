import pandas as pd
from src.budget_analysis import compare_budget_to_actual


def generate_financial_insights(transactions_df: pd.DataFrame, budget_df: pd.DataFrame) -> list:
    """
    Generate AI-style personalised financial insights.
    """

    insights = []

    total_income = transactions_df["income"].sum()
    total_expense = transactions_df["expense"].sum()

    if total_income > total_expense:
        insights.append(
            f"Your total income is higher than your spending. Estimated savings are £{total_income - total_expense:,.2f}."
        )
    else:
        insights.append(
            f"Your spending is higher than your income by £{total_expense - total_income:,.2f}. You may need to review your budget."
        )

    category_spending = (
        transactions_df[transactions_df["transaction_type"] == "debit"]
        .groupby("category")["expense"]
        .sum()
        .sort_values(ascending=False)
    )

    if not category_spending.empty:
        top_category = category_spending.index[0]
        top_amount = category_spending.iloc[0]

        insights.append(
            f"Your highest spending category is {top_category}, with £{top_amount:,.2f} spent."
        )

    monthly = (
        transactions_df.groupby("month")["expense"]
        .sum()
        .reset_index()
        .sort_values(by="month")
    )

    if len(monthly) >= 2:
        previous_month = monthly.iloc[-2]["expense"]
        current_month = monthly.iloc[-1]["expense"]
        difference = current_month - previous_month

        if difference > 0:
            insights.append(
                f"Your spending increased by £{difference:,.2f} compared with the previous month."
            )
        elif difference < 0:
            insights.append(
                f"Your spending decreased by £{abs(difference):,.2f} compared with the previous month."
            )
        else:
            insights.append(
                "Your spending stayed the same compared with the previous month."
            )

    budget_comparison = compare_budget_to_actual(transactions_df, budget_df)

    over_budget = budget_comparison[budget_comparison["budget_status"] == "Over Budget"]

    if len(over_budget) > 0:
        worst_category = over_budget.iloc[0]["category"]
        overspend = abs(over_budget.iloc[0]["remaining_budget"])

        insights.append(
            f"You are over budget in {worst_category} by £{overspend:,.2f}."
        )
    else:
        insights.append(
            "You are currently within budget across your planned categories."
        )

    return insights