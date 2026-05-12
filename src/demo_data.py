import random

import pandas as pd

from src.clean import clean_transactions, clean_budget
from src.blockchain_audit import add_transaction_hashes
from src.database import save_to_database


def create_demo_transactions() -> pd.DataFrame:
    """
    Create 12 months of demo transaction data.
    """

    random.seed(42)

    year = 2025
    rows = []

    def add(
        date,
        description,
        amount,
        transaction_type,
        category,
        account_name,
        location,
        payment_method,
    ):
        rows.append(
            {
                "Date": pd.to_datetime(date).strftime("%m/%d/%Y"),
                "Description": description,
                "Amount": round(float(amount), 2),
                "Transaction Type": transaction_type,
                "Category": category,
                "Account Name": account_name,
                "Location": location,
                "Payment Method": payment_method,
            }
        )

    for month in range(1, 13):
        add(
            f"{year}-{month:02d}-01",
            "Salary Payment",
            2300 + random.randint(-50, 80),
            "credit",
            "Salary",
            "Checking",
            "London",
            "Bank Transfer",
        )

        add(
            f"{year}-{month:02d}-02",
            "Mortgage Payment",
            950,
            "debit",
            "Mortgage & Rent",
            "Checking",
            "London",
            "Direct Debit",
        )

        add(
            f"{year}-{month:02d}-04",
            "Gas Company",
            55 + random.randint(-10, 15),
            "debit",
            "Utilities",
            "Checking",
            "London",
            "Direct Debit",
        )

        add(
            f"{year}-{month:02d}-05",
            "Electric Company",
            70 + random.randint(-15, 20),
            "debit",
            "Utilities",
            "Checking",
            "London",
            "Direct Debit",
        )

        add(
            f"{year}-{month:02d}-06",
            "Internet Provider",
            45,
            "debit",
            "Internet",
            "Checking",
            "Online",
            "Direct Debit",
        )

        add(
            f"{year}-{month:02d}-07",
            "Phone Company",
            38 + random.randint(-4, 6),
            "debit",
            "Mobile Phone",
            "Checking",
            "Online",
            "Direct Debit",
        )

        for day in [5, 12, 19, 26]:
            add(
                f"{year}-{month:02d}-{day:02d}",
                "Grocery Store",
                65 + random.randint(-15, 30),
                "debit",
                "Groceries",
                "Platinum Card",
                "London",
                "Debit Card",
            )

        for day in [11, 23]:
            add(
                f"{year}-{month:02d}-{day:02d}",
                random.choice(["Thai Restaurant", "Italian Restaurant", "American Tavern"]),
                28 + random.randint(-8, 25),
                "debit",
                "Restaurants",
                "Silver Card",
                "London",
                "Credit Card",
            )

        add(
            f"{year}-{month:02d}-16",
            "Amazon",
            40 + random.randint(0, 120),
            "debit",
            "Shopping",
            "Platinum Card",
            "Online",
            "Credit Card",
        )

        add(
            f"{year}-{month:02d}-24",
            "Cinema",
            18 + random.randint(0, 20),
            "debit",
            "Entertainment",
            "Platinum Card",
            "London",
            "Credit Card",
        )

        if month in [4, 8, 12]:
            add(
                f"{year}-{month:02d}-25",
                "Weekend Travel Booking",
                260 + random.randint(0, 180),
                "debit",
                "Travel",
                "Platinum Card",
                "Online",
                "Credit Card",
            )

    return pd.DataFrame(rows)


def create_demo_budget() -> pd.DataFrame:
    """
    Create demo budget data.
    """

    data = [
        ("Entertainment", 80),
        ("Gas & Fuel", 120),
        ("Groceries", 350),
        ("Internet", 50),
        ("Mobile Phone", 45),
        ("Mortgage & Rent", 950),
        ("Restaurants", 120),
        ("Shopping", 180),
        ("Travel", 150),
        ("Utilities", 160),
    ]

    return pd.DataFrame(data, columns=["Category", "Budget"])


def load_demo_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean and save demo data into uploaded transaction and budget databases.
    """

    transactions = create_demo_transactions()
    budget = create_demo_budget()

    cleaned_transactions = clean_transactions(transactions)
    cleaned_transactions = add_transaction_hashes(cleaned_transactions)

    cleaned_budget = clean_budget(budget)

    save_to_database(cleaned_transactions, "transactions")
    save_to_database(cleaned_budget, "budget")

    return cleaned_transactions, cleaned_budget