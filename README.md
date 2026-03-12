<div align="center">

🩺 Healthy AI

Advanced ML-Powered Clinical Health Prediction Platform

<p align="center">
<a href="https://healthyai-dlog.onrender.com"><b>View Live Demo</b></a> •
<a href="https://www.google.com/search?q=%23-quick-start"><b>Quick Start</b></a> •
<a href="https://www.google.com/search?q=%23-ml-architecture--pipeline"><b>Architecture</b></a> •
<a href="https://www.google.com/search?q=%23-model-analytics"><b>Analytics</b></a>
</p>

Predict Heart Disease and Diabetes risk instantly using production-grade machine learning models.

</div>

⚡ Overview

Healthy AI is a comprehensive, full-stack predictive healthcare platform. It bridges the gap between raw clinical data and actionable patient insights. By leveraging Gradient Boosting and other advanced classification algorithms, it provides immediate risk assessments alongside professional, downloadable medical reports.

Live Deployment: https://healthyai-dlog.onrender.com

(Note: Hosted on Render free tier. The server may take 30-50 seconds to spin up after periods of inactivity.)

🧠 ML Architecture & Pipeline

A look under the hood at how data flows from raw clinical records to actionable PDF reports.

graph TD
    subgraph Data Pipeline
        A[Raw Clinical Data] -->|Cleaning & Imputation| B(Feature Engineering)
        B --> C[Standard Scaler / Label Encoders]
    end

    subgraph Model Training
        C --> D{Model Selection}
        D -->|Gradient Boosting| E[Heart Disease Model]
        D -->|Random Forest| F[Diabetes Model]
    end

    subgraph Production API
        E --> G((Flask Backend))
        F --> G
        G <--> H[(SQLite Database)]
    end

    subgraph Client Application
        G -->|JSON API| I[Web Dashboard]
        I -->|Visual Gauge| J[Risk Assessment UI]
        G -->|ReportLab| K[PDF Generation]
    end


🔄 Prediction Flow

sequenceDiagram
    participant User
    participant Frontend UI
    participant Flask API
    participant ML Model
    participant PDF Generator

    User->>Frontend UI: Inputs Clinical Vitals (BMI, Glucose, etc.)
    Frontend UI->>Flask API: POST /predict/{disease}
    Flask API->>ML Model: Apply Scalers & Predict Probability
    ML Model-->>Flask API: Return Risk % (e.g., 87%)
    Flask API->>PDF Generator: Compile Patient Data
    PDF Generator-->>Flask API: medical_report.pdf
    Flask API-->>Frontend UI: Render Risk Gauge & PDF Download
    Frontend UI-->>User: Display High/Low Risk & Report


📊 Model Analytics

Our models are trained on robust clinical datasets, optimized for high recall in medical environments where false negatives are costly.

Predictive Model

Accuracy

ROC-AUC

Dataset Size

Key Features Analyzed

❤️ Heart Disease

83.7%

67.2%

3.6K

Systolic BP, Glucose, Cholesterol, BMI

💉 Diabetes

97.2%

97.6%

100K+

HbA1c, Blood Glucose, BMI, Age

<details>
<summary><b>🔍 View Dataset Distribution (Click to Expand)</b></summary>

pie title Diabetes Dataset Class Distribution
    "Negative (Healthy)" : 91500
    "Positive (Diabetic)" : 8500


Note: Models utilize SMOTE/class weighting to handle inherent medical dataset imbalances.

</details>

✨ Core Features

🩺 Clinical Predictions

Heart Disease Assessment: Predicts 10-year cardiovascular risk utilizing a meticulously trained Gradient Boosting Classifier.

Diabetes Detection: Highly accurate predictions based on a 100K+ clinical record dataset focusing on HbA1c and glucose levels.

📈 Exploratory Data Analysis (EDA) Dashboard

Built-in visual analytics directly in the browser:

Feature importance rankings.

Correlation matrices & dataset statistics.

Interactive BMI / Age distribution charts.

📄 Automated Medical Reports

Instant PDF generation for every prediction.

Includes patient details, visual risk gauges, probability percentages, and medical recommendations.

🔐 Secure User Ecosystem

Authentication: SHA-256 password hashing & secure session management.

History: Persistent storage of user prediction history and downloadable past reports.

Admin Panel: Restricted internal dashboard for viewing platform analytics and user feedback.

🗺️ System Routes

Route

Method

Description

Access Level

/

GET

Landing page & Overview

🟢 Public

/login

GET/POST

User authentication & registration

🟢 Public

/dashboard

GET

Main user dashboard

🔴 Private

/predict/<type>

GET/POST

Heart/Diabetes inference engine

🔴 Private

/eda/<type>

GET

Visual dataset analytics

🔴 Private

/reports

GET

Personal prediction history

🔴 Private

/download/<file>

GET

Fetch generated PDF report

🔴 Private

/api/stats

GET

JSON platform statistics API

🔴 Private

🚀 Quick Start (Local Development)

Get the ML platform running on your local machine in under 3 minutes.

1️⃣ Clone the Repository

git clone [https://github.com/BhavyaKansal20/healthy-ai.git](https://github.com/BhavyaKansal20/healthy-ai.git)
cd healthy-ai


2️⃣ Install Dependencies

It is recommended to use a virtual environment (venv).

pip install -r requirements.txt


3️⃣ Train the Machine Learning Models

This script processes heart.csv and diabetes.csv, trains the models, and outputs the .pkl files to the models/ directory.

python train_models.py


4️⃣ Run the Application

python app.py


Success: Open your browser and navigate to http://localhost:5000

📁 Project Structure

healthy-ai/
├── app.py                  # Core Flask application & routing
├── train_models.py         # ML pipeline & model generation
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
├── data_files/             # Raw clinical datasets
│   ├── heart.csv
│   └── diabetes.csv
├── models/                 # Serialized ML artifacts (.pkl, .json)
├── static/                 # CSS, JS, Images, & generated PDFs
└── templates/              # Jinja2 HTML templates
    ├── index.html
    ├── dashboard.html
    └── predict_*.html


⚠️ Medical Disclaimer

Healthy AI is developed for educational, portfolio, and research purposes only.
The predictions generated by these machine learning models do not constitute professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional regarding any medical conditions or health concerns.

<div align="center">

👨‍💻 Developed by Bhavya Kansal

Founder — Automyx AI

If this project helped you understand ML deployment or inspired your own work, please consider giving it a ⭐!

<img src="https://www.google.com/search?q=https://img.shields.io/badge/Automyx_AI-2026-black%3Fstyle%3Dfor-the-badge">

</div>
