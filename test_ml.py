from src.database import load_transactions
from src.ml_model import train_spending_model, predict_next_month
from src.fraud_detection import detect_unusual_transactions


transactions = load_transactions()

model, results, monthly = train_spending_model(transactions)
prediction = predict_next_month(model, monthly)

print("Model Results:")
print(results)

print("Predicted next month spending:")
print(prediction)

risk_df = detect_unusual_transactions(transactions)

print("Suspicious transactions:")
print(
    risk_df[risk_df["risk_status"] == "Suspicious"][
        [
            "date",
            "description",
            "amount",
            "category",
            "account_name",
            "risk_status",
            "risk_reason"
        ]
    ].head()
)