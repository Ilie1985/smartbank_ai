import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.fraud_detection import detect_unusual_transactions
from src.ui.display import safe_dataframe, get_available_display_columns


def unusual_transactions_page():
    st.header("Unusual Transaction Detection")

    try:
        transactions = load_transactions()

        risk_df = detect_unusual_transactions(transactions)

        suspicious = risk_df[risk_df["risk_status"] == "Suspicious"]

        st.metric("Unusual Transactions Found", len(suspicious))

        risk_columns = get_available_display_columns(
            risk_df,
            extra_columns=["risk_status", "risk_reason"],
        )

        if len(suspicious) > 0:
            st.warning(
                "Some transactions are unusually high compared with normal spending."
            )

            safe_dataframe(suspicious[risk_columns])
        else:
            st.success("No unusual transactions detected.")

        st.subheader("All Transactions with Risk Status")

        safe_dataframe(risk_df[risk_columns])

    except Exception:
        st.warning("Please add or upload transaction data first.")