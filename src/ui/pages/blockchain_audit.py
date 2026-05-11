import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.blockchain_audit import verify_transaction_hash
from src.ui.display import safe_dataframe, get_available_display_columns


def blockchain_audit_page():
    st.header("Blockchain-Style Transaction Audit")

    try:
        transactions = load_transactions()

        st.write(
            "This page uses SHA-256 hashing to create a tamper-evident record for each transaction."
        )

        if "transaction_hash" not in transactions.columns:
            st.error(
                "No transaction hash found. Please upload or add transactions again."
            )
            return

        transactions["hash_valid"] = transactions.apply(
            verify_transaction_hash,
            axis=1,
        )

        valid_count = transactions["hash_valid"].sum()
        invalid_count = len(transactions) - valid_count

        col1, col2 = st.columns(2)

        col1.metric("Valid Hashes", valid_count)
        col2.metric("Invalid Hashes", invalid_count)

        audit_columns = get_available_display_columns(
            transactions,
            extra_columns=["transaction_hash", "hash_valid"],
        )

        safe_dataframe(transactions[audit_columns])

    except Exception:
        st.warning("Please add or upload transaction data first.")