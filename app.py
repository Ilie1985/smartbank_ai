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

    data_source_options = [
        "All data",
        "Manual data only",
        "Uploaded CSV data only",
    ]

    data_source_labels = {
        "All data": "Best available data",
        "Manual data only": "Manual data only",
        "Uploaded CSV data only": "Uploaded CSV data only",
    }

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Home"

    if "data_source_mode" not in st.session_state:
        st.session_state["data_source_mode"] = "All data"

    query_page = st.query_params.get("page")
    query_data_source = st.query_params.get("data_source")

    if query_data_source in data_source_options:
        st.session_state["data_source_mode"] = query_data_source

    if query_page in PAGES:
        st.session_state["selected_page"] = query_page

    if query_page or query_data_source:
        st.query_params.clear()

    current_mode = st.session_state.get("data_source_mode", "All data")

    if current_mode not in data_source_options:
        current_mode = "All data"

    st.sidebar.markdown("### Data Source")

    data_source_mode = st.sidebar.selectbox(
        "Use data from",
        data_source_options,
        index=data_source_options.index(current_mode),
        format_func=lambda option: data_source_labels.get(option, option),
    )

    st.session_state["data_source_mode"] = data_source_mode

    if st.session_state["selected_page"] == "AI Spending Forecast":
        st.sidebar.caption(
            "Best available data uses uploaded CSV data for ML and only adds "
            "manual data once it has enough monthly history."
        )
    else:
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
