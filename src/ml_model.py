import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


MODEL_PATH = "models/spending_model.pkl"


def prepare_monthly_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare monthly spending totals for machine learning.
    """

    monthly = (
        df.groupby("month")["expense"]
        .sum()
        .reset_index()
        .sort_values(by="month")
    )

    monthly["month_number"] = range(1, len(monthly) + 1)

    return monthly


def train_spending_model(df: pd.DataFrame):
    """
    Train a linear regression model to predict future spending.
    """

    Path("models").mkdir(exist_ok=True)

    monthly = prepare_monthly_data(df)

    X = monthly[["month_number"]]
    y = monthly["expense"]

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)

    if len(monthly) > 1:
        r2 = r2_score(y, predictions)
    else:
        r2 = 0

    joblib.dump(model, MODEL_PATH)

    results = {
        "mae": mae,
        "r2_score": r2
    }

    monthly["predicted_expense"] = predictions

    return model, results, monthly


def predict_next_month(model, monthly: pd.DataFrame) -> float:
    """
    Predict the next month's spending.
    """

    next_month_number = len(monthly) + 1

    next_month_df = pd.DataFrame(
        {"month_number": [next_month_number]}
    )

    prediction = model.predict(next_month_df)

    return float(prediction[0])