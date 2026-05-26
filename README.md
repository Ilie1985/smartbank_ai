# SmartBank AI

## Personal Finance and Budget Intelligence App

SmartBank AI is a personal finance web application built with Python and Streamlit. The app helps users manage their money by tracking income, expenses, budgets, spending patterns, financial health, and future spending forecasts.

The project combines practical financial tools with machine learning, AI-style recommendations, flexible data upload, secure transaction auditing, data cleaning, SQLite storage, and a modern custom user interface.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [User Journey](#user-journey)
- [Data Gathering and Input Methods](#data-gathering-and-input-methods)
- [Data Cleaning and Processing](#data-cleaning-and-processing)
- [Data Storage](#data-storage)
- [Dashboard](#dashboard)
- [Budget Tracker](#budget-tracker)
- [Spending Analysis](#spending-analysis)
- [AI Spending Forecast](#ai-spending-forecast)
- [Machine Learning Approach](#machine-learning-approach)
- [Machine Learning Readiness Logic](#machine-learning-readiness-logic)
- [Model Evaluation](#model-evaluation)
- [AI Insights](#ai-insights)
- [Security Audit With Blockchain-Style Hashing](#security-audit-with-blockchain-style-hashing)
- [User Interface and CSS Design](#user-interface-and-css-design)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [How to Run the Project](#how-to-run-the-project)
- [Example Bank Statement CSV Format](#example-bank-statement-csv-format)
- [Data Privacy](#data-privacy)
- [Current Limitations](#current-limitations)
- [Future Improvements](#future-improvements)
- [Skills Demonstrated](#skills-demonstrated)
- [Why This Project Is Valuable](#why-this-project-is-valuable)
- [Author](#author)
- [Project Status](#project-status)

---

## Project Overview

SmartBank AI was designed to solve a common personal finance problem:

> Many users want to understand and control their spending, but they may not have months of organised financial data available when they start.

To solve this, the app supports both:

- users who already have bank statement CSV files
- users who want to start manually by adding income, budgets, and expenses

The app provides immediate value through budgeting, spending tracking, dashboards, and category analysis. Machine learning forecasting becomes more useful once enough reliable historical data is available.

This makes SmartBank AI useful for both new users and users who already have historical bank data.

---

## Problem Statement

Many personal finance tools require users to connect a bank account, upload historical data, or manually enter large amounts of information before receiving value.

This can make budgeting tools difficult to start using.

SmartBank AI addresses this issue by allowing users to:

- start with simple manual inputs
- add expenses quickly
- set monthly income and budgets
- upload a bank statement CSV if available
- analyse spending immediately
- unlock machine learning forecasts once enough data exists

The app is designed around a realistic user journey where not every user has six months of financial data available at the beginning.

---

## Key Features

### 1. Home Page

The Home page provides a clear starting point for the user.

It includes clickable action cards that allow the user to quickly access:

- Quick Add Expense
- Budget Setup
- Upload Data
- Dashboard
- AI Spending Forecast
- Security Audit

The Home page was designed to make the user journey simpler and less overwhelming than a crowded data input page.

---

### 2. Data Source Selection

The app includes a sidebar data source selector.

Users can choose whether the app should use:

- Best available data
- Manual data only
- Uploaded CSV data only

This makes the app flexible and allows users to test different data sources.

For example:

- A new user can rely on manual entries.
- A user with a bank statement can use uploaded CSV data.
- The app can combine data where appropriate.

For machine learning, the app uses the best available reliable data. Uploaded CSV data can be used immediately if it contains enough history. Manual data is only included in machine learning once it has enough monthly history to support meaningful forecasting.

---

### 3. Quick Add Expense

The Quick Add Expense page allows users to quickly record daily spending.

Users can enter:

- amount
- description
- category
- payment method

The transaction is saved into the manual transaction database and can be used immediately by:

- Dashboard
- Budget Tracker
- Spending Analysis
- AI Insights
- Security Audit

This gives the app value even when the user does not have a bank CSV file.

---

### 4. Budget Setup

The Budget Setup page allows users to set up their monthly financial plan.

Users can:

- set monthly income
- create budget categories
- edit existing budget categories
- view saved budget data
- delete old budget categories
- view or edit monthly income

The monthly income acts as the user’s available budget pot.

Budget categories help the app compare planned spending against actual spending.

Example budget categories:

- Groceries
- Rent
- Utilities
- Restaurants
- Transport
- Holiday
- School
- Shopping

---

### 5. Upload Data

The Upload Data page supports bank statement CSV uploads.

The app supports two upload methods:

#### Original Project CSV Upload

This option is used when the CSV files already match the expected project format.

#### Flexible Bank Statement Upload With Column Mapping

This option allows users to upload real-world bank statement CSV files with different column names.

The user can map fields such as:

- transaction date
- description
- payer / payee
- reference
- amount
- money in
- money out
- balance
- transaction type
- account name
- payment method

This is important because real bank CSV files often have different structures.

For example, a bank statement may have:

```text
Booking date
Value date
Transaction type
Payer / Payee
Reference
Money in
Money out
Balance
```

The app transforms these fields into the structure needed by SmartBank AI.

---

## User Journey

The app supports two main user journeys.

### User With No Historical Data

A new user can:

1. Set monthly income.
2. Create budget categories.
3. Add daily expenses using Quick Add Expense.
4. View remaining income and budget.
5. Analyse spending by category.
6. Build up history over time.
7. Unlock better machine learning forecasting after enough months of data.

This means the app is useful from day one.

### User With Bank Statement Data

A user with historical bank data can:

1. Upload a bank statement CSV.
2. Map CSV columns to the app’s required fields.
3. Store cleaned transactions.
4. View dashboard summaries.
5. Analyse spending patterns.
6. Use machine learning forecasting if enough months are available.
7. Continue adding manual expenses for current tracking.

This gives the app immediate forecasting value if the uploaded CSV contains enough history.

---

## Data Gathering and Input Methods

SmartBank AI supports several ways to gather user data.

### Manual Data Entry

The user can manually add:

- monthly income
- budget categories
- individual expenses
- transaction details

This allows users to start using the app immediately even if they do not have a bank statement CSV.

### Quick Expense Entry

The Quick Add Expense page is designed for fast daily use.

The user can quickly enter a small number of important details, such as:

- amount
- description
- category
- payment method

This supports regular spending tracking.

### CSV Bank Statement Upload

Users can upload bank statement CSV files.

The app supports flexible column mapping, meaning it can work with different CSV structures from different banks.

This makes the upload feature more realistic because real banks do not all use the same column names.

### Data Source Modes

The app allows users to choose between:

```text
Best available data
Manual data only
Uploaded CSV data only
```

This gives users more control over how the app analyses their information.

---

## Data Cleaning and Processing

Uploaded and manually entered data is cleaned before being used by the app.

The data cleaning process includes:

- converting dates into standard date format
- converting money values into numbers
- handling currency symbols such as £
- handling commas in values such as £2,300.00
- identifying income and expenses
- assigning default values for missing optional fields
- preparing month, year, and day columns
- standardising text fields
- preparing data for charts, dashboards, and machine learning

Example transformation:

```text
£2,300.00 -> 2300.00
£45.20 -> 45.20
```

The app can also detect transaction direction:

```text
Money in  -> credit / income
Money out -> debit / expense
```

---

## Data Storage

SmartBank AI uses SQLite databases to store data locally.

The project separates uploaded data from manually entered data.

### Uploaded Data

Uploaded CSV transactions are stored in the uploaded transactions database.

When a new CSV is uploaded, it replaces the previous uploaded CSV transaction data. This avoids duplicate transactions from repeated uploads.

This behaviour is useful because bank CSV uploads are treated as the current uploaded dataset.

### Manual Data

Manual transactions and manual budgets are stored separately.

This means manually entered data is preserved even when uploaded CSV data is replaced.

Manual data includes:

- manually added expenses
- manually added transactions
- manual budget categories
- monthly income records

This separation gives the user control over both uploaded and manually entered data.

---

## Dashboard

The Financial Dashboard provides a high-level summary of the user’s financial activity.

It displays:

- total income
- total expenses
- net savings
- number of transactions
- spending by category
- visual charts

The dashboard helps users quickly understand where their money is going.

It can work with:

- uploaded CSV data
- manual data
- best available data

---

## Budget Tracker

The Budget Tracker helps users monitor their spending against their budget.

It shows:

- monthly income
- spent so far
- remaining income
- planned budget
- remaining budget
- safe daily spend
- projected month-end balance
- budget health score
- budget category breakdown

The page is designed to answer practical questions such as:

- How much have I spent this month?
- How much money do I have left?
- Am I on track with my budget?
- How much can I safely spend each day?
- Which categories are using most of my budget?

This feature is useful even without machine learning.

---

## Spending Analysis

The Spending Analysis page allows users to explore their transactions.

It includes:

- category filtering
- transaction tables
- top spending descriptions
- spending visualisations
- category-level insights

This helps users identify spending habits and understand which areas of their life cost the most.

---

## AI Spending Forecast

The AI Spending Forecast page uses machine learning to forecast future monthly spending.

The app converts individual transactions into monthly spending totals. These monthly totals are then used to train a machine learning model.

The page displays:

- machine learning readiness status
- training months available
- minimum months needed
- predicted future spending
- latest completed monthly spending
- predicted change
- Mean Absolute Error
- R² score
- actual vs predicted chart
- monthly data used by the model
- plain-English recommendation

---

## Machine Learning Approach

The project uses a Linear Regression model to predict future monthly spending.

The machine learning pipeline is:

1. Load transaction data.
2. Clean and prepare the transaction records.
3. Convert transactions into monthly spending totals.
4. Check whether enough months of data are available.
5. Train a Linear Regression model.
6. Predict future monthly spending.
7. Evaluate the model using MAE and R².
8. Display the prediction in a user-friendly way.

The aim is not only to generate a prediction, but also to explain whether the prediction is reliable.

---

## Machine Learning Readiness Logic

The app requires at least 6 months of transaction history before the machine learning forecast is considered ready.

This avoids giving unreliable predictions when there is not enough historical data.

The app handles data sources carefully.

### Uploaded CSV Data

If uploaded CSV data has at least 6 months of history, it can be used for machine learning.

### Manual Data

Manual data is useful immediately for budgeting and dashboards.

However, manual data is only used for machine learning once it has at least 6 months of monthly history.

This prevents a small number of manual entries from damaging the accuracy of the model.

### Best Available Data

When the user selects Best Available Data, the app uses the strongest available dataset for machine learning.

Uploaded CSV data can be used first, while manual data is added later when it has enough history.

---

## Model Evaluation

The app evaluates the machine learning model using:

### Mean Absolute Error

Mean Absolute Error shows the average prediction error in pounds.

Example:

```text
MAE = £262.64
```

This means the model is usually around £262.64 away from the actual monthly spending.

### R² Score

R² shows how well the model explains the spending pattern.

General interpretation:

```text
R² close to 1.00 = strong pattern
R² around 0.00 = weak or no clear pattern
R² below 0.00 = worse than a simple average prediction
```

The app does not hide weak model performance. If R² is low, the user is warned that the forecast should be treated as an estimate.

This makes the project more trustworthy because it does not pretend that every prediction is reliable.

---

## Plain-English Recommendations

The AI Spending Forecast page includes a plain-English explanation of the prediction.

Instead of only showing numbers, the app explains:

- whether spending may increase or decrease
- how confident the model is
- how large the average prediction error is
- what the user should consider doing next

Example recommendation:

```text
The model predicts that future spending may increase compared with the latest completed month.
However, the model confidence is low because the historical spending pattern is not strongly predictable.
Use this forecast as guidance only.
```

This makes the machine learning output easier for non-technical users to understand.

---

## AI Insights

The AI Insights page provides user-friendly financial observations based on the user’s data.

It helps explain spending behaviour in a more understandable way.

The goal of this section is to turn raw financial data into useful insights for the user.

Possible insights include:

- high spending categories
- unusual spending patterns
- budget warnings
- savings opportunities
- practical recommendations

---

## Security Audit With Blockchain-Style Hashing

SmartBank AI includes a blockchain-style transaction audit feature.

Each transaction is given a SHA-256 hash.

A hash is a unique digital fingerprint created from the transaction data.

If the transaction data changes, the hash changes too.

This allows the app to identify whether transaction records may have been altered.

The Security Audit page shows:

- valid hashes
- invalid hashes
- transaction hash values
- hash verification status

This is not a real blockchain network, but it uses blockchain-inspired principles:

- hashing
- tamper-evidence
- transaction integrity checking
- auditability

This feature demonstrates how cybersecurity concepts can be applied to financial data.

---

## Why Hashing Is Useful

Hashing helps protect data integrity.

For example, if a transaction originally contains:

```text
Date: 02 Jan 2026
Description: Tesco Groceries
Amount: £45.20
Type: debit
```

The app creates a hash from those values.

If someone later changes the amount or description, the recalculated hash will no longer match the stored hash.

This allows the app to flag the transaction as potentially changed.

---

## User Interface and CSS Design

SmartBank AI includes a custom CSS design to improve usability and presentation.

The UI includes:

- modern card-based layout
- clickable Home page cards
- gradient headings
- styled sidebar navigation
- responsive layout
- hover effects
- rounded cards
- custom metric cards
- improved spacing and visual hierarchy
- clean typography
- data source selector
- consistent page layout

The UI was improved to make the app more user-friendly and professional.

Instead of showing technical database options to the user, the app presents clear user-facing pages such as:

- Quick Add Expense
- Budget Setup
- Upload Data
- Dashboard
- Budget Tracker
- Spending Analysis
- AI Spending Forecast
- Security Audit
- AI Insights

---

## Technologies Used

### Programming Language

- Python

### Web App Framework

- Streamlit

### Data Processing

- Pandas
- NumPy

### Machine Learning

- Scikit-learn
- Linear Regression
- MAE evaluation
- R² evaluation

### Data Visualisation

- Plotly Express
- Streamlit charts
- Interactive dataframes

### Database

- SQLite

### Security / Integrity

- SHA-256 hashing
- blockchain-style transaction audit

### Styling and UI

- Custom CSS
- responsive layout
- card-based design
- gradient headings
- styled sidebar
- modern dashboard cards
- hover effects
- clean visual hierarchy

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smartbank-ai.git
cd smartbank-ai
```

Replace the GitHub link above with your actual repository link.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

On Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit App

```bash
streamlit run app.py
```

---

## Example Bank Statement CSV Format

The app can support flexible bank statement CSV files.

Example:

```csv
Booking date,Value date,Transaction type,Payer / Payee,Reference,Money in,Money out,Balance
02 Jan 2026,02 Jan 2026,Faster Payment In,ABC Ltd,Salary,"£2,300.00",,"£3,550.00"
04 Jan 2026,04 Jan 2026,Card Payment,Tesco,Groceries,,"£45.20","£3,504.80"
08 Jan 2026,08 Jan 2026,Direct Debit,Vodafone,Mobile bill,,"£25.00","£3,479.80"
15 Jan 2026,15 Jan 2026,Faster Payment Out,Jane Brown,Rent share,,"£750.00","£2,729.80"
25 Jan 2026,25 Jan 2026,Card Payment,Transport for London,Travel,,"£12.50","£2,717.30"
```

The app allows the user to map these columns into the fields needed by SmartBank AI.

---

## Data Privacy

This project stores data locally using SQLite.

No external banking API is used.

The app does not connect to a real bank account.

Users upload CSV files manually or enter transactions manually.

This makes the project safer for demonstration and academic purposes.

---

## Current Limitations

Although the app has many features, there are still limitations:

- The machine learning model uses a simple Linear Regression approach.
- Forecasts may be weak if spending behaviour is irregular.
- The app depends on the quality of uploaded CSV data.
- Bank CSV formats vary, so column mapping is required.
- Manual data needs several months before it can support machine learning.
- The blockchain audit is blockchain-style, not a real distributed blockchain network.
- The app currently stores data locally rather than in a cloud database.
- The app does not currently include user authentication.

---

## Future Improvements

Possible future improvements include:

- improved machine learning models such as Random Forest or XGBoost
- category-level spending forecasts
- automatic transaction categorisation
- anomaly detection for unusual spending
- user authentication
- encrypted database storage
- exportable PDF reports
- recurring payment detection
- personalised savings recommendations
- mobile-first design improvements
- integration with open banking APIs
- cloud database support
- multi-user support
- advanced AI financial coaching
- improved accessibility features

---

## Skills Demonstrated

This project demonstrates skills in:

- Python programming
- Streamlit web development
- data cleaning and preprocessing
- CSV import and transformation
- flexible column mapping
- SQLite database design
- manual and uploaded data handling
- machine learning model training
- model evaluation using MAE and R²
- interactive data visualisation
- financial analytics
- user interface design
- custom CSS styling
- hashing and data integrity checking
- practical problem solving
- user-centred software design
- software architecture
- data source management
- financial technology concepts
- cybersecurity concepts

---

## Why This Project Is Valuable

SmartBank AI is valuable because it does not rely only on machine learning.

The app provides immediate practical value through:

- budgeting
- expense tracking
- dashboards
- spending analysis
- income tracking
- remaining budget calculations
- safe daily spend calculations
- transaction auditing

Machine learning is added as an advanced feature once enough reliable historical data exists.

This makes the application useful for both:

- users who already have months of bank data
- users who are starting from zero and want to build better financial habits

The project shows how data science, machine learning, cybersecurity concepts, and software engineering can be combined into a realistic personal finance application.

---

## Recruiter-Focused Summary

SmartBank AI demonstrates the ability to build a full data-driven application from end to end.

The project includes:

- frontend development using Streamlit
- backend data storage using SQLite
- data cleaning and transformation using Pandas
- machine learning forecasting using Scikit-learn
- model evaluation using MAE and R²
- custom UI styling using CSS
- flexible CSV upload and mapping
- secure transaction integrity checks using SHA-256 hashing
- user-focused product design

This project shows practical experience in software development, data analytics, machine learning, and applied cybersecurity concepts.

---

## Academic Summary

SmartBank AI is a personal finance and budget intelligence application that combines data processing, financial analytics, machine learning, and transaction integrity auditing.

The application allows users to enter financial data manually or upload bank statement CSV files. The data is cleaned, transformed, stored in SQLite, and used across several analytical pages.

The machine learning component uses Linear Regression to forecast future monthly spending. The model is evaluated using Mean Absolute Error and R² score. The app also provides plain-English explanations to help users understand the reliability of the forecast.

The blockchain-style audit feature applies SHA-256 hashing to transaction records to support tamper-evidence and data integrity checking.

Overall, the project demonstrates a practical implementation of data-driven software development with a focus on usability, financial decision support, and responsible machine learning.

---

## Author

**Marian**

SmartBank AI was developed as a personal finance and budget intelligence project, combining software development, data analysis, machine learning, and secure transaction auditing.

---

## Project Status

The project currently includes:

- manual expense entry
- monthly income setup
- budget setup
- flexible CSV upload with column mapping
- financial dashboard
- budget tracker
- spending analysis
- AI spending forecast
- model evaluation
- AI-style recommendations
- blockchain-style transaction audit
- custom CSS user interface
- data source selection
- local SQLite data storage

Further improvements can be added in future versions.