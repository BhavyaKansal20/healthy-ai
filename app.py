"""
Healthy AI - Flask Web Application
Heart Disease & Diabetes Prediction Platform
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from reportlab.platypus import Image
import sqlite3, hashlib, json, os, io, base64, re
import threading
from datetime import datetime
import joblib, numpy as np
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import warnings
warnings.filterwarnings('ignore')

plt = None


def _ensure_matplotlib():
    global plt
    if plt is not None:
        return
    # Render containers may have read-only HOME; keep font cache in /tmp.
    os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as _plt
    plt = _plt

torch = None
nn = None
models = None
transforms = None
PILImage = None


def _ensure_torch_modules():
    global torch, nn, models, transforms, PILImage
    if torch is not None:
        return True
    try:
        import torch as _torch
        import torch.nn as _nn
        from torchvision import models as _models, transforms as _transforms
        from PIL import Image as _PILImage
        torch = _torch
        nn = _nn
        models = _models
        transforms = _transforms
        PILImage = _PILImage
        return True
    except Exception as e:
        print(f"Torch runtime unavailable: {e}")
        return False

app = Flask(__name__)
app.secret_key = 'healthyai_secret_2026_secure'

BASE        = os.path.dirname(__file__)
MODELS_DIR  = os.path.join(BASE, 'models')
REPORTS_DIR = os.path.join(BASE, 'static', 'reports')
UPLOADS_DIR = os.path.join(BASE, 'static', 'uploads')
DB_PATH     = os.path.join(BASE, 'healthyai.db')
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Google Apps Script URL — feedback Google Sheets mein jaata hai
GOOGLE_SHEET_URL = 'https://script.google.com/macros/s/AKfycbwavNMreUplQA7NAZj5_SAJd4Sigkk633zyPYk9PFf4B4v6k2JPVI9XFHyeLjyew2w3yQ/exec'

# Load or train models
def load_or_train_models():
    heart_pkl = os.path.join(MODELS_DIR, 'heart_model.pkl')
    diab_pkl  = os.path.join(MODELS_DIR, 'diabetes_model.pkl')
    brain_pt  = os.path.join(MODELS_DIR, 'brain_tumor_model.pt')
    need_train = not os.path.exists(heart_pkl) or not os.path.exists(diab_pkl)
    if not need_train:
        try:
            joblib.load(heart_pkl)
            joblib.load(diab_pkl)
        except Exception:
            need_train = True
            print("Models incompatible — retraining now...")
    if need_train:
        import train_models
        train_models.train_heart()
        train_models.train_diabetes()
        print("Models trained successfully.")

    # Brain model training is optional at startup (dataset may not exist in production).
    if not os.path.exists(brain_pt):
        try:
            import train_models
            train_models.train_brain()
            print("Brain model trained successfully.")
        except Exception as e:
            print(f"Brain model not available yet: {e}")

load_or_train_models()

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


brain_model = None
brain_meta = {
    'accuracy': 0,
    'roc_auc': 0,
    'n_samples': 0,
    'classes': ['glioma', 'meningioma', 'notumor', 'pituitary']
}
brain_classes = ['glioma', 'meningioma', 'notumor', 'pituitary']
brain_pt_path = os.path.join(MODELS_DIR, 'brain_tumor_model.pt')
brain_meta_path = os.path.join(MODELS_DIR, 'brain_tumor_meta.json')
brain_labels_path = os.path.join(MODELS_DIR, 'brain_tumor_labels.pkl')
brain_available = os.path.exists(brain_pt_path)
brain_device = None
brain_transform = None
brain_warming = False
brain_warm_error = None

if os.path.exists(brain_meta_path):
    try:
        with open(brain_meta_path) as f:
            brain_meta = json.load(f)
    except Exception as e:
        print(f"Failed to read brain meta: {e}")

if os.path.exists(brain_labels_path):
    try:
        brain_classes = joblib.load(brain_labels_path)
    except Exception as e:
        print(f"Failed to read brain labels: {e}")


def _ensure_brain_runtime_loaded():
    global brain_model, brain_transform, brain_device, brain_classes, brain_warming, brain_warm_error
    if brain_model is not None and brain_transform is not None and brain_device is not None:
        return True, None
    if not brain_available:
        return False, 'Brain tumor model is not available in models folder.'
    if not _ensure_torch_modules():
        return False, 'PyTorch runtime is unavailable in this deployment.'

    try:
        brain_warming = True
        class BrainTumorNet(nn.Module):
            def __init__(self, num_classes=4):
                super().__init__()
                self.backbone = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
                in_features = self.backbone.classifier[1].in_features
                self.backbone.classifier[1] = nn.Sequential(
                    nn.Dropout(p=0.30),
                    nn.Linear(in_features, num_classes)
                )

            def forward(self, x):
                return self.backbone(x)

        brain_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        ckpt = torch.load(brain_pt_path, map_location=brain_device)
        classes = ckpt.get('classes', None)
        if classes:
            brain_classes = classes
        elif os.path.exists(brain_labels_path):
            brain_classes = joblib.load(brain_labels_path)

        brain_model = BrainTumorNet(num_classes=len(brain_classes)).to(brain_device)
        brain_model.load_state_dict(ckpt['state_dict'])
        brain_model.eval()

        # Keep CPU inference predictable on small instances.
        try:
            if brain_device.type == 'cpu':
                torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
        except Exception:
            pass

        brain_transform = 'manual'

        # One-time warmup to avoid first-user latency spike.
        with torch.inference_mode():
            dummy = torch.zeros((1, 3, 224, 224), device=brain_device)
            _ = brain_model(dummy)
        brain_warm_error = None
        brain_warming = False
        return True, None
    except Exception as e:
        print(f"Failed to initialize brain runtime: {e}")
        brain_warm_error = str(e)
        brain_warming = False
        return False, 'Brain model failed to initialize at runtime.'


def _pil_to_brain_tensor(image):
    # Fully manual conversion to avoid numpy/torchvision dtype edge-cases on hosted runtimes.
    image = image.resize((224, 224)).convert('RGB')
    px = list(image.getdata())
    x = torch.tensor(px, dtype=torch.float32).view(224, 224, 3).permute(2, 0, 1)
    x = x / 255.0
    mean = torch.tensor([0.485, 0.456, 0.406], dtype=torch.float32).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225], dtype=torch.float32).view(3, 1, 1)
    x = (x - mean) / std
    return x.unsqueeze(0)


def _start_brain_warmup_async():
    if not brain_available:
        return

    def _warm():
        _ensure_brain_runtime_loaded()

    t = threading.Thread(target=_warm, daemon=True)
    t.start()


_start_brain_warmup_async()

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

def fig_to_b64(fig):
    _ensure_matplotlib()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True, dpi=110)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return b64

PALETTE = ['#00d4ff', '#7c3aed', '#06d6a0', '#ff6b6b', '#ffd166', '#118ab2']

def chart_feature_importance(meta, title):
    _ensure_matplotlib()
    fi = meta['feature_importance']
    labels = list(fi.keys())
    vals = list(fi.values())
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    labels = [labels[i] for i in order]
    vals = [vals[i] for i in order]
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
    _ensure_matplotlib()
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
    _ensure_matplotlib()
    corr = meta['correlation']
    labels = list(corr.keys())
    vals = list(corr.values())
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

def get_eda_charts(model_type):
    _ensure_matplotlib()
    import pandas as pd
    if model_type == 'heart':
        df = pd.read_csv(os.path.join(BASE, 'data_files', 'heart.csv'))
        df.columns = df.columns.str.strip()
        meta = heart_meta
        fi_chart   = chart_feature_importance(meta, 'Heart Disease')
        dist_chart = chart_class_dist(meta, {'0': 'No CHD', '1': 'CHD Risk'}, 'Heart Disease')
        corr_chart = chart_correlation(meta, 'Heart Disease')
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_alpha(0)
        ax.set_facecolor((0,0,0,0))
        for target_val, color, lbl in [(0, PALETTE[0], 'No CHD'), (1, PALETTE[3], 'CHD')]:
            ax.hist(df[df['TenYearCHD']==target_val]['age'].dropna(), bins=20,
                    alpha=0.6, color=color, label=lbl)
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
        meta = diabetes_meta
        fi_chart   = chart_feature_importance(meta, 'Diabetes')
        dist_chart = chart_class_dist(meta, {'0': 'No Diabetes', '1': 'Diabetes'}, 'Diabetes')
        corr_chart = chart_correlation(meta, 'Diabetes')
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_alpha(0)
        ax.set_facecolor((0,0,0,0))
        for target_val, color, lbl in [(0, PALETTE[0], 'No Diabetes'), (1, PALETTE[3], 'Diabetes')]:
            ax.hist(df[df['diabetes']==target_val]['bmi'].dropna(), bins=25,
                    alpha=0.6, color=color, label=lbl)
        ax.set_xlabel('BMI', color='white')
        ax.set_ylabel('Count', color='white')
        ax.set_title('BMI Distribution by Outcome', color='white', fontsize=11)
        ax.tick_params(colors='white')
        ax.legend(labelcolor='white', facecolor='#0a0a1a')
        for sp in ax.spines.values(): sp.set_edgecolor('#ffffff30')
        bmi_chart = fig_to_b64(fig)
        return {'fi': fi_chart, 'dist': dist_chart, 'corr': corr_chart, 'age': bmi_chart}

def gauge_chart(probability, risk_level):
    _ensure_matplotlib()
    fig, ax = plt.subplots(figsize=(5, 3), subplot_kw={'projection': 'polar'})
    fig.patch.set_alpha(0)
    ax.set_facecolor((0,0,0,0))
    for t_start, t_end, col in [(np.pi, np.pi*2/3, '#06d6a0'),
                                 (np.pi*2/3, np.pi/3, '#ffd166'),
                                 (np.pi/3, 0, '#ff6b6b')]:
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
            color={'Low Risk': '#06d6a0', 'Moderate Risk': '#ffd166', 'High Risk': '#ff6b6b'}.get(risk_level, 'white'),
            fontsize=10, transform=ax.transData)
    return fig_to_b64(fig)

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
    risk_color = {'Low Risk': '#06d6a0', 'Moderate Risk': '#f59e0b', 'High Risk': '#ef4444'}.get(risk_level, '#555')
    logo_path = os.path.join(BASE, 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=60, height=60)
        logo.hAlign = 'CENTER'
        story.append(logo)
    story.append(Paragraph("Healthy AI", title_style))
    story.append(Paragraph("Advanced Health Prediction Report", subtitle_style))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#7c3aed'), spaceAfter=12))
    type_label = {
        'heart': 'Heart Disease Prediction',
        'diabetes': 'Diabetes Prediction',
        'brain': 'Brain Tumor MRI Prediction'
    }.get(report_type, 'Health Prediction')
    story.append(Paragraph(f"Report Type: {type_label}", section_style))
    meta_data = [
        ['Report ID', f'HAI-{report_id:06d}', 'Date', datetime.now().strftime('%B %d, %Y')],
        ['Patient Name', patient_info.get('name', 'N/A'), 'Age', str(patient_info.get('age', 'N/A'))],
        ['Gender', patient_info.get('gender', 'N/A'), 'Generated By', 'Healthy AI System'],
    ]
    meta_table = Table(meta_data, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9f0ff')),
        ('TEXTCOLOR',  (0,0), (-1,-1), colors.HexColor('#333')),
        ('FONTNAME',   (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#ddd')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#f9f0ff'), colors.white]),
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',   (2,0), (2,-1), 'Helvetica-Bold'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING',    (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#eee'), spaceAfter=8))
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
        ('TEXTCOLOR',  (1,1), (1,1), colors.HexColor(risk_color)),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#eee'), spaceAfter=8))
    story.append(Paragraph("Input Parameters", section_style))
    param_rows = [['Parameter', 'Value']]
    for k, v in input_data.items():
        param_rows.append([k.replace('_', ' ').title(), str(v)])
    param_table = Table(param_rows, colWidths=[8*cm, 9*cm])
    param_table.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,0), colors.HexColor('#7c3aed')),
        ('TEXTCOLOR',      (0,0), (-1,0), colors.white),
        ('FONTNAME',       (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',       (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',       (0,0), (-1,-1), 9),
        ('GRID',           (0,0), (-1,-1), 0.5, colors.HexColor('#ddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f0ff')]),
        ('VALIGN',         (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING',        (0,0), (-1,-1), 6),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#eee'), spaceAfter=8))
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
    elif report_type == 'diabetes':
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
    else:
        if risk_level == 'High Risk':
            recs = ["Consult a neurologist immediately.",
                    "Get MRI reviewed by a radiologist.",
                    "Avoid self-medication and seek urgent clinical evaluation.",
                    "Follow emergency care advice for severe neurological symptoms.",
                    "Keep all imaging and reports available for specialist review."]
        elif risk_level == 'Moderate Risk':
            recs = ["Schedule specialist consultation within a week.",
                    "Repeat MRI scan if clinically advised.",
                    "Track symptoms such as headache, vision changes or seizures.",
                    "Follow physician guidance for further tests."]
        else:
            recs = ["No significant tumor pattern detected by AI model.",
                    "Continue regular preventive health checkups.",
                    "Consult a doctor if neurological symptoms persist."]
    for i, rec in enumerate(recs, 1):
        story.append(Paragraph(f"  {i}. {rec}", normal_style))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#eee'), spaceAfter=8))
    story.append(Paragraph(
        "DISCLAIMER: This report is generated by an AI system and is for informational purposes only. "
        "It does not constitute medical advice. Please consult a qualified healthcare professional "
        "for proper diagnosis and treatment.",
        disclaimer_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Generated by Healthy AI | 2026 Healthy AI", disclaimer_style))
    doc.build(story)
    return filename

@app.route('/')
def index():
    user = None
    if logged_in():
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
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
        user    = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
        reports = db.execute('SELECT * FROM reports WHERE user_id=? ORDER BY created_at DESC LIMIT 20',
                             (session['user_id'],)).fetchall()
    return render_template('dashboard.html', user=user, reports=reports,
                           heart_meta=heart_meta, diabetes_meta=diabetes_meta,
                           brain_meta=brain_meta, brain_available=brain_available)

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
                '''INSERT INTO reports (user_id, report_type, patient_name, patient_age, patient_gender,
                   input_data, prediction, probability, risk_level)
                   VALUES (?,?,?,?,?,?,?,?,?)''',
                (session['user_id'], 'heart', patient['name'], patient['age'], patient['gender'],
                 json.dumps(input_data), prediction_text, prob, risk))
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
        pdf_file = generate_pdf_report('heart', patient, display_data, prediction_text, prob, risk, report_id)
        with get_db() as db:
            db.execute('UPDATE reports SET report_file=? WHERE id=?', (pdf_file, report_id))
            db.commit()
        gauge = gauge_chart(prob, risk)
        return jsonify({
            'success': True, 'prediction': prediction_text, 'probability': round(prob*100, 1),
            'risk_level': risk, 'gauge_chart': gauge, 'report_id': report_id, 'pdf_file': pdf_file
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
        patient    = {'name': d.get('patient_name', 'Patient'), 'age': d['age'], 'gender': gender_str}
        input_data = {k: v for k, v in d.items() if k != 'patient_name'}
        with get_db() as db:
            cursor = db.execute(
                '''INSERT INTO reports (user_id, report_type, patient_name, patient_age, patient_gender,
                   input_data, prediction, probability, risk_level)
                   VALUES (?,?,?,?,?,?,?,?,?)''',
                (session['user_id'], 'diabetes', patient['name'], patient['age'], patient['gender'],
                 json.dumps(input_data), prediction_text, prob, risk))
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
        pdf_file = generate_pdf_report('diabetes', patient, display_data, prediction_text, prob, risk, report_id)
        with get_db() as db:
            db.execute('UPDATE reports SET report_file=? WHERE id=?', (pdf_file, report_id))
            db.commit()
        gauge = gauge_chart(prob, risk)
        return jsonify({
            'success': True, 'prediction': prediction_text, 'probability': round(prob*100, 1),
            'risk_level': risk, 'gauge_chart': gauge, 'report_id': report_id, 'pdf_file': pdf_file
        })
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('predict_diabetes.html', user=user, meta=diabetes_meta)


@app.route('/predict/brain', methods=['GET', 'POST'])
def predict_brain():
    if not logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            if brain_warming and brain_model is None:
                return jsonify({'success': False, 'msg': 'Brain model is warming up. Please retry in 20-30 seconds.'}), 503

            ok, err = _ensure_brain_runtime_loaded()
            if not ok:
                return jsonify({'success': False, 'msg': err}), 503

            file = request.files.get('mri_image')
            if file is None or file.filename == '':
                return jsonify({'success': False, 'msg': 'Please upload an MRI image.'}), 400

            filename = secure_filename(file.filename)
            save_name = f"brain_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            save_path = os.path.join(UPLOADS_DIR, save_name)
            file.save(save_path)

            image = PILImage.open(save_path).convert('RGB')
            x = _pil_to_brain_tensor(image).to(brain_device)

            with torch.inference_mode():
                logits = brain_model(x)
                probs = torch.softmax(logits, dim=1)[0].detach().cpu().tolist()

            pred_idx = max(range(len(probs)), key=lambda i: probs[i])
            pred_class = brain_classes[pred_idx] if pred_idx < len(brain_classes) else 'unknown'
            confidence = float(probs[pred_idx])
            no_tumor_aliases = {'notumor', 'no_tumor', 'no-tumor', 'not tumor'}
            tumor_prob = 1.0 - confidence if pred_class.lower().replace(' ', '') in no_tumor_aliases else confidence

            if tumor_prob < 0.3:
                risk = 'Low Risk'
            elif tumor_prob < 0.6:
                risk = 'Moderate Risk'
            else:
                risk = 'High Risk'

            nice_class = {
                'glioma': 'Glioma',
                'meningioma': 'Meningioma',
                'pituitary': 'Pituitary Tumor',
                'notumor': 'No Tumor',
                'no_tumor': 'No Tumor'
            }.get(pred_class.lower(), pred_class.replace('_', ' ').title())

            prediction_text = 'No Significant Brain Tumor Pattern Detected' if nice_class == 'No Tumor' else f'{nice_class} Pattern Detected'

            patient = {
                'name': request.form.get('patient_name', 'Patient'),
                'age': request.form.get('age', 'N/A'),
                'gender': request.form.get('gender', 'N/A')
            }

            input_data = {
                'mri_file': filename,
                'predicted_class': nice_class,
                'model_confidence': f"{confidence * 100:.2f}%"
            }

            with get_db() as db:
                cursor = db.execute(
                    '''INSERT INTO reports (user_id, report_type, patient_name, patient_age, patient_gender,
                       input_data, prediction, probability, risk_level)
                       VALUES (?,?,?,?,?,?,?,?,?)''',
                    (session['user_id'], 'brain', patient['name'], patient['age'], patient['gender'],
                     json.dumps(input_data), prediction_text, tumor_prob, risk)
                )
                db.commit()
                report_id = cursor.lastrowid

            display_data = {
                'Gender': patient['gender'],
                'Age': patient['age'],
                'MRI Filename': filename,
                'Predicted Class': nice_class,
                'Model Confidence': f"{confidence * 100:.1f}%"
            }
            pdf_file = generate_pdf_report('brain', patient, display_data, prediction_text, tumor_prob, risk, report_id)

            with get_db() as db:
                db.execute('UPDATE reports SET report_file=? WHERE id=?', (pdf_file, report_id))
                db.commit()

            gauge = gauge_chart(tumor_prob, risk)
            return jsonify({
                'success': True,
                'prediction': prediction_text,
                'probability': round(tumor_prob * 100, 1),
                'confidence': round(confidence * 100, 1),
                'predicted_class': nice_class,
                'risk_level': risk,
                'gauge_chart': gauge,
                'report_id': report_id,
                'pdf_file': pdf_file
            })
        except Exception as e:
            print(f"Brain prediction error: {e}")
            return jsonify({'success': False, 'msg': f'Prediction error: {str(e)}'}), 500

    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('predict_brain.html', user=user, meta=brain_meta, brain_available=brain_available)

@app.route('/eda/<model_type>')
def eda(model_type):
    if not logged_in(): return redirect(url_for('index'))
    if model_type not in ('heart', 'diabetes'):
        return redirect(url_for('dashboard'))
    charts = get_eda_charts(model_type)
    meta   = heart_meta if model_type == 'heart' else diabetes_meta
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('eda.html', user=user, charts=charts, meta=meta, model_type=model_type)

@app.route('/reports')
def reports():
    if not logged_in(): return redirect(url_for('index'))
    with get_db() as db:
        user        = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
        all_reports = db.execute('SELECT * FROM reports WHERE user_id=? ORDER BY created_at DESC',
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
        total          = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=?", (session['user_id'],)).fetchone()['c']
        heart_count    = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=? AND report_type='heart'", (session['user_id'],)).fetchone()['c']
        diabetes_count = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=? AND report_type='diabetes'", (session['user_id'],)).fetchone()['c']
        brain_count    = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=? AND report_type='brain'", (session['user_id'],)).fetchone()['c']
        high_risk      = db.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=? AND risk_level='High Risk'", (session['user_id'],)).fetchone()['c']
    return jsonify({'total': total, 'heart': heart_count, 'diabetes': diabetes_count, 'brain': brain_count, 'high_risk': high_risk})

@app.route('/terms')
def terms():
    user = None
    if logged_in():
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('terms.html', user=user)

@app.route('/privacy')
def privacy():
    user = None
    if logged_in():
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('privacy.html', user=user)

# Feedback route — user ka data Google Sheets mein save karta hai
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    import requests as req_lib
    payload = {
        'name':            data.get('name', ''),
        'prediction_type': data.get('prediction_type', ''),
        'rating':          data.get('rating', ''),
        'helpful':         data.get('helpful', ''),
        'message':         data.get('message', ''),
        'get_reports':     data.get('get_reports', '')
    }
    try:
        req_lib.post(GOOGLE_SHEET_URL, json=payload, timeout=10)
        return jsonify({'success': True})
    except Exception as e:
        print(f'Feedback error: {e}')
        return jsonify({'success': False, 'error': str(e)})

# Admin Panel
@app.route('/admin/Kansal0920Admin')
def admin_view():
    with get_db() as db:
        users   = db.execute('SELECT id, name, email, created_at FROM users').fetchall()
        reports = db.execute('''
            SELECT r.id, u.name as username, u.email, r.report_type,
                   r.patient_name, r.risk_level, r.probability, r.created_at
            FROM reports r
            JOIN users u ON r.user_id = u.id
            ORDER BY r.created_at DESC
        ''').fetchall()
    html = f'''<html><head><title>Healthy AI Admin</title>
    <style>
        body{{background:#0a0a1a;color:white;font-family:monospace;padding:30px}}
        h1{{color:#00d4ff;margin-bottom:5px}} h2{{color:#7c3aed;margin-top:40px}}
        .stats{{display:flex;gap:20px;margin:20px 0}}
        .stat{{background:#ffffff10;padding:15px 25px;border-radius:10px;text-align:center}}
        .stat h3{{color:#00d4ff;font-size:28px;margin:0}} .stat p{{margin:5px 0;color:#aaa}}
        table{{border-collapse:collapse;width:100%;margin-top:15px}}
        th{{background:#7c3aed;padding:10px 12px;text-align:left;font-size:13px}}
        td{{padding:8px 12px;border-bottom:1px solid #ffffff15;font-size:12px}}
        tr:hover{{background:#ffffff08}}
        .low{{color:#06d6a0}} .mod{{color:#ffd166}} .high{{color:#ff6b6b}}
    </style></head><body>
    <h1>Healthy AI Admin Panel</h1>
    <p style="color:#aaa">Secret admin view.</p>
    <div class="stats">
        <div class="stat"><h3>{len(users)}</h3><p>Total Users</p></div>
        <div class="stat"><h3>{len(reports)}</h3><p>Total Reports</p></div>
        <div class="stat"><h3>{sum(1 for r in reports if r["report_type"]=="heart")}</h3><p>Heart Reports</p></div>
        <div class="stat"><h3>{sum(1 for r in reports if r["report_type"]=="diabetes")}</h3><p>Diabetes Reports</p></div>
        <div class="stat"><h3>{sum(1 for r in reports if r["report_type"]=="brain")}</h3><p>Brain Reports</p></div>
        <div class="stat"><h3>{sum(1 for r in reports if r["risk_level"]=="High Risk")}</h3><p>High Risk Cases</p></div>
    </div>'''
    html += f'<h2>Users ({len(users)} total)</h2><table>'
    html += '<tr><th>#</th><th>Name</th><th>Email</th><th>Joined</th></tr>'
    for u in users:
        html += f'<tr><td>{u["id"]}</td><td>{u["name"]}</td><td>{u["email"]}</td><td>{u["created_at"]}</td></tr>'
    html += '</table>'
    html += f'<h2>Reports ({len(reports)} total)</h2><table>'
    html += '<tr><th>#</th><th>User</th><th>Email</th><th>Type</th><th>Patient</th><th>Risk</th><th>Probability</th><th>Date</th></tr>'
    for r in reports:
        risk_class = 'low' if r["risk_level"]=='Low Risk' else ('high' if r["risk_level"]=='High Risk' else 'mod')
        html += f'<tr><td>{r["id"]}</td><td>{r["username"]}</td><td>{r["email"]}</td><td>{r["report_type"].upper()}</td><td>{r["patient_name"]}</td><td class="{risk_class}">{r["risk_level"]}</td><td>{round(r["probability"]*100,1)}%</td><td>{r["created_at"]}</td></tr>'
    html += '</table></body></html>'
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)