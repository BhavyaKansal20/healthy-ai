"""
Healthy AI - Flask Web Application
Heart Disease & Diabetes Prediction Platform
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from reportlab.platypus import Image
import sqlite3, hashlib, json, os, io, base64, re
from datetime import datetime
import joblib, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'healthyai_secret_2026_secure')

BASE        = os.path.dirname(__file__)
MODELS_DIR  = os.path.join(BASE, 'models')
REPORTS_DIR = os.path.join(BASE, 'static', 'reports')
DB_PATH     = os.path.join(BASE, 'healthyai.db')
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR,  exist_ok=True)

# ─── Load models (trained during build via render.yaml) ────
def load_models():
    heart_pkl = os.path.join(MODELS_DIR, 'heart_model.pkl')
    diab_pkl  = os.path.join(MODELS_DIR, 'diabetes_model.pkl')

    # If models missing or incompatible, train now (fallback)
    need_train = not os.path.exists(heart_pkl) or not os.path.exists(diab_pkl)
    if not need_train:
        try:
            joblib.load(heart_pkl)
            joblib.load(diab_pkl)
        except Exception:
            need_train = True
            print("⚠️  Models incompatible — retraining...")

    if need_train:
        print("🔄 Training models (fallback)...")
        import train_models
        train_models.train_heart()
        train_models.train_diabetes()
        print("✅ Models ready.")

    global heart_model, heart_scaler, heart_meta
    global diabetes_model, diabetes_scaler, diabetes_le_gender, diabetes_le_smoke, diabetes_meta

    heart_model        = joblib.load(os.path.join(MODELS_DIR, 'heart_model.pkl'))
    heart_scaler       = joblib.load(os.path.join(MODELS_DIR, 'heart_scaler.pkl'))
    with open(os.path.join(MODELS_DIR, 'heart_meta.json')) as f:
        heart_meta = json.load(f)

    diabetes_model     = joblib.load(os.path.join(MODELS_DIR, 'diabetes_model.pkl'))
    diabetes_scaler    = joblib.load(os.path.join(MODELS_DIR, 'diabetes_scaler.pkl'))
    diabetes_le_gender = joblib.load(os.path.join(MODELS_DIR, 'diabetes_le_gender.pkl'))
    diabetes_le_smoke  = joblib.load(os.path.join(MODELS_DIR, 'diabetes_le_smoke.pkl'))
    with open(os.path.join(MODELS_DIR, 'diabetes_meta.json')) as f:
        diabetes_meta = json.load(f)

# Declare globals first so gunicorn can import the module without blocking
heart_model = heart_scaler = heart_meta = None
diabetes_model = diabetes_scaler = diabetes_le_gender = diabetes_le_smoke = diabetes_meta = None

# Load models — fast if already trained during build, trains if missing
load_models()

# ─── Database ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            report_type TEXT NOT NULL,
            patient_name TEXT,
            patient_age INTEGER,
            patient_gender TEXT,
            input_data TEXT,
            prediction TEXT,
            probability REAL,
            risk_level TEXT,
            report_file TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        db.commit()

init_db()

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def logged_in(): return 'user_id' in session

# ─── Chart helpers ─────────────────────────────────────────
def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True, dpi=110)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return b64

PALETTE = ['#00d4ff', '#7c3aed', '#06d6a0', '#ff6b6b', '#ffd166', '#118ab2']

def chart_feature_importance(meta, title):
    fi     = meta['feature_importance']
    labels = list(fi.keys())
    vals   = list(fi.values())
    order  = sorted(range(len(vals)), key=lambda i: vals[i])
    labels = [labels[i] for i in order]
    vals   = [vals[i]   for i in order]
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0,0,0,0))
    bars = ax.barh(labels, vals, color=PALETTE[0], alpha=0.85, height=0.6)
    for bar, v in zip(bars, vals):
        ax.text(v + 0.002, bar.get_y() + bar.get_height()/2, f'{v:.3f}',
                va='center', color='white', fontsize=8)
    ax.set_xlabel('Importance', color='white')
    ax.set_title(f'Feature Importance - {title}', color='white', fontsize=12, pad=10)
    ax.tick_params(colors='white')
    for spine in ax.spines.values(): spine.set_edgecolor('#ffffff30')
    ax.xaxis.label.set_color('white')
    return fig_to_b64(fig)

def chart_class_dist(meta, labels_map, title):
    dist = meta['class_distribution']
    keys = list(dist.keys())
    vals = [dist[k] for k in keys]
    lbls = [labels_map.get(k, k) for k in keys]
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0,0,0,0))
    wedges, texts, autotexts = ax.pie(vals, labels=lbls, autopct='%1.1f%%',
                                       colors=[PALETTE[2], PALETTE[3]],
                                       startangle=90, textprops={'color':'white'})
    for at in autotexts: at.set_color('white')
    ax.set_title(f'Class Distribution - {title}', color='white', fontsize=11, pad=10)
    return fig_to_b64(fig)

def chart_correlation(meta, title):
    corr       = meta['correlation']
    labels     = list(corr.keys())
    vals       = list(corr.values())
    colors_bar = [PALETTE[0] if v >= 0 else PALETTE[3] for v in vals]
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0,0,0,0))
    ax.bar(range(len(labels)), vals, color=colors_bar, alpha=0.8)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', color='white', fontsize=8)
    ax.axhline(0, color='white', linewidth=0.5)
    ax.set_title(f'Feature Correlation with Target - {title}', color='white', fontsize=11, pad=10)
    ax.tick_params(colors='white')
    for spine in ax.spines.values(): spine.set_edgecolor('#ffffff30')
    ax.set_ylabel('Correlation', color='white')
    return fig_to_b64(fig)

# ─── EDA Charts ────────────────────────────────────────────
def get_eda_charts(model_type):
    import pandas as pd
    if model_type == 'heart':
        df = pd.read_csv(os.path.join(BASE, 'data_files', 'heart.csv'))
        df.columns = df.columns.str.strip()
        meta       = heart_meta
        fi_chart   = chart_feature_importance(meta, 'Heart Disease')
        dist_chart = chart_class_dist(meta, {'0': 'No CHD', '1': 'CHD Risk'}, 'Heart Disease')
        corr_chart = chart_correlation(meta, 'Heart Disease')
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_alpha(0)
        ax.set_facecolor((0,0,0,0))
        for target_val, color, lbl in [(0, PALETTE[0], 'No CHD'), (1, PALETTE[3], 'CHD')]:
            ax.hist(df[df['TenYearCHD']==target_val]['age'].dropna(),
                    bins=20, alpha=0.6, color=color, label=lbl)
        ax.set_xlabel('Age', color='white')
        ax.set_ylabel('Count', color='white')
        ax.set_title('Age Distribution by Outcome', color='white', fontsize=11)
        ax.tick_params(colors='white')
        ax.legend(labelcolor='white', facecolor='#0a0a1a')
        for sp in ax.spines.values(): sp.set_edgecolor('#ffffff30')
        age_chart = fig_to_b64(fig)
        return {'fi': fi_chart, 'dist': dist_chart, 'corr': corr_chart, 'age': age_chart}
    else:
        df = pd.read_csv(os.path.join(BASE, 'data_files', 'diabetes.csv')).sample(5000, random_state=42)
        meta       = diabetes_meta
        fi_chart   = chart_feature_importance(meta, 'Diabetes')
        dist_chart = chart_class_dist(meta, {'0': 'No Diabetes', '1': 'Diabetes'}, 'Diabetes')
        corr_chart = chart_correlation(meta, 'Diabetes')
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_alpha(0)
        ax.set_facecolor((0,0,0,0))
        for target_val, color, lbl in [(0, PALETTE[0], 'No Diabetes'), (1, PALETTE[3], 'Diabetes')]:
            ax.hist(df[df['diabetes']==target_val]['bmi'].dropna(),
                    bins=25, alpha=0.6, color=color, label=lbl)
        ax.set_xlabel('BMI', color='white')
        ax.set_ylabel('Count', color='white')
        ax.set_title('BMI Distribution by Outcome', color='white', fontsize=11)
        ax.tick_params(colors='white')
        ax.legend(labelcolor='white', facecolor='#0a0a1a')
        for sp in ax.spines.values(): sp.set_edgecolor('#ffffff30')
        bmi_chart = fig_to_b64(fig)
        return {'fi': fi_chart, 'dist': dist_chart, 'corr': corr_chart, 'age': bmi_chart}

# ─── Prediction gauge chart ────────────────────────────────
def gauge_chart(probability, risk_level):
    fig, ax = plt.subplots(figsize=(5, 3), subplot_kw={'projection': 'polar'})
    fig.patch.set_alpha(0)
    ax.set_facecolor((0,0,0,0))
    for t_start, t_end, col in [(np.pi, np.pi*2/3, '#06d6a0'),
                                 (np.pi*2/3, np.pi/3, '#ffd166'),
                                 (np.pi/3,   0,       '#ff6b6b')]:
        t = np.linspace(t_start, t_end, 50)
        ax.fill_between(t, 0.7, 1.0, color=col, alpha=0.7)
    needle_angle = np.pi * (1 - probability)
    ax.annotate('', xy=(needle_angle, 0.85), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='white', lw=2))
    ax.set_ylim(0, 1.1)
    ax.set_theta_zero_location('E')
    ax.set_thetalim(0, np.pi)
    ax.axis('off')
    ax.text(np.pi/2, 1.25, f'{probability*100:.1f}%', ha='center', va='center',
            color='white', fontsize=16, fontweight='bold', transform=ax.transData)
    ax.text(np.pi/2, 1.45, risk_level, ha='center', va='center',
            color={'Low Risk': '#06d6a0', 'Moderate Risk': '#ffd166',
                   'High Risk': '#ff6b6b'}.get(risk_level, 'white'),
            fontsize=10, transform=ax.transData)
    return fig_to_b64(fig)

# ─── PDF Report ────────────────────────────────────────────
def generate_pdf_report(report_type, patient_info, input_data, prediction, probability, risk_level, report_id):
    filename = f"report_{report_type}_{report_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story  = []

    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                 fontSize=24, textColor=colors.HexColor('#7c3aed'),
                                 spaceAfter=6, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'],
                                    fontSize=11, textColor=colors.HexColor('#555'),
                                    alignment=TA_CENTER, spaceAfter=20)
    section_style = ParagraphStyle('Sec', parent=styles['Heading2'],
                                   fontSize=13, textColor=colors.HexColor('#7c3aed'),
                                   spaceBefore=16, spaceAfter=8)
    normal_style = ParagraphStyle('Norm', parent=styles['Normal'],
                                  fontSize=10, leading=16, spaceAfter=6)
    disclaimer_style = ParagraphStyle('Disc', parent=styles['Normal'],
                                      fontSize=8, textColor=colors.HexColor('#888'),
                                      alignment=TA_CENTER, leading=12)
    risk_color = {'Low Risk': '#06d6a0', 'Moderate Risk': '#f59e0b',
                  'High Risk': '#ef4444'}.get(risk_level, '#555')

    # Logo
    logo_path = os.path.join(BASE, 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=60, height=60)
        logo.hAlign = 'CENTER'
        story.append(logo)

    # Header
    story.append(Paragraph("Healthy AI", title_style))
    story.append(Paragraph("Advanced Health Prediction Report", subtitle_style))
    story.append(HRFlowable(width='100%', thickness=2,
                             color=colors.HexColor('#7c3aed'), spaceAfter=12))

    # Report type
    story.append(Paragraph(
        f"Report Type: {'Heart Disease Prediction' if report_type == 'heart' else 'Diabetes Prediction'}",
        section_style))

    # Meta table
    meta_data = [
        ['Report ID',    f'HAI-{report_id:06d}', 'Date',         datetime.now().strftime('%B %d, %Y')],
        ['Patient Name', patient_info.get('name', 'N/A'), 'Age', str(patient_info.get('age', 'N/A'))],
        ['Gender',       patient_info.get('gender', 'N/A'), 'Generated By', 'Healthy AI System'],
    ]
    meta_table = Table(meta_data, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,-1), colors.HexColor('#f9f0ff')),
        ('TEXTCOLOR',      (0,0), (-1,-1), colors.HexColor('#333')),
        ('FONTNAME',       (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',       (0,0), (-1,-1), 9),
        ('GRID',           (0,0), (-1,-1), 0.5, colors.HexColor('#ddd')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#f9f0ff'), colors.white]),
        ('FONTNAME',       (0,0), (0,-1),  'Helvetica-Bold'),
        ('FONTNAME',       (2,0), (2,-1),  'Helvetica-Bold'),
        ('VALIGN',         (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING',        (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Prediction result
    story.append(HRFlowable(width='100%', thickness=1,
                             color=colors.HexColor('#eee'), spaceAfter=8))
    story.append(Paragraph("Prediction Result", section_style))
    result_data = [
        ['Diagnosis',   prediction],
        ['Risk Level',  risk_level],
        ['Probability', f'{probability*100:.1f}%'],
        ['Confidence',  'High' if abs(probability - 0.5) > 0.3 else 'Moderate'],
    ]
    result_table = Table(result_data, colWidths=[7*cm, 10*cm])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#7c3aed')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#f9f0ff')),
        ('TEXTCOLOR',  (0,0), (0,-1), colors.white),
        ('TEXTCOLOR',  (1,0), (1,-1), colors.HexColor('#333')),
        ('FONTNAME',   (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#ddd')),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING',    (0,0), (-1,-1), 8),
        ('TEXTCOLOR',  (1,1), (1,1),   colors.HexColor(risk_color)),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 12))

    # Input parameters
    story.append(HRFlowable(width='100%', thickness=1,
                             color=colors.HexColor('#eee'), spaceAfter=8))
    story.append(Paragraph("Input Parameters", section_style))
    param_rows = [['Parameter', 'Value']]
    for k, v in input_data.items():
        param_rows.append([k.replace('_', ' ').title(), str(v)])
    param_table = Table(param_rows, colWidths=[8*cm, 9*cm])
    param_table.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,0),  colors.HexColor('#7c3aed')),
        ('TEXTCOLOR',      (0,0), (-1,0),  colors.white),
        ('FONTNAME',       (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTNAME',       (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',       (0,0), (-1,-1), 9),
        ('GRID',           (0,0), (-1,-1), 0.5, colors.HexColor('#ddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f0ff')]),
        ('VALIGN',         (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING',        (0,0), (-1,-1), 6),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 12))

    # Recommendations
    story.append(HRFlowable(width='100%', thickness=1,
                             color=colors.HexColor('#eee'), spaceAfter=8))
    story.append(Paragraph("Medical Recommendations", section_style))
    if report_type == 'heart':
        if risk_level == 'High Risk':
            recs = ["Immediately consult a cardiologist.",
                    "Monitor blood pressure daily.",
                    "Avoid smoking and alcohol consumption.",
                    "Follow a heart-healthy low-sodium diet.",
                    "Engage in light supervised exercise only.",
                    "Take prescribed medications regularly."]
        elif risk_level == 'Moderate Risk':
            recs = ["Schedule a cardiac check-up within 1 month.",
                    "Maintain healthy cholesterol levels.",
                    "Exercise 30 minutes daily (walking/yoga).",
                    "Reduce stress with meditation.",
                    "Monitor glucose and blood pressure weekly."]
        else:
            recs = ["Continue healthy lifestyle habits.",
                    "Annual cardiac screening recommended.",
                    "Maintain BMI within healthy range (18.5-24.9).",
                    "Exercise regularly and eat a balanced diet."]
    else:
        if risk_level == 'High Risk':
            recs = ["Consult an endocrinologist immediately.",
                    "Monitor blood glucose daily.",
                    "Follow a strict low-glycemic diet.",
                    "Avoid sugary beverages and processed foods.",
                    "Take prescribed medications as directed.",
                    "Exercise 150+ minutes per week (supervised)."]
        elif risk_level == 'Moderate Risk':
            recs = ["Get HbA1c tested within 2 weeks.",
                    "Reduce carbohydrate intake.",
                    "Exercise 30-45 minutes daily.",
                    "Maintain healthy body weight.",
                    "Monitor blood sugar weekly."]
        else:
            recs = ["Maintain healthy diet and exercise.",
                    "Annual diabetes screening recommended.",
                    "Keep BMI in healthy range.",
                    "Limit sugar and refined carbohydrates."]
    for i, rec in enumerate(recs, 1):
        story.append(Paragraph(f"  {i}. {rec}", normal_style))
    story.append(Spacer(1, 16))

    # Disclaimer
    story.append(HRFlowable(width='100%', thickness=1,
                             color=colors.HexColor('#eee'), spaceAfter=8))
    story.append(Paragraph(
        "⚠️ DISCLAIMER: This report is generated by an AI system and is for informational "
        "purposes only. It does not constitute medical advice. Please consult a qualified "
        "healthcare professional for proper diagnosis and treatment.",
        disclaimer_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Generated by Healthy AI | © 2026 Healthy AI", disclaimer_style))

    doc.build(story)
    return filename

# ─── Routes ────────────────────────────────────────────────

@app.route('/')
def index():
    user = None
    if logged_in():
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE id=?',
                              (session['user_id'],)).fetchone()
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        d = request.get_json()
        email, password = d.get('email'), d.get('password')
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE email=? AND password=?',
                              (email, hash_pw(password))).fetchone()
        if user:
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            return jsonify({'success': True, 'name': user['name']})
        return jsonify({'success': False, 'msg': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        d = request.get_json()
        name, email, password = d.get('name'), d.get('email'), d.get('password')
        try:
            with get_db() as db:
                db.execute('INSERT INTO users (name, email, password) VALUES (?,?,?)',
                           (name, email, hash_pw(password)))
                db.commit()
                user = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            return jsonify({'success': True, 'name': name})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'msg': 'Email already registered'})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not logged_in():
        return redirect(url_for('index'))
    with get_db() as db:
        user    = db.execute('SELECT * FROM users WHERE id=?',
                             (session['user_id'],)).fetchone()
        reports = db.execute(
            'SELECT * FROM reports WHERE user_id=? ORDER BY created_at DESC LIMIT 20',
            (session['user_id'],)).fetchall()
    return render_template('dashboard.html', user=user, reports=reports,
                           heart_meta=heart_meta, diabetes_meta=diabetes_meta)

@app.route('/predict/heart', methods=['GET','POST'])
def predict_heart():
    if not logged_in(): return redirect(url_for('index'))
    if request.method == 'POST':
        d = request.get_json()
        patient = {
            'name':   d.get('patient_name', 'Patient'),
            'age':    d.get('age', 0),
            'gender': 'Male' if int(d.get('male', 0)) == 1 else 'Female'
        }
        features = [
            int(d['male']), int(d['age']),
            int(d['currentSmoker']), float(d['cigsPerDay']),
            int(d['BPMeds']), int(d['prevalentStroke']), int(d['prevalentHyp']),
            int(d['diabetes']), float(d['totChol']), float(d['sysBP']),
            float(d['diaBP']), float(d['BMI']), float(d['heartRate']), float(d['glucose'])
        ]
        X    = np.array(features).reshape(1, -1)
        X_sc = heart_scaler.transform(X)
        prob = heart_model.predict_proba(X_sc)[0][1]
        pred = int(prob >= 0.5)
        if prob < 0.3:   risk = 'Low Risk'
        elif prob < 0.6: risk = 'Moderate Risk'
        else:            risk = 'High Risk'
        prediction_text = 'Heart Disease Risk Detected' if pred else 'No Significant Heart Disease Risk'
        input_data = {k: v for k, v in d.items() if k != 'patient_name'}
        with get_db() as db:
            cursor = db.execute(
                '''INSERT INTO reports (user_id, report_type, patient_name, patient_age,
                   patient_gender, input_data, prediction, probability, risk_level)
                   VALUES (?,?,?,?,?,?,?,?,?)''',
                (session['user_id'], 'heart', patient['name'], patient['age'],
                 patient['gender'], json.dumps(input_data), prediction_text, prob, risk))
            db.commit()
            report_id = cursor.lastrowid
        display_data = {
            'Gender':            patient['gender'],
            'Age':               d['age'],
            'Smoker':            'Yes' if d['currentSmoker'] == '1' else 'No',
            'Cigs/Day':          d['cigsPerDay'],
            'BP Meds':           'Yes' if d['BPMeds'] == '1' else 'No',
            'Total Cholesterol': d['totChol'],
            'Systolic BP':       d['sysBP'],
            'Diastolic BP':      d['diaBP'],
            'BMI':               d['BMI'],
            'Heart Rate':        d['heartRate'],
            'Glucose':           d['glucose'],
            'Hypertension':      'Yes' if d['prevalentHyp'] == '1' else 'No',
        }
        pdf_file = generate_pdf_report('heart', patient, display_data,
                                        prediction_text, prob, risk, report_id)
        with get_db() as db:
            db.execute('UPDATE reports SET report_file=? WHERE id=?', (pdf_file, report_id))
            db.commit()
        gauge = gauge_chart(prob, risk)
        return jsonify({
            'success': True, 'prediction': prediction_text,
            'probability': round(prob*100, 1), 'risk_level': risk,
            'gauge_chart': gauge, 'report_id': report_id, 'pdf_file': pdf_file
        })
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('predict_heart.html', user=user, meta=heart_meta)

@app.route('/predict/diabetes', methods=['GET','POST'])
def predict_diabetes():
    if not logged_in(): return redirect(url_for('index'))
    if request.method == 'POST':
        d           = request.get_json()
        gender_str  = d.get('gender', 'Male')
        smoking_str = d.get('smoking_history', 'never')
        try:
            gender_enc = diabetes_le_gender.transform([gender_str])[0]
        except:
            gender_enc = 0
        try:
            smoking_enc = diabetes_le_smoke.transform([smoking_str])[0]
        except:
            smoking_enc = 0
        features = [
            gender_enc, float(d['age']), int(d['hypertension']),
            int(d['heart_disease']), smoking_enc,
            float(d['bmi']), float(d['HbA1c_level']), float(d['blood_glucose_level'])
        ]
        X    = np.array(features).reshape(1, -1)
        X_sc = diabetes_scaler.transform(X)
        prob = diabetes_model.predict_proba(X_sc)[0][1]
        pred = int(prob >= 0.5)
        if prob < 0.3:   risk = 'Low Risk'
        elif prob < 0.6: risk = 'Moderate Risk'
        else:            risk = 'High Risk'
        prediction_text = 'Diabetes Risk Detected' if pred else 'No Significant Diabetes Risk'
        patient    = {'name': d.get('patient_name', 'Patient'),
                      'age': d['age'], 'gender': gender_str}
        input_data = {k: v for k, v in d.items() if k != 'patient_name'}
        with get_db() as db:
            cursor = db.execute(
                '''INSERT INTO reports (user_id, report_type, patient_name, patient_age,
                   patient_gender, input_data, prediction, probability, risk_level)
                   VALUES (?,?,?,?,?,?,?,?,?)''',
                (session['user_id'], 'diabetes', patient['name'], patient['age'],
                 patient['gender'], json.dumps(input_data), prediction_text, prob, risk))
            db.commit()
            report_id = cursor.lastrowid
        display_data = {
            'Gender':                gender_str,
            'Age':                   d['age'],
            'Hypertension':          'Yes' if d['hypertension'] == '1' else 'No',
            'Heart Disease History': 'Yes' if d['heart_disease'] == '1' else 'No',
            'Smoking History':       smoking_str,
            'BMI':                   d['bmi'],
            'HbA1c Level':           d['HbA1c_level'],
            'Blood Glucose Level':   d['blood_glucose_level'],
        }
        pdf_file = generate_pdf_report('diabetes', patient, display_data,
                                        prediction_text, prob, risk, report_id)
        with get_db() as db:
            db.execute('UPDATE reports SET report_file=? WHERE id=?', (pdf_file, report_id))
            db.commit()
        gauge = gauge_chart(prob, risk)
        return jsonify({
            'success': True, 'prediction': prediction_text,
            'probability': round(prob*100, 1), 'risk_level': risk,
            'gauge_chart': gauge, 'report_id': report_id, 'pdf_file': pdf_file
        })
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('predict_diabetes.html', user=user, meta=diabetes_meta)

@app.route('/eda/<model_type>')
def eda(model_type):
    if not logged_in(): return redirect(url_for('index'))
    charts = get_eda_charts(model_type)
    meta   = heart_meta if model_type == 'heart' else diabetes_meta
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('eda.html', user=user, charts=charts, meta=meta, model_type=model_type)

@app.route('/reports')
def reports():
    if not logged_in(): return redirect(url_for('index'))
    with get_db() as db:
        user        = db.execute('SELECT * FROM users WHERE id=?',
                                 (session['user_id'],)).fetchone()
        all_reports = db.execute(
            'SELECT * FROM reports WHERE user_id=? ORDER BY created_at DESC',
            (session['user_id'],)).fetchall()
    return render_template('reports.html', user=user, reports=all_reports)

@app.route('/download/<filename>')
def download_report(filename):
    if not logged_in(): return redirect(url_for('index'))
    filepath = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

@app.route('/api/stats')
def api_stats():
    if not logged_in(): return jsonify({'error': 'unauthorized'})
    with get_db() as db:
        total          = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=?",
                                    (session['user_id'],)).fetchone()['c']
        heart_count    = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=? AND report_type='heart'",
                                    (session['user_id'],)).fetchone()['c']
        diabetes_count = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=? AND report_type='diabetes'",
                                    (session['user_id'],)).fetchone()['c']
        high_risk      = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=? AND risk_level='High Risk'",
                                    (session['user_id'],)).fetchone()['c']
    return jsonify({'total': total, 'heart': heart_count,
                    'diabetes': diabetes_count, 'high_risk': high_risk})

@app.route('/terms')
def terms():
    user = None
    if logged_in():
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE id=?',
                              (session['user_id'],)).fetchone()
    return render_template('terms.html', user=user)

@app.route('/privacy')
def privacy():
    user = None
    if logged_in():
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE id=?',
                              (session['user_id'],)).fetchone()
    return render_template('privacy.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
