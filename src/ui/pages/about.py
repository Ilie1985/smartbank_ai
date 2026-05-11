import streamlit as st


def about_page():
    st.header("About SmartBank AI")

    st.write(
        """
        SmartBank AI is a personal finance and banking analytics prototype built with Python.

        The application supports multiple data input methods:

        1. Upload the original project datasets
           - personal_transactions.csv
           - Budget.csv

        2. Upload a different transaction CSV using column mapping

        3. Enter transactions manually

        4. Enter budget categories manually

        The system demonstrates:

        - CSV data extraction
        - Flexible data input
        - Column mapping
        - Manual transaction entry
        - Manual budget entry
        - Data validation
        - Data cleaning
        - SQLite local storage
        - Financial dashboarding
        - Budget tracking
        - Account/card analysis
        - Machine learning spending prediction
        - Unusual transaction detection
        - Blockchain-style SHA-256 transaction auditing
        - AI-style personalised financial insights
        - Interactive Streamlit user experience
        """
    )