<div align="center">

<br>

```
██╗  ██╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗██╗   ██╗     █████╗ ██╗
██║  ██║██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║╚██╗ ██╔╝    ██╔══██╗██║
███████║█████╗  ███████║██║     ██║   ███████║ ╚████╔╝     ███████║██║
██╔══██║██╔══╝  ██╔══██║██║     ██║   ██╔══██║  ╚██╔╝      ██╔══██║██║
██║  ██║███████╗██║  ██║███████╗██║   ██║  ██║   ██║       ██║  ██║██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝
```

### ✦ Advanced ML-powered Health Prediction Platform ✦
#### Predict Your Health Before It's Too Late — Powered by Machine Learning

<br>

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Visit%20Now-06d6a0?style=for-the-badge&labelColor=0d1117)](https://healthyai-dlog.onrender.com)
[![GitHub Repo](https://img.shields.io/badge/⭐%20GitHub-Star%20Repo-7c3aed?style=for-the-badge&labelColor=0d1117)](https://github.com/BhavyaKansal20/healthy-ai)

<br>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Engine-red?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-EDA-11557c?style=flat-square&logo=python&logoColor=white)

<br>

> **"Predict Your Health Before It's Too Late. No waiting rooms. No paperwork."**

</div>

---

<br>

## ⚡ At a Glance

<div align="center">

| 🫀 Heart Disease | 💉 Diabetes | 🧠 Brain Tumor | 📄 PDF Reports | 🔐 Auth System |
|:---:|:---:|:---:|:---:|:---:|
| Gradient Boosting | Gradient Boosting | EfficientNet-B0 | Auto-Generated | SHA-256 Hashed |
| 83.7% Accuracy | 97.2% Accuracy | MRI Classification | Downloadable | Session Auth |
| 3,600 records | 100,000 records | Multi-class MRI data | Risk Gauge | Private Reports |

</div>

---

<br>

## 🏗️ System Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🩺  HEALTHY AI  —  SYSTEM ARCHITECTURE              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   ┌─────────────┐     HTTPS      ┌──────────────────────────────────────┐   ║
║   │   🌐 USER   │ ─────────────► │          FLASK APPLICATION           │   ║
║   │   BROWSER   │                │                                      │   ║
║   └─────────────┘                │  ┌────────────┐  ┌────────────────┐  │   ║
║                                  │  │  Auth      │  │  Route Handler │  │   ║
║   ┌─────────────┐                │  │  Middleware │  │  /predict      │  │   ║
║   │  📱 MOBILE  │ ─────────────► │  │  (SHA-256) │  │  /eda          │  │   ║
║   │             │                │  └────────────┘  │  /reports      │  │   ║
║   └─────────────┘                │                  └────────────────┘  │   ║
║                                  └──────────────┬───────────────────────┘   ║
║                                                 │                            ║
║              ┌──────────────────────────────────┼──────────────────────┐    ║
║              │                                  │                      │    ║
║              ▼                                  ▼                      ▼    ║
║   ┌──────────────────┐             ┌─────────────────┐     ┌────────────────┐║
║   │  🧠 ML ENGINE    │             │  🗄️  SQLITE DB  │     │  📄 PDF ENGINE │║
║   │                  │             │                 │     │                │║
║   │  heart_model.pkl │             │  users table    │     │  ReportLab     │║
║   │  diabetes_  .pkl │             │  reports table  │     │  Risk Gauge    │║
║   │  brain_model.pt  │             │  feedback table │     │  Auto-Generate │║
║   └──────────────────┘             └─────────────────┘     └────────────────┘║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

<br>

## 🤖 ML Pipeline

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         ML PIPELINE — END TO END                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   RAW DATA                PREPROCESSING            MODEL TRAINING            ║
║  ──────────              ───────────────          ────────────────           ║
║  heart.csv    ────────►  Handle Nulls   ────────► GradientBoostingClassifier ║
║  3,600 rows              Label Encode             (Heart Disease)            ║
║                          StandardScaler                                      ║
║  diabetes.csv ────────►  Remove Outliers ───────► RandomForestClassifier     ║
║  100,000 rows            Feature Select           (Diabetes)                 ║
║                                                                              ║
║              EVALUATION               EXPORT             SERVE               ║
║             ────────────            ──────────          ────────             ║
║             Accuracy Score ───────► .pkl files ───────► Flask API            ║
║             ROC-AUC Score           heart_model         /predict/heart       ║
║             Confusion Matrix        diabetes_model      /predict/diabetes    ║
║             Cross-Validation        scalers.pkl         JSON response        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

<br>

## 📊 Model Performance

<div align="center">

```
  HEART DISEASE MODEL                     DIABETES MODEL                    BRAIN TUMOR MODEL
  ─────────────────                       ──────────────                    ─────────────────

  Accuracy   ████████████████░░░░  83.7%  Accuracy   ███████████████████░  97.2%  Type      MRI Classifier
  ROC-AUC    █████████████░░░░░░░  67.2%  ROC-AUC    ████████████████████  97.6%  Classes   4 tumor classes
  Dataset    ▓▓▓ 3,600 records            Dataset    ▓▓▓▓▓▓▓▓▓▓ 100,000 records    Dataset   Brain MRI dataset
  Algorithm  Gradient Boosting           Algorithm  Gradient Boosting       Algorithm EfficientNet-B0
```

| Metric | ❤️ Heart Disease | 💉 Diabetes | 🧠 Brain Tumor |
|:--|:--:|:--:|:--:|
| **Accuracy** | `83.7%` | `97.2%` | `Image-classifier dependent` |
| **ROC-AUC** | `67.2%` | `97.6%` | `OVR multi-class` |
| **Algorithm** | Gradient Boosting | Gradient Boosting | EfficientNet-B0 |
| **Training Records** | 3,600 | 100,000 | MRI class folders |
| **Features Used** | 14 clinical inputs | 8 clinical inputs | MRI image pixels |

</div>

---

<br>

## 🔮 Prediction Flow

```
                         USER SUBMITS FORM
                               │
                               ▼
             ┌─────────────────────────────────┐
             │       Input Validation          │
             │  (age, BMI, glucose, BP, etc.)  │
             └────────────────┬────────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │      StandardScaler.transform() │
             │      (normalize input values)   │
             └────────────────┬────────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │     model.predict_proba()       │
             │     → probability score [0-1]   │
             └────────────────┬────────────────┘
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
         prob < 0.3      0.3–0.6        prob > 0.6
           │                │                │
     ✅ LOW RISK    ⚠️ MODERATE RISK   🚨 HIGH RISK
               │              │              │
               └──────────────┼──────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │    PDF Report Auto-Generated    │
             │  • Risk Gauge  • Probability    │
             │  • Recommendations  • Details   │
             └─────────────────────────────────┘
                              │
                              ▼
                  Saved to DB + Available
                  in User Dashboard 📋
```

---

<br>

## ✨ Features

<details>
<summary><b>❤️ Heart Disease Prediction</b> — click to expand</summary>

<br>

Predict **10-year cardiovascular risk** using a Gradient Boosting Classifier trained on clinical data.

**Input Features:**
| Feature | Type | Description |
|---|---|---|
| `age` | Numeric | Patient age in years |
| `sysBP` | Numeric | Systolic blood pressure |
| `glucose` | Numeric | Blood glucose level |
| `totChol` | Numeric | Total cholesterol |
| `BMI` | Numeric | Body mass index |
| `currentSmoker` | Binary | Smoking status |
| `cigsPerDay` | Numeric | Cigarettes per day |
| `BPMeds` | Binary | On BP medication |
| `prevalentHyp` | Binary | Hypertension history |
| `diabetes` | Binary | Diabetes history |

</details>

<details>
<summary><b>💉 Diabetes Detection</b> — click to expand</summary>

<br>

ML model trained on **100K+ clinical records** with top-tier accuracy.

**Key Features:**
| Feature | Importance | Description |
|---|---|---|
| `HbA1c_level` | 🔴 High | Hemoglobin A1c |
| `blood_glucose_level` | 🔴 High | Fasting glucose |
| `bmi` | 🟡 Medium | Body mass index |
| `age` | 🟡 Medium | Patient age |
| `smoking_history` | 🟢 Low | Smoking status |
| `hypertension` | 🟢 Low | BP condition |
| `heart_disease` | 🟢 Low | Cardiac history |

</details>

<details>
<summary><b>🧠 Brain Tumor Detection</b> — click to expand</summary>

<br>

Deep-learning image classifier trained on MRI scans to detect:

- `Glioma`
- `Meningioma`
- `Pituitary`
- `No Tumor`

**Input:** MRI image (JPG/PNG) + patient basic information.  
**Output:** Predicted class, confidence score, risk level and downloadable PDF report.

</details>

<details>
<summary><b>📊 Exploratory Data Analysis</b> — click to expand</summary>

<br>

Built-in analytics engine renders:
- **Feature Importance** bar charts
- **Correlation Heatmaps** for all features
- **Class Distribution** pie charts
- **BMI vs Age** scatter plots
- **Dataset Statistics** summary tables

</details>

<details>
<summary><b>📄 Automated PDF Reports</b> — click to expand</summary>

<br>

Every prediction triggers auto-generation of a professional medical report:

```
┌────────────────────────────────────────┐
│         🩺 HEALTHY AI REPORT          │
│                                        │
│  Patient: John Doe      Age: 45        │
│  Date: 2026-03-13       ID: #0042      │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │      RISK GAUGE VISUALIZATION   │  │
│  │   LOW ▓▓▓░░░░░░░░░░░░ HIGH      │  │
│  │        35% — MODERATE RISK      │  │
│  └──────────────────────────────────┘  │
│                                        │
│  RECOMMENDATIONS:                      │
│  • Monitor blood pressure weekly       │
│  • Reduce sodium intake                │
│  • Consult cardiologist                │
└────────────────────────────────────────┘
```

</details>

---

<br>

## 🌐 API Routes

```
  PUBLIC ROUTES                          PRIVATE ROUTES (Auth Required)
  ─────────────                          ───────────────────────────────
  GET  /                  Landing        GET  /dashboard
  GET  /login             Auth Page      POST /predict/heart
  GET  /terms             ToS            POST /predict/diabetes
  GET  /privacy           Policy         POST /predict/brain
                                         GET  /eda/heart
                                         GET  /eda/diabetes
                                         GET  /reports
                                         GET  /download/<file>
                                         GET  /api/stats
                                         GET  /admin  (restricted)
```

---

<br>

## 🗂️ Project Structure

```
healthy-ai/
│
├── 📄 app.py                    ← Flask application entry point
├── 🤖 train_models.py           ← ML training pipeline
├── 📋 requirements.txt          ← Python dependencies
├── ⚙️  render.yaml              ← Render deployment config
│
├── 📂 data_files/
│   ├── heart.csv                ← Framingham Heart Study dataset
│   ├── diabetes.csv             ← 100K clinical records
│   └── brain_tumor_mri_dataset/ ← Kaggle MRI dataset (Training/Testing)
│
├── 📂 models/
│   ├── heart_model.pkl          ← Trained GradientBoostingClassifier
│   ├── heart_scaler.pkl         ← StandardScaler for heart features
│   ├── heart_meta.json          ← Model metadata & thresholds
│   ├── diabetes_model.pkl       ← Trained RandomForestClassifier
│   ├── diabetes_scaler.pkl      ← StandardScaler for diabetes features
│   ├── diabetes_le_*.pkl        ← LabelEncoders for categorical inputs
│   ├── brain_tumor_model.pt     ← Trained PyTorch model
│   ├── brain_tumor_labels.pkl   ← Brain class labels
│   └── brain_tumor_meta.json    ← Brain model metadata
│
├── 📂 static/
│   ├── img/logo.png
│   └── reports/                 ← Generated PDF reports
│
└── 📂 templates/
    ├── base.html                ← Base layout
    ├── index.html               ← Landing page
    ├── login.html               ← Auth page
    ├── dashboard.html           ← User dashboard
    ├── reports.html             ← Report history
    ├── predict_heart.html       ← Heart prediction form
    ├── predict_diabetes.html    ← Diabetes prediction form
    ├── predict_brain.html       ← Brain MRI prediction form
    ├── eda.html                 ← EDA visualizations
    ├── terms.html
    └── privacy.html
```

---

<br>

## ⚙️ Setup & Run Locally

### Prerequisites

```bash
python --version   # Python 3.11+
pip --version      # pip 22+
```

### Step 1 — Clone

```bash
git clone https://github.com/BhavyaKansal20/healthy-ai.git
cd healthy-ai
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Train Models

```bash
python train_models.py
# ✔ heart_model.pkl saved
# ✔ diabetes_model.pkl saved
# ✔ brain_tumor_model.pt saved
# ✔ scalers and encoders exported
```

### Step 4 — Launch

```bash
python app.py
# 🚀 Running on http://localhost:5000
```

---

<br>

## 🧰 Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:--|:--|:--|
| **Language** | ![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white) | Core runtime |
| **Backend** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | Web framework & routing |
| **ML (Tabular)** | ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white) | Heart/Diabetes training & inference |
| **ML (Vision)** | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) | Brain MRI model training & inference |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | Users, reports, feedback |
| **PDF** | ![ReportLab](https://img.shields.io/badge/ReportLab-CC0000?style=flat-square) | Auto PDF generation |
| **Analytics** | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square&logo=python&logoColor=white) | EDA charts & plots |
| **Security** | ![SHA-256](https://img.shields.io/badge/SHA--256-333?style=flat-square) | Password hashing |
| **Deployment** | ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white) | Cloud hosting |

</div>

---

<br>

## 🔐 Security Architecture

```
  USER PASSWORD
       │
       ▼
  SHA-256 Hash ──────► Stored in SQLite (never plain text)
       
  LOGIN REQUEST
       │
       ├─► Hash & Compare ──► ✅ Match → Session Created
       │                      ❌ Mismatch → 401 Denied
       │
       └─► Flask Session ──► Secure cookie (server-side)
                              Every private route validates session
```

---

<br>

## ⚠️ Medical Disclaimer

> **Healthy AI is developed for educational and research purposes only.**
> Predictions generated by machine learning models do **not** constitute medical advice.
> Always consult a qualified healthcare professional for diagnosis and treatment.

---

<br>

## 👨‍💻 Author

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   👤  Bhavya Kansal                                          ║
║   🎓  AI Engineer | DeepTech Developer                       ║
║   🏢  Founder — MultiModex AI                                ║
║   🎓  B.Tech AI & ML — Thapar Institute of Engg. & Tech      ║
║   🔬  AI/ML Intern Trainee — IIT Ropar × NIELIT              ║
║   🌐  bhavyakansal.dev                                       ║
║   📧  kansalbhavya27@gmail.com                               ║
║                                                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

[![Portfolio](https://img.shields.io/badge/🌐%20Portfolio-bhavyakansal.dev-06d6a0?style=for-the-badge&labelColor=0d1117)](https://bhavyakansal.dev)
[![GitHub](https://img.shields.io/badge/GitHub-BhavyaKansal20-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BhavyaKansal20)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kansal0920-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kansal0920)
[![MultiModex AI](https://img.shields.io/badge/🤖%20MultiModex%20AI-Platform-7c3aed?style=for-the-badge&labelColor=0d1117)](https://multimodexai.vercel.app)

</div>

---

<br>

## ⭐ Support

If **Healthy AI** helped you or impressed you:

```
  1. ⭐ Star this repository
  2. 🍴 Fork and build on it
  3. 📣 Share with your network
  4. 🐛 Open issues / PRs
```

Every star helps this project reach more developers. 🙏

---

<div align="center">

<br>

```
  ╔══════════════════════════════════════════════════════╗
  ║     🩺  H E A L T H Y   A I                         ║
  ║     MultiModex AI  •  © 2026 Bhavya Kansal           ║
  ║     Built with ❤️  for healthier lives               ║
  ╚══════════════════════════════════════════════════════╝
```

[![Live Demo](https://img.shields.io/badge/🚀%20Try%20It%20Live-healthyai--dlog.onrender.com-06d6a0?style=for-the-badge)](https://healthyai-dlog.onrender.com)

</div>
