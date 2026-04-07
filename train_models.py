"""
Train and save ML models for Heart Disease, Diabetes and Brain Tumor prediction.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import json
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader
    from torchvision import datasets, models, transforms
except Exception:
    torch = None
    nn = None
    DataLoader = None
    datasets = None
    models = None
    transforms = None

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data_files')
os.makedirs(MODELS_DIR, exist_ok=True)


if nn is not None and models is not None:
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
else:
    class BrainTumorNet:
        def __init__(self, *args, **kwargs):
            raise RuntimeError('PyTorch is required for brain tumor training.')

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


# ─────────────────────────────────────────────
# BRAIN TUMOR (MRI IMAGES)
# ─────────────────────────────────────────────
def _find_brain_dataset_root(data_root: Path):
    candidates = [
        data_root / 'brain_tumor_mri_dataset',
        data_root / 'brain_tumor_mri',
        data_root / 'brain_tumor',
        data_root,
    ]
    for c in candidates:
        if (c / 'Training').exists() and (c / 'Testing').exists():
            return c
    return None


def train_brain(epochs=6, batch_size=32, learning_rate=1e-3):
    if torch is None:
        raise RuntimeError('PyTorch/Torchvision not installed. Add torch and torchvision to requirements.')

    data_root = Path(DATA_DIR)
    dataset_root = _find_brain_dataset_root(data_root)
    if dataset_root is None:
        raise FileNotFoundError(
            'Brain MRI dataset not found. Expected folders: data_files/brain_tumor_mri_dataset/Training and Testing.'
        )

    train_dir = dataset_root / 'Training'
    test_dir = dataset_root / 'Testing'

    train_tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(8),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    eval_tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    train_ds = datasets.ImageFolder(train_dir, transform=train_tf)
    test_ds = datasets.ImageFolder(test_dir, transform=eval_tf)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=0)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = BrainTumorNet(num_classes=len(train_ds.classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    history = []
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            logits = model(x_batch)
            loss = criterion(logits, y_batch)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * x_batch.size(0)

        train_loss = running_loss / len(train_ds)

        model.eval()
        correct = 0
        total = 0
        all_probs = []
        all_true = []
        with torch.no_grad():
            for x_batch, y_batch in test_loader:
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                logits = model(x_batch)
                probs = torch.softmax(logits, dim=1)
                preds = torch.argmax(probs, dim=1)
                correct += (preds == y_batch).sum().item()
                total += y_batch.size(0)
                all_probs.append(probs.cpu().numpy())
                all_true.append(y_batch.cpu().numpy())

        val_acc = correct / max(total, 1)
        history.append({'epoch': epoch + 1, 'train_loss': float(train_loss), 'val_acc': float(val_acc)})
        print(f'Brain Epoch {epoch + 1}/{epochs} | loss={train_loss:.4f} | val_acc={val_acc:.4f}')

    y_true = np.concatenate(all_true)
    y_prob = np.concatenate(all_probs)
    y_pred = np.argmax(y_prob, axis=1)
    acc = accuracy_score(y_true, y_pred)
    try:
        roc = roc_auc_score(y_true, y_prob, multi_class='ovr')
    except Exception:
        roc = 0.0

    class_dist = {}
    for idx, cls in enumerate(train_ds.classes):
        class_dist[cls] = int(sum(sample[1] == idx for sample in train_ds.samples))

    meta = {
        'accuracy': round(acc * 100, 2),
        'roc_auc': round(roc * 100, 2),
        'n_samples': len(train_ds) + len(test_ds),
        'classes': train_ds.classes,
        'class_distribution': class_dist,
        'model_type': 'efficientnet_b0',
        'image_size': [224, 224],
        'history': history,
        'report': classification_report(y_true, y_pred, output_dict=True)
    }

    torch.save(
        {
            'state_dict': model.state_dict(),
            'classes': train_ds.classes,
            'image_size': [224, 224]
        },
        os.path.join(MODELS_DIR, 'brain_tumor_model.pt')
    )
    joblib.dump(train_ds.classes, os.path.join(MODELS_DIR, 'brain_tumor_labels.pkl'))
    with open(os.path.join(MODELS_DIR, 'brain_tumor_meta.json'), 'w') as f:
        json.dump(meta, f)

    print('Brain tumor model saved.')
    return meta

if __name__ == '__main__':
    print("Training Heart Disease model...")
    train_heart()
    print("\nTraining Diabetes model...")
    train_diabetes()
    print("\nTraining Brain Tumor model...")
    try:
        train_brain()
    except Exception as e:
        print(f"Brain model training skipped: {e}")
    print("\nAll models trained and saved!")
