# Loan Approval Prediction System (CareXpert Risk Intelligence)

URL:: https://ai-loan-predicator.streamlit.app/

## Project Overview
An end-to-end Machine Learning application that predicts whether a loan application should be **Approved** or **Rejected** based on applicant financial and demographic information.

This project was built to automate first-level loan screening for banks and financial institutions by using Machine Learning to analyze applicant profiles and generate underwriting-style risk reports.

This project includes:

✅ Data preprocessing  
✅ Missing value handling  
✅ Feature engineering  
✅ Multiple ML models training  
✅ Best model selection  
✅ Prediction pipeline  
✅ Model serialization  
✅ Interactive Streamlit web application UI  
✅ Professional underwriting-style risk intelligence report

---

## Problem Statement
Banks receive thousands of loan applications, and manual approval checks can be:

- Time-consuming  
- Costly  
- Inconsistent  
- Error-prone  

This system helps automate loan approval prediction by:

- Analyzing applicant financial history  
- Learning approval patterns from historical data  
- Predicting loan approval probability  
- Generating risk-based decision insights  
- Improving operational efficiency  

---

## Dataset Features
The model uses applicant information such as:

- Loan_ID
- Gender
- Married
- Dependents
- Education
- Self_Employed
- ApplicantIncome
- CoapplicantIncome
- LoanAmount
- Loan_Amount_Term
- Credit_History
- Property_Area

### Target Variable
**Loan_Status**
- Approved
- Rejected

---

## Machine Learning Workflow

### 1) Data Loading
- Dataset loaded using Pandas

### 2) Data Cleaning
Handled missing values:

- **Mode** → categorical columns  
- **Median** → numerical columns

### 3) Feature Engineering
Created meaningful features:

- TotalIncome
- Income_Loan_Ratio
- Log_LoanAmount
- Log_TotalIncome
- High_Income Flag

### 4) Data Encoding
Converted categorical features into numeric format using Label Encoding.

### 5) Feature Scaling
Applied StandardScaler normalization.

### 6) Model Training
Trained multiple ML models:

- Logistic Regression ✅
- Decision Tree
- KNN
- Random Forest
- XGBoost

### 7) Model Evaluation
Evaluated using:

- Accuracy Score
- Confusion Matrix
- Classification Report

### 8) Best Model Selection
Selected best-performing model based on validation accuracy.

---

## Model Performance

| Model | Accuracy |
|------|----------|
| Logistic Regression | 78.86% ✅ |
| Random Forest | 77.23% |
| KNN | 75.60% |
| XGBoost | 73.17% |
| Decision Tree | 70.73% |

### Best Model
# Logistic Regression → 78.86%

---

## Web Application (Streamlit UI)

A premium professional UI was developed using Streamlit for real-time prediction and underwriting intelligence.

### Features
- Premium dark luxury interface
- Applicant profile input form
- Credit score intelligence system
- Real-time prediction
- Approval probability score
- Risk tier classification
- Debt-to-income analysis
- Decision interpretability report
- Final underwriting verdict
- Responsive design

### Risk Categories
- **Tier 1 → High Trust**
- **Tier 2 → Moderate Risk**
- **Tier 3 → High Risk**
- **Tier 4 → Decline**

---

## Tech Stack

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost

### Visualization
- Matplotlib
- Seaborn

### Deployment / UI
- Streamlit
- Joblib

---

## Project Structure

```bash
Loan-Prediction/
│
├── dataset/
│   ├── train.csv
│   └── test.csv
│
├── model/
│   ├── loan_logistic_model.pkl
│   ├── feature_names.pkl
│   └── encoders.pkl
│
├── app/
│   └── app.py
│
├── notebook/
│   └── Loan_Prediction.ipynb
│
├── requirements.txt
└── README.md
```

---

## Run Locally

Clone repository:

```bash
git clone https://github.com/yourusername/loan-prediction-ml.git
cd loan-prediction-ml
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

---

## Business Value
This system can help:

- Banks
- FinTech startups
- Microfinance institutions
- Credit analysts
- Lending platforms

by automating first-level loan screening and reducing manual underwriting workload.

---

## Future Improvements
- SHAP Explainability
- FastAPI deployment
- Cloud deployment
- Database integration
- Authentication system
- Admin dashboard
- Live analytics

---

## Author
**Yousaf Khan**  
Machine Learning Engineer | AI Automation Developer | n8n Workflow Builder

GitHub: https://github.com/yourusername
