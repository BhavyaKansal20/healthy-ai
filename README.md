# 🩺 Healthy AI — Setup & Launch Guide

## Overview
**Healthy AI** is an advanced ML-powered health prediction web platform built with:
- **Backend**: Python Flask + SQLite
- **ML**: Gradient Boosting Classifier (scikit-learn)
- **PDF Reports**: ReportLab
- **Frontend**: Glassmorphism UI (HTML/CSS/JS)
- **Database**: SQLite (zero-setup required)

---

## 📁 Project Structure
```
healthyai/
├── app.py                   # Main Flask application
├── train_models.py          # Model training script
├── requirements.txt         # Python dependencies
├── healthyai.db             # SQLite database (auto-created)
├── data_files/
│   ├── heart.csv            # Heart disease dataset
│   └── diabetes.csv         # Diabetes dataset
├── models/                  # Saved ML models (.pkl files)
├── static/
│   ├── img/logo.png         # Healthy AI logo
│   └── reports/             # Generated PDF reports
└── templates/               # HTML templates (Jinja2)
    ├── base.html
    ├── index.html
    ├── dashboard.html
    ├── predict_heart.html
    ├── predict_diabetes.html
    ├── eda.html
    └── reports.html
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train ML Models (already done — skip if models/ exists)
```bash
python train_models.py
```
This trains both models and saves them to `models/`.

### 3. Run the Application
```bash
python app.py
```
Open browser at: **http://localhost:5000**

---

## 🌐 Pages & Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page with features overview |
| `/dashboard` | User dashboard with stats & quick actions |
| `/predict/heart` | ❤️ Heart disease prediction form |
| `/predict/diabetes` | 💉 Diabetes prediction form |
| `/eda/heart` | 📊 Heart disease EDA & visualizations |
| `/eda/diabetes` | 📊 Diabetes EDA & visualizations |
| `/reports` | 📋 All saved reports with download |
| `/download/<file>` | Download PDF report |

---

## 🧪 Model Details

### Heart Disease Model
- **Algorithm**: Gradient Boosting Classifier
- **Dataset**: Framingham Heart Study (4,238 records)
- **Accuracy**: 83.74%  |  **ROC-AUC**: 68.10%
- **Features**: 15 clinical parameters
- **Target**: 10-Year CHD Risk (TenYearCHD)

### Diabetes Model
- **Algorithm**: Gradient Boosting Classifier
- **Dataset**: 100,000 patient records
- **Accuracy**: 97.22%  |  **ROC-AUC**: 97.64%
- **Features**: 8 metabolic parameters
- **Target**: Diabetes (0/1)

---

## 📄 Report Features
Each prediction generates a PDF report containing:
- Patient info (Name, Age, Gender)
- Report ID and timestamp
- Prediction result & risk level
- All input parameters
- Personalized medical recommendations
- Healthy AI branding & disclaimer

---

## 🔐 Authentication
- User registration and login (SQLite)
- Passwords hashed with SHA-256
- Session-based authentication
- Each user sees only their own reports

---

## 💡 Tech Stack
| Layer | Technology |
|-------|-----------|
| Web Framework | Flask 2.x |
| Database | SQLite (via sqlite3) |
| ML Library | scikit-learn (GradientBoosting) |
| PDF Generation | ReportLab |
| Charts | Matplotlib |
| Frontend | Vanilla JS + CSS Glassmorphism |
| Fonts | Google Fonts (Outfit + Space Mono) |

---

## ⚠️ Disclaimer
This application is for **educational and research purposes only**. 
Predictions are not medical advice. Always consult a qualified healthcare professional.
