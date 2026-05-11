import streamlit as st

from src.ui.styles import load_css

from src.ui.pages.data_input import data_input_page
from src.ui.pages.data_quality import data_quality_page
from src.ui.pages.dashboard import dashboard_page
from src.ui.pages.budget_tracker import budget_tracker_page
from src.ui.pages.account_analysis import account_analysis_page
from src.ui.pages.spending_analysis import spending_analysis_page
from src.ui.pages.prediction import prediction_page
from src.ui.pages.unusual_transactions import unusual_transactions_page
from src.ui.pages.blockchain_audit import blockchain_audit_page
from src.ui.pages.ai_insights import ai_insights_page
from src.ui.pages.about import about_page


st.set_page_config(
    page_title="SmartBank AI",
    page_icon="🏦",
    layout="wide",
)


PAGES = {
    "Data Input": data_input_page,
    "Data Quality": data_quality_page,
    "Dashboard": dashboard_page,
    "Budget Tracker": budget_tracker_page,
    "Account Analysis": account_analysis_page,
    "Spending Analysis": spending_analysis_page,
    "Prediction": prediction_page,
    "Unusual Transactions": unusual_transactions_page,
    "Blockchain Audit": blockchain_audit_page,
    "AI Insights": ai_insights_page,
    "About": about_page,
}


def render_header():
    st.markdown(
        """
        <div class="smartbank-hero">
            <div class="smartbank-title">🏦 SmartBank AI</div>
            <div class="smartbank-subtitle">
                Personal Finance and Budget Intelligence App
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    load_css()
    render_header()

    selected_page = st.sidebar.radio(
        "Navigation",
        list(PAGES.keys()),
    )

    page_function = PAGES[selected_page]
    page_function()


if __name__ == "__main__":
    main()