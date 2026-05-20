from urllib.parse import quote

import streamlit as st


def render_clickable_card(icon, badge, title, description, colour_class, target_page):
    """
    Render a clickable card that navigates to another Streamlit page.
    """

    encoded_page = quote(target_page)

    st.markdown(
        f"""
<a class="card-link" href="?page={encoded_page}" target="_self">
    <div class="action-card {colour_class}">
        <div class="card-top">
            <div class="card-icon">{icon}</div>
            <div class="card-badge">{badge}</div>
        </div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
</a>
""",
        unsafe_allow_html=True,
    )


def home_page():
    st.markdown(
        """
<div class="gradient-title">Welcome to SmartBank AI</div>
<div class="hero-subtitle">
A personal finance intelligence app that helps you track expenses, manage budgets,
analyse spending patterns, detect unusual transactions, and forecast future spending
using machine learning.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="section-header">
    <span class="section-icon" style="background:#dbeafe;color:#2563eb;">🚀</span>
    <span>Start here</span>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        render_clickable_card(
            icon="⚡",
            badge="Fast",
            title="Quick Add Expense",
            description="Add daily spending quickly and keep your budget tracker up to date.",
            colour_class="card-green",
            target_page="Quick Add Expense",
        )

    with col2:
        render_clickable_card(
            icon="💙",
            badge="Plan",
            title="Set Monthly Budget",
            description="Create your monthly income and budget categories so expenses can be tracked properly.",
            colour_class="card-blue",
            target_page="Budget Setup",
        )

    with col3:
        render_clickable_card(
            icon="📤",
            badge="Import",
            title="Upload Bank CSV",
            description="Upload a bank statement CSV and map columns such as Money In, Money Out, and Reference.",
            colour_class="card-orange",
            target_page="Upload Data",
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        render_clickable_card(
            icon="🤖",
            badge="ML",
            title="AI Spending Forecast",
            description="Use machine learning to estimate future monthly spending once enough data is available.",
            colour_class="card-purple",
            target_page="AI Spending Forecast",
        )

    with col5:
        render_clickable_card(
            icon="📊",
            badge="Insights",
            title="View Dashboard",
            description="See income, expenses, savings, category spending, and monthly trends.",
            colour_class="card-blue",
            target_page="Dashboard",
        )

    with col6:
        render_clickable_card(
            icon="🔐",
            badge="Audit",
            title="Security Audit",
            description="Check transaction hashes and identify possible changes in stored transaction records.",
            colour_class="card-red",
            target_page="Security Audit",
        )

    st.markdown(
        """
<div class="section-header">
    <span class="section-icon" style="background:#ede9fe;color:#7c3aed;">✨</span>
    <span>Recommended user journey</span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.info(
        "Start by setting your monthly income and budget categories. "
        "Then add expenses manually or upload a bank CSV. "
        "After enough monthly history is available, the AI Spending Forecast can predict future spending."
    )
