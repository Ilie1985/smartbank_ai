import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_unusual_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect unusual transactions using amount-based anomaly detection
    and simple rule-based checks for location and payment method.
    """

    data = df.copy()

    expenses = data[data["transaction_type"] == "debit"].copy()

    if expenses.empty:
        data["risk_status"] = "Normal"
        data["risk_reason"] = "No debit transactions available"
        return data

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    expenses["anomaly_result"] = model.fit_predict(expenses[["expense"]])

    expenses["risk_status"] = expenses["anomaly_result"].apply(
        lambda value: "Suspicious" if value == -1 else "Normal"
    )

    expenses["risk_reason"] = expenses.apply(assign_risk_reason, axis=1)

    data["risk_status"] = "Normal"
    data["risk_reason"] = "No issue detected"

    data.loc[expenses.index, "risk_status"] = expenses["risk_status"]
    data.loc[expenses.index, "risk_reason"] = expenses["risk_reason"]

    return data


def assign_risk_reason(row):
    """
    Explain why a transaction may be unusual.
    """

    if row["risk_status"] == "Suspicious":
        if row["expense"] > 1000:
            return "Very high transaction amount"

        if row.get("location", "Unknown") not in ["Unknown", "Online"]:
            return "Unusual transaction pattern with location information"

        if row.get("payment_method", "Unknown") not in ["Unknown"]:
            return "Unusual transaction pattern with payment method information"

        return "Unusual amount compared with normal spending"

    return "No issue detected"