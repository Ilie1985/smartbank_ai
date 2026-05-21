import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_access import load_app_transactions as load_transactions
from src.analytics import monthly_spending
from src.ml_model import train_spending_model, predict_next_month
from src.ui.display import safe_dataframe

MIN_TRAINING_MONTHS = 6


def load_transactions_for_mode(mode: str) -> pd.DataFrame:
    """
    Load transactions for a specific data source mode.

    This uses the existing load_app_transactions() function, but temporarily
    changes the session data source mode so we can load uploaded and manual
    transactions separately.
    """

    original_mode = st.session_state.get("data_source_mode", "All data")

    try:
        st.session_state["data_source_mode"] = mode
        transactions = load_transactions()

        if transactions is None:
            return pd.DataFrame()

        return transactions

    except Exception:
        return pd.DataFrame()

    finally:
        st.session_state["data_source_mode"] = original_mode


def prepare_transactions_for_month_count(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare transaction dates for monthly checks.
    """

    if transactions_df is None or transactions_df.empty:
        return pd.DataFrame()

    df = transactions_df.copy()

    if "date" not in df.columns:
        return pd.DataFrame()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        return pd.DataFrame()

    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df


def count_months_available(transactions_df: pd.DataFrame) -> int:
    """
    Count how many different months are available in a transaction dataset.
    """

    df = prepare_transactions_for_month_count(transactions_df)

    if df.empty:
        return 0

    return df["month"].nunique()


def remove_duplicate_transactions(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate transactions before ML training.

    This helps prevent double counting if a transaction appears in more than one source.
    """

    if transactions_df is None or transactions_df.empty:
        return pd.DataFrame()

    df = transactions_df.copy()

    duplicate_columns = [
        column
        for column in ["date", "description", "amount", "transaction_type"]
        if column in df.columns
    ]

    if duplicate_columns:
        df = df.drop_duplicates(subset=duplicate_columns, keep="last")
    else:
        df = df.drop_duplicates(keep="last")

    return df


def exclude_current_incomplete_month(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Exclude the current month from ML training.

    The current month may be incomplete, so including it can make the model look worse.
    """

    if transactions_df is None or transactions_df.empty:
        return pd.DataFrame()

    df = transactions_df.copy()

    if "date" not in df.columns:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        return pd.DataFrame()

    df["month"] = df["date"].dt.to_period("M").astype(str)

    current_month = pd.Timestamp.today().to_period("M").strftime("%Y-%m")

    historical_df = df[df["month"] < current_month].copy()

    return historical_df


def select_ml_training_data(
    uploaded_transactions: pd.DataFrame,
    manual_transactions: pd.DataFrame,
    data_source_mode: str,
):
    """
    Choose which transaction data should be used for machine learning.

    Rule:
    - Uploaded CSV data can be used when available.
    - Manual data is only included in ML training when it has at least 6 months.
    - This avoids weak manual data reducing the quality of the uploaded CSV model.
    """

    uploaded_months = count_months_available(uploaded_transactions)
    manual_months = count_months_available(manual_transactions)

    manual_is_ml_ready = manual_months >= MIN_TRAINING_MONTHS

    notes = []

    if data_source_mode == "Uploaded CSV data only":
        selected_df = (
            uploaded_transactions.copy()
            if uploaded_transactions is not None
            else pd.DataFrame()
        )

        notes.append(
            f"Using uploaded CSV data only. Uploaded CSV months available: {uploaded_months}."
        )

        return selected_df, uploaded_months, manual_months, notes

    if data_source_mode == "Manual data only":
        selected_df = (
            manual_transactions.copy()
            if manual_transactions is not None
            else pd.DataFrame()
        )

        if manual_is_ml_ready:
            notes.append(
                f"Using manual data only. Manual months available: {manual_months}."
            )
        else:
            notes.append(
                f"Manual data has only {manual_months} month(s). "
                f"At least {MIN_TRAINING_MONTHS} months are needed before manual data can support ML forecasting."
            )

        return selected_df, manual_months, manual_months, notes

    selected_parts = []

    if uploaded_transactions is not None and not uploaded_transactions.empty:
        selected_parts.append(uploaded_transactions.copy())
        notes.append(
            f"Best available ML data is being used. Uploaded CSV data is included. Uploaded CSV months available: {uploaded_months}."
        )
    else:
        notes.append("No uploaded CSV transactions were found.")

    if manual_transactions is not None and not manual_transactions.empty:
        if manual_is_ml_ready:
            selected_parts.append(manual_transactions.copy())
            notes.append(
                f"Manual data is included because it has {manual_months} months of history."
            )
        else:
            notes.append(
                f"Manual data is useful for Dashboard, Budget Tracker, Spending Analysis, "
                f"and AI Insights, but it is not included in ML training yet because it has only "
                f"{manual_months} month(s). It will be included automatically once it reaches "
                f"{MIN_TRAINING_MONTHS} months."
            )
    else:
        notes.append("No manual transactions were found.")

    if selected_parts:
        selected_df = pd.concat(selected_parts, ignore_index=True)
    else:
        selected_df = pd.DataFrame()

    selected_months = count_months_available(selected_df)

    return selected_df, selected_months, manual_months, notes


def format_month_column(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Display months as 'May 2026' instead of '2026-05'.
    """

    if monthly_df is None or monthly_df.empty or "month" not in monthly_df.columns:
        return monthly_df

    display_df = monthly_df.copy()

    display_df["month"] = pd.to_datetime(
        display_df["month"].astype(str) + "-01",
        errors="coerce",
    ).dt.strftime("%B %Y")

    return display_df


def prediction_page():
    st.header("AI Spending Forecast")

    st.write(
        "This page uses machine learning to forecast future monthly spending. "
        "The model learns from previous monthly spending patterns and estimates "
        "how much may be spent next month."
    )

    try:
        data_source_mode = st.session_state.get("data_source_mode", "All data")

        uploaded_transactions = load_transactions_for_mode("Uploaded CSV data only")
        manual_transactions = load_transactions_for_mode("Manual data only")

        transactions, selected_months, manual_months, ml_notes = (
            select_ml_training_data(
                uploaded_transactions=uploaded_transactions,
                manual_transactions=manual_transactions,
                data_source_mode=data_source_mode,
            )
        )

        transactions = remove_duplicate_transactions(transactions)

        if transactions.empty:
            st.warning(
                "No transaction data found. Please upload or enter transactions first."
            )
            return

        training_transactions = exclude_current_incomplete_month(transactions)

        if training_transactions.empty:
            st.warning(
                "There is transaction data available, but not enough completed monthly history for ML forecasting yet."
            )

            with st.expander("Data used for this forecast"):
                st.write(f"Selected data source mode: **{data_source_mode}**")
                for note in ml_notes:
                    st.write(f"- {note}")

            return

        monthly_check = monthly_spending(training_transactions)

        if monthly_check.empty:
            st.warning("No monthly spending data is available yet.")
            return

        training_months = len(monthly_check)

        st.subheader("Machine Learning Status")

        status_col1, status_col2, status_col3 = st.columns(3)

        status_col1.metric("Training Months Available", training_months)
        status_col2.metric("Minimum Months Needed", MIN_TRAINING_MONTHS)

        if training_months >= MIN_TRAINING_MONTHS:
            status_col3.metric("ML Status", "Ready")
            st.success(
                "The machine learning model has enough completed historical monthly data to produce a forecast."
            )
        else:
            status_col3.metric("ML Status", "Not Ready")
            st.warning(
                "Not enough completed historical data for reliable machine learning forecasting. "
                f"Please add at least {MIN_TRAINING_MONTHS} months of transactions."
            )

            st.info(
                "You can still use Budget Tracker, Quick Add Expense, Dashboard, "
                "Spending Analysis, Security Audit, and AI Insights."
            )

            with st.expander("Data used for this forecast"):
                st.write(f"Selected data source mode: **{data_source_mode}**")
                for note in ml_notes:
                    st.write(f"- {note}")

            st.subheader("Current Monthly Spending Data")
            safe_dataframe(format_month_column(monthly_check), width="stretch")

            chart_monthly_check = format_month_column(monthly_check)

            fig = px.line(
                chart_monthly_check,
                x="month",
                y="expense",
                markers=True,
                title="Current Monthly Spending",
            )

            st.plotly_chart(fig, width="stretch")

            st.subheader("Plain-English Recommendation")
            st.info(
                "At the moment, the app can track spending and budgets, but it needs more completed monthly history "
                "before the ML model can identify a useful spending trend. Keep adding expenses or upload "
                "bank CSV data to improve the forecast."
            )

            return

        with st.expander("Data used for this forecast"):
            st.write(f"Selected data source mode: **{data_source_mode}**")
            for note in ml_notes:
                st.write(f"- {note}")
            st.write(
                "- The current incomplete month is excluded from ML training to avoid damaging forecast quality."
            )

        model, results, monthly = train_spending_model(training_transactions)
        prediction = predict_next_month(model, monthly)

        st.subheader("Forecast Result")

        forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

        forecast_col1.metric(
            "Predicted Spending Next Month",
            f"£{prediction:,.2f}",
        )

        latest_actual_spending = monthly["expense"].iloc[-1]
        spending_change = prediction - latest_actual_spending

        forecast_col2.metric(
            "Latest Completed Monthly Spending",
            f"£{latest_actual_spending:,.2f}",
        )

        forecast_col3.metric(
            "Predicted Change",
            f"£{spending_change:,.2f}",
        )

        st.subheader("Model Evaluation")

        eval_col1, eval_col2 = st.columns(2)

        eval_col1.metric(
            "Mean Absolute Error",
            f"£{results['mae']:,.2f}",
        )

        eval_col2.metric(
            "R² Score",
            f"{results['r2_score']:.2f}",
        )

        st.caption(
            "Mean Absolute Error shows the average prediction error in pounds. "
            "R² Score shows how well the model explains the spending pattern. "
            "A higher R² score usually means the model has found a stronger trend."
        )

        if results["r2_score"] < 0.1:
            st.warning(
                "The R² score is very low, so the spending pattern is not strongly predictable. "
                "Use this forecast as guidance only."
            )
        elif results["r2_score"] < 0.4:
            st.warning(
                "The R² score is low, so the spending pattern may not be strongly predictable. "
                "Treat this forecast as an early estimate, not a guaranteed result."
            )
        elif results["r2_score"] < 0.7:
            st.info(
                "The model has found a moderate spending pattern, but the forecast should still be used carefully."
            )
        else:
            st.success(
                "The model has found a stronger spending pattern in the historical data."
            )

        st.subheader("Actual vs Predicted Monthly Spending")

        chart_monthly = format_month_column(monthly)

        fig = px.line(
            chart_monthly,
            x="month",
            y=["expense", "predicted_expense"],
            markers=True,
            title="Actual vs Predicted Monthly Spending",
        )

        st.plotly_chart(fig, width="stretch")

        st.subheader("Monthly Data Used by the Model")

        safe_dataframe(format_month_column(monthly), width="stretch")

        st.subheader("Plain-English Recommendation")

        recommendation = generate_prediction_recommendation(
            prediction=prediction,
            latest_actual_spending=latest_actual_spending,
            spending_change=spending_change,
            mae=results["mae"],
            r2_score=results["r2_score"],
        )

        st.info(recommendation)

        st.subheader("How the Machine Learning Works")

        st.write("""
            The app converts individual transactions into monthly spending totals.
            These monthly totals are used to train a Linear Regression model.
            The model learns the spending trend over time and predicts future spending.
            """)

        st.markdown("""
            **Machine learning pipeline used by this page:**

            1. Load uploaded and manual transactions separately  
            2. Include manual data only when it has enough monthly history  
            3. Remove duplicate transactions  
            4. Exclude the current incomplete month from ML training  
            5. Convert transactions into monthly spending totals  
            6. Train a Linear Regression model  
            7. Predict future spending  
            8. Evaluate the model using MAE and R² score  
            9. Show the result as a user-friendly forecast  
            """)

    except Exception as error:
        st.warning(
            "Please add or upload transaction data first. "
            "The AI Spending Forecast needs transaction history before it can run."
        )
        st.write(error)


def generate_prediction_recommendation(
    prediction: float,
    latest_actual_spending: float,
    spending_change: float,
    mae: float,
    r2_score: float,
) -> str:
    """
    Generate a simple user-friendly recommendation from the ML forecast.
    """

    if spending_change > 0:
        direction_message = (
            f"The model predicts that future spending may increase by "
            f"about £{spending_change:,.2f} compared with the latest completed month."
        )
    elif spending_change < 0:
        direction_message = (
            f"The model predicts that future spending may decrease by "
            f"about £{abs(spending_change):,.2f} compared with the latest completed month."
        )
    else:
        direction_message = (
            "The model predicts that future spending may stay about the same "
            "as the latest completed month."
        )

    if r2_score < 0.1:
        confidence_message = (
            "However, the model confidence is very low because the historical spending pattern "
            "is not strongly predictable. Use this as a guide only."
        )
    elif r2_score < 0.4:
        confidence_message = (
            "However, the model confidence is low because the historical spending pattern "
            "is only weakly predictable. Use this as an early estimate."
        )
    elif r2_score < 0.7:
        confidence_message = (
            "The model has moderate confidence. It can help with planning, but the result "
            "should still be checked against your budget."
        )
    else:
        confidence_message = (
            "The model has found a stronger trend in your spending history, so this forecast "
            "may be more useful for planning."
        )

    action_message = (
        f"The average model error is about £{mae:,.2f}. "
        "To use this forecast practically, compare the predicted spending with your monthly budget. "
        "If the prediction is higher than expected, consider reducing flexible spending categories "
        "such as shopping, restaurants, entertainment, or travel."
    )

    return f"{direction_message} {confidence_message} {action_message}"
