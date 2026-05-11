import plotly.express as px
import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.analytics import yearly_summary, top_descriptions
from src.ui.display import safe_dataframe, get_available_display_columns


def spending_analysis_page():
    st.header("Spending Analysis")

    try:
        transactions = load_transactions()

        categories = ["All"] + sorted(
            transactions["category"].dropna().unique().tolist()
        )

        selected_category = st.selectbox(
            "Filter by category",
            categories,
        )

        filtered_df = transactions.copy()

        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]

        st.subheader("Filtered Transactions")

        safe_dataframe(filtered_df[get_available_display_columns(filtered_df)])

        st.subheader("Top Descriptions by Spending")

        description_df = top_descriptions(filtered_df)

        if description_df.empty:
            st.info("No description spending data available.")
        else:
            fig = px.bar(
                description_df,
                x="description",
                y="expense",
                title="Top Spending Descriptions",
            )

            st.plotly_chart(fig, width="stretch")

        st.subheader("Yearly Summary")

        yearly_df = yearly_summary(filtered_df)

        if yearly_df.empty:
            st.info("No yearly data available.")
        else:
            fig2 = px.bar(
                yearly_df,
                x="year",
                y=["income", "expense"],
                barmode="group",
                title="Yearly Income vs Expense",
            )

            st.plotly_chart(fig2, width="stretch")

    except Exception:
        st.warning("Please add or upload transaction data first.")