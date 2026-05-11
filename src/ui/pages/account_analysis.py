import plotly.express as px
import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.analytics import spending_by_account
from src.ui.display import safe_dataframe, get_available_display_columns


def account_analysis_page():
    st.header("Account Analysis")

    try:
        transactions = load_transactions()

        if "account_name" not in transactions.columns:
            st.warning("No account name column found.")
            return

        account_df = spending_by_account(transactions)

        st.subheader("Spending by Account")

        if account_df.empty:
            st.info("No account spending data available.")
        else:
            fig = px.bar(
                account_df,
                x="account_name",
                y="expense",
                title="Spending by Account or Card",
            )

            st.plotly_chart(fig, width="stretch")

        accounts = ["All"] + sorted(
            transactions["account_name"].dropna().unique().tolist()
        )

        selected_account = st.selectbox(
            "Filter by account",
            accounts,
        )

        filtered_df = transactions.copy()

        if selected_account != "All":
            filtered_df = filtered_df[filtered_df["account_name"] == selected_account]

        st.subheader("Transactions for Selected Account")
        safe_dataframe(filtered_df[get_available_display_columns(filtered_df)])

    except Exception:
        st.warning("Please add or upload transaction data first.")