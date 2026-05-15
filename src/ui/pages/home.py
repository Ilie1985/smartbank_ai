import streamlit as st


def home_page():
    st.header("Welcome to SmartBank AI")

    st.write(
        "SmartBank AI helps you track your spending, manage budgets, "
        "forecast future expenses, and understand your financial habits."
    )

    st.markdown(
        """
        <div class="section-note">
            Start by choosing one of the actions below. You can quickly add an expense,
            set a budget, upload bank data, or check your financial dashboard.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💸 Quick Add Expense")
        st.write(
            "Record a new expense quickly. This is useful for daily spending tracking."
        )

        if st.button("Go to Quick Add Expense"):
            st.session_state["selected_page"] = "Quick Add Expense"
            st.rerun()

        st.subheader("📊 Check Budget Health")
        st.write(
            "See your remaining budget, daily allowance, weekly allowance, "
            "and projected month-end spending."
        )

        if st.button("Go to Budget Tracker"):
            st.session_state["selected_page"] = "Budget Tracker"
            st.rerun()

        st.subheader("🤖 View Spending Prediction")
        st.write(
            "Use machine learning to forecast future spending when enough data exists."
        )

        if st.button("Go to Prediction"):
            st.session_state["selected_page"] = "Prediction"
            st.rerun()

    with col2:
        st.subheader("🧾 Set or Update Budget")
        st.write(
            "Create or update your monthly budget categories."
        )

        if st.button("Go to Budget Setup"):
            st.session_state["selected_page"] = "Budget Setup"
            st.rerun()

        st.subheader("📁 Upload Bank CSV")
        st.write(
            "Upload a bank statement CSV or use column mapping for different CSV formats."
        )

        if st.button("Go to Upload Data"):
            st.session_state["selected_page"] = "Upload Data"
            st.rerun()

        st.subheader("📈 View Dashboard")
        st.write(
            "See your income, expenses, category spending, and monthly trends."
        )

        if st.button("Go to Dashboard"):
            st.session_state["selected_page"] = "Dashboard"
            st.rerun()