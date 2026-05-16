import streamlit as st

from src.ui.pages.data_input import (
    upload_data_page,
    flexible_csv_upload_section,
)


def upload_data_menu_page():
    st.header("Upload Data")

    st.write(
        "Use this page to upload transaction and budget data. "
        "You can upload the original project CSV format, or upload a different "
        "bank statement CSV and map its columns to the app's required fields."
    )

    st.info(
        "Tip: Many banks allow users to export transactions as CSV files. "
        "You can download a bank statement CSV, upload it here, and map the columns."
    )

    option = st.radio(
        "Choose upload method",
        [
            "Upload Original Transactions and Budget Files",
            "Upload Different Transaction CSV With Column Mapping",
        ],
    )

    if option == "Upload Original Transactions and Budget Files":
        upload_data_page()

    elif option == "Upload Different Transaction CSV With Column Mapping":
        flexible_csv_upload_section()