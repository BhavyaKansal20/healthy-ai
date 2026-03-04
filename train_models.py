"""
Train and save ML models for Heart Disease & Diabetes prediction
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import joblib
import json
import os
import warnings
warnings.filterwarnings('ignore')

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data_files')
os.makedirs(MODELS_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# HEART DISEASE
# ─────────────────────────────────────────────
def train_heart():
    df = pd.read_csv(os.path.join(DATA_DIR, 'heart.csv'))
    df.columns = df.columns.str.strip()
    df.dropna(inplace=True)
    
    # Encode male column
    df['male'] = df['male'].astype(int)
    
    features = ['male','age','currentSmoker','cigsPerDay',
                 'BPMeds','prevalentStroke','prevalentHyp','diabetes',
                 'totChol','sysBP','diaBP','BMI','heartRate','glucose']
    target = 'TenYearCHD'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)
    
    model = GradientBoostingClassifier(n_estimators=200, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X_train_sc, y_train)
    
    y_pred = model.predict(X_test_sc)
    acc = accuracy_score(y_test, y_pred)
    roc = roc_auc_score(y_test, model.predict_proba(X_test_sc)[:,1])
    
    print(f"Heart Model Accuracy: {acc:.4f}, ROC-AUC: {roc:.4f}")
    
    # Feature importance
    fi = dict(zip(features, model.feature_importances_.tolist()))
    
    # Class distribution
    class_dist = y.value_counts().to_dict()
    
    # Correlation data for EDA
    corr = df[features + [target]].corr()[target].drop(target).to_dict()
    
    meta = {
        'accuracy': round(acc * 100, 2),
        'roc_auc': round(roc * 100, 2),
        'feature_importance': fi,
        'class_distribution': {str(k): int(v) for k, v in class_dist.items()},
        'correlation': {k: round(v, 4) for k, v in corr.items()},
        'features': features,
        'n_samples': len(df),
        'report': classification_report(y_test, y_pred, output_dict=True)
    }
    
    joblib.dump(model, os.path.join(MODELS_DIR, 'heart_model.pkl'))
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'heart_scaler.pkl'))
    with open(os.path.join(MODELS_DIR, 'heart_meta.json'), 'w') as f:
        json.dump(meta, f)
    
    print("Heart model saved.")
    return meta

# ─────────────────────────────────────────────
# DIABETES
# ─────────────────────────────────────────────
def train_diabetes():
    df = pd.read_csv(os.path.join(DATA_DIR, 'diabetes.csv'))
    df.columns = df.columns.str.strip()
    df.dropna(inplace=True)
    
    # Encode categorical
    le_gender = LabelEncoder()
    df['gender_enc'] = le_gender.fit_transform(df['gender'])
    
    le_smoke = LabelEncoder()
    df['smoking_enc'] = le_smoke.fit_transform(df['smoking_history'])
    
    features = ['gender_enc','age','hypertension','heart_disease',
                 'smoking_enc','bmi','HbA1c_level','blood_glucose_level']
    target = 'diabetes'
    
    # Sample for speed
    df_sample = df.sample(n=min(20000, len(df)), random_state=42)
    
    X = df_sample[features]
    y = df_sample[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)
    
    model = GradientBoostingClassifier(n_estimators=150, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X_train_sc, y_train)
    
    y_pred = model.predict(X_test_sc)
    acc = accuracy_score(y_test, y_pred)
    roc = roc_auc_score(y_test, model.predict_proba(X_test_sc)[:,1])
    
    print(f"Diabetes Model Accuracy: {acc:.4f}, ROC-AUC: {roc:.4f}")
    
    fi = dict(zip(features, model.feature_importances_.tolist()))
    class_dist = y.value_counts().to_dict()
    corr = df_sample[features + [target]].corr()[target].drop(target).to_dict()
    
    # Age distribution stats
    age_stats = df['age'].describe().to_dict()
    bmi_stats = df['bmi'].describe().to_dict()
    
    meta = {
        'accuracy': round(acc * 100, 2),
        'roc_auc': round(roc * 100, 2),
        'feature_importance': fi,
        'class_distribution': {str(k): int(v) for k, v in class_dist.items()},
        'correlation': {k: round(v, 4) for k, v in corr.items()},
        'features': features,
        'n_samples': len(df),
        'gender_classes': le_gender.classes_.tolist(),
        'smoking_classes': le_smoke.classes_.tolist(),
        'report': classification_report(y_test, y_pred, output_dict=True)
    }
    
    joblib.dump(model, os.path.join(MODELS_DIR, 'diabetes_model.pkl'))
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'diabetes_scaler.pkl'))
    joblib.dump(le_gender, os.path.join(MODELS_DIR, 'diabetes_le_gender.pkl'))
    joblib.dump(le_smoke, os.path.join(MODELS_DIR, 'diabetes_le_smoke.pkl'))
    with open(os.path.join(MODELS_DIR, 'diabetes_meta.json'), 'w') as f:
        json.dump(meta, f)
    
    print("Diabetes model saved.")
    return meta

if __name__ == '__main__':
    print("Training Heart Disease model...")
    train_heart()
    print("Training Diabetes model...")
    train_diabetes()
    print("All models trained and saved!")
