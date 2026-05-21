import streamlit as st

from src.ui.styles import load_css

from src.ui.pages.home import home_page
from src.ui.pages.quick_add_expense import quick_add_expense_page
from src.ui.pages.budget_setup import budget_setup_page
from src.ui.pages.upload_data import upload_data_menu_page
from src.ui.pages.dashboard import dashboard_page
from src.ui.pages.budget_tracker import budget_tracker_page
from src.ui.pages.spending_analysis import spending_analysis_page
from src.ui.pages.prediction import prediction_page
from src.ui.pages.blockchain_audit import blockchain_audit_page
from src.ui.pages.ai_insights import ai_insights_page
from src.ui.pages.about import about_page

st.set_page_config(
    page_title="SmartBank AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


PAGES = {
    "Home": home_page,
    "Quick Add Expense": quick_add_expense_page,
    "Budget Setup": budget_setup_page,
    "Upload Data": upload_data_menu_page,
    "Dashboard": dashboard_page,
    "Budget Tracker": budget_tracker_page,
    "Spending Analysis": spending_analysis_page,
    "AI Spending Forecast": prediction_page,
    "Security Audit": blockchain_audit_page,
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

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Home"

    query_page = st.query_params.get("page")

    if query_page in PAGES:
        st.session_state["selected_page"] = query_page
        st.query_params.clear()

    if "data_source_mode" not in st.session_state:
        st.session_state["data_source_mode"] = "All data"

    st.sidebar.markdown("### Data Source")

    data_source_mode = st.sidebar.selectbox(
        "Use data from",
        [
            "All data",
            "Manual data only",
            "Uploaded CSV data only",
        ],
        index=[
            "All data",
            "Manual data only",
            "Uploaded CSV data only",
        ].index(st.session_state["data_source_mode"]),
    )

    st.session_state["data_source_mode"] = data_source_mode

    st.sidebar.caption("Choose which data source the app should use.")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")

    selected_page = st.sidebar.radio(
        "Navigation menu",
        list(PAGES.keys()),
        index=list(PAGES.keys()).index(st.session_state["selected_page"]),
        label_visibility="collapsed",
    )

    st.session_state["selected_page"] = selected_page

    st.sidebar.markdown("---")
    st.sidebar.caption("SmartBank AI")

    page_function = PAGES[selected_page]
    page_function()


if __name__ == "__main__":
    main()
