import pandas as pd


def calculate_summary(df: pd.DataFrame) -> dict:
    """
    Calculate total income, expenses, savings, and transaction count.
    """

    total_income = df["income"].sum()
    total_expenses = df["expense"].sum()
    net_savings = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "transaction_count": len(df)
    }


def spending_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total expense by category.
    """

    expenses = df[df["transaction_type"] == "debit"]

    result = (
        expenses.groupby("category")["expense"]
        .sum()
        .reset_index()
        .sort_values(by="expense", ascending=False)
    )

    return result


def monthly_spending(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total monthly spending.
    """

    result = (
        df.groupby("month")["expense"]
        .sum()
        .reset_index()
        .sort_values(by="month")
    )

    return result


def monthly_income(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total monthly income.
    """

    result = (
        df.groupby("month")["income"]
        .sum()
        .reset_index()
        .sort_values(by="month")
    )

    return result


def yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate yearly income, expense, and savings.
    """

    result = (
        df.groupby("year")[["income", "expense"]]
        .sum()
        .reset_index()
        .sort_values(by="year")
    )

    result["savings"] = result["income"] - result["expense"]

    return result


def spending_by_account(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate spending by account or card.
    """

    expenses = df[df["transaction_type"] == "debit"]

    result = (
        expenses.groupby("account_name")["expense"]
        .sum()
        .reset_index()
        .sort_values(by="expense", ascending=False)
    )

    return result


def top_descriptions(df: pd.DataFrame, limit: int = 20) -> pd.DataFrame:
    """
    Calculate top transaction descriptions by spending.
    """

    expenses = df[df["transaction_type"] == "debit"]

    result = (
        expenses.groupby("description")["expense"]
        .sum()
        .reset_index()
        .sort_values(by="expense", ascending=False)
        .head(limit)
    )

    return result