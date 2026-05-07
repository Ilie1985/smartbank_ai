# SmartBank AI

SmartBank AI is a personal finance and budget intelligence application built with Python and Streamlit.

## Project Overview

The application allows users to upload personal transaction data and budget data. It cleans the data, stores it locally in SQLite, and provides dashboards, budget tracking, machine learning predictions, unusual transaction detection, blockchain-style audit hashes, and AI-style financial insights.

## Project Logic

The application uses two connected datasets: a personal transactions dataset and a budget dataset. The personal transactions dataset contains transaction-level information including date, description, amount, transaction type, category, and account name. The budget dataset contains planned budget values for each spending category.

The application begins by allowing the user to upload both CSV files. The files are validated to ensure that the required columns are present. The data is then cleaned using a pandas-based pipeline. This includes standardising column names, converting dates and amounts, removing duplicates, handling missing values, and creating new fields such as month, year, income, and expense.

After cleaning, the datasets are stored locally in a SQLite database. The transaction data is used to generate financial dashboard metrics such as total income, total expenses, net savings, monthly trends, and spending by category. The budget data is joined with actual spending data to compare planned budget against real spending. This allows the application to identify categories where the user is over budget, close to the limit, or within budget.

Machine learning is used to predict future spending based on historical monthly expenses. Anomaly detection is used to identify unusual transactions based on transaction amounts. A blockchain-style audit feature uses SHA-256 hashing to create tamper-evident records for each transaction. Finally, AI-style insights translate the analysis into simple language that helps users understand their financial behaviour.

## Datasets

The application uses two connected CSV files.

### personal_transactions.csv

Columns:

- Date
- Description
- Amount
- Transaction Type
- Category
- Account Name

### Budget.csv

Columns:

- Category
- Budget

## Features

- CSV upload
- Data validation
- Data cleaning
- Local SQLite storage
- Financial dashboard
- Budget tracker
- Account/card analysis
- Spending analysis
- Machine learning spending prediction
- Unusual transaction detection
- Blockchain-style SHA-256 audit hashing
- AI-style financial insights

## Technologies Used

- Python
- Pandas
- SQLite
- Streamlit
- Plotly
- Scikit-learn
- Joblib
- Hashlib

## How to Run

Create a virtual environment:

```bash
python -m venv venv