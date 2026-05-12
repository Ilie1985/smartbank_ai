import sqlite3
import pandas as pd


DATABASES = {
    "uploaded_transactions": {
        "path": "database/uploaded_transactions.db",
        "table": "transactions",
    },
    "uploaded_budget": {
        "path": "database/uploaded_budget.db",
        "table": "budget",
    },
    "manual_transactions": {
        "path": "database/manual_transactions.db",
        "table": "manual_transactions",
    },
    "manual_budget": {
        "path": "database/manual_budget.db",
        "table": "manual_budget",
    },
}


for name, config in DATABASES.items():
    print(f"\nChecking {name}")
    print("-" * 50)

    try:
        conn = sqlite3.connect(config["path"])

        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            conn,
        )

        print("Tables:")
        print(tables)

        df = pd.read_sql_query(
            f"SELECT * FROM {config['table']};",
            conn,
        )

        print(f"\nData from {config['table']}:")
        print(df.head(20))
        print(f"\nRows: {len(df)}")

        conn.close()

    except Exception as error:
        print(f"Could not read {name}: {error}")