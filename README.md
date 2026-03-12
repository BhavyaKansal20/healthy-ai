<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Healthy AI — README</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #04040f;
    --bg2: #08081a;
    --purple: #7c3aed;
    --cyan: #00d4ff;
    --green: #06d6a0;
    --red: #ff6b6b;
    --yellow: #ffd166;
    --glass: rgba(255,255,255,0.04);
    --border: rgba(255,255,255,0.08);
    --text: #e2e8f0;
    --muted: #64748b;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    line-height: 1.7;
    overflow-x: hidden;
  }

  /* ── Animated background ── */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
      radial-gradient(ellipse 80% 60% at 20% 10%, rgba(124,58,237,0.15) 0%, transparent 60%),
      radial-gradient(ellipse 60% 50% at 80% 90%, rgba(0,212,255,0.10) 0%, transparent 60%),
      radial-gradient(ellipse 40% 40% at 50% 50%, rgba(6,214,160,0.05) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
  }

  .wrap { max-width: 960px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }

  /* ── Hero ── */
  .hero {
    text-align: center;
    padding: 80px 24px 60px;
    position: relative;
  }

  .logo-wrap {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100px; height: 100px;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(0,212,255,0.2));
    border: 1px solid rgba(124,58,237,0.4);
    margin-bottom: 28px;
    box-shadow: 0 0 40px rgba(124,58,237,0.4), 0 0 80px rgba(124,58,237,0.15), inset 0 1px 0 rgba(255,255,255,0.1);
    animation: pulse-glow 3s ease-in-out infinite;
    font-size: 48px;
  }

  @keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 40px rgba(124,58,237,0.4), 0 0 80px rgba(124,58,237,0.15); }
    50%       { box-shadow: 0 0 60px rgba(124,58,237,0.7), 0 0 120px rgba(124,58,237,0.3), 0 0 160px rgba(0,212,255,0.1); }
  }

  .hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, var(--cyan) 50%, var(--purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 16px;
  }

  .hero-sub {
    font-size: 1.15rem;
    color: var(--muted);
    max-width: 560px;
    margin: 0 auto 36px;
  }

  .badges {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 48px;
  }

  .badge {
    padding: 6px 14px;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid;
    letter-spacing: 0.5px;
  }

  .badge-purple { background: rgba(124,58,237,0.15); border-color: rgba(124,58,237,0.4); color: #a78bfa; }
  .badge-cyan   { background: rgba(0,212,255,0.10);  border-color: rgba(0,212,255,0.3);  color: #67e8f9; }
  .badge-green  { background: rgba(6,214,160,0.10);  border-color: rgba(6,214,160,0.3);  color: #6ee7b7; }
  .badge-yellow { background: rgba(255,209,102,0.10);border-color: rgba(255,209,102,0.3);color: #fde68a; }

  /* ── Stats row ── */
  .stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 60px;
  }

  @media(max-width:640px) { .stats { grid-template-columns: repeat(2,1fr); } }

  .stat-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 16px;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
  }

  .stat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(124,58,237,0.4);
    box-shadow: 0 8px 32px rgba(124,58,237,0.2);
  }

  .stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--cyan), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .stat-label { font-size: 12px; color: var(--muted); margin-top: 4px; font-weight: 500; }

  /* ── Section title ── */
  .section { margin-bottom: 56px; }

  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: white;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, rgba(124,58,237,0.4), transparent);
  }

  /* ── Glass cards ── */
  .card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(12px);
    transition: border-color 0.3s, box-shadow 0.3s;
  }

  .card:hover {
    border-color: rgba(124,58,237,0.3);
    box-shadow: 0 4px 24px rgba(124,58,237,0.15);
  }

  /* ── Feature grid ── */
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }

  @media(max-width:640px) { .feature-grid { grid-template-columns: 1fr; } }

  .feature-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
  }

  .feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(to right, var(--purple), var(--cyan));
    opacity: 0;
    transition: opacity 0.3s;
  }

  .feature-card:hover::before { opacity: 1; }
  .feature-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(124,58,237,0.2);
    border-color: rgba(124,58,237,0.3);
  }

  .feat-icon { font-size: 28px; margin-bottom: 10px; }
  .feat-title { font-weight: 700; color: white; margin-bottom: 6px; font-size: 15px; }
  .feat-desc  { font-size: 13px; color: var(--muted); line-height: 1.5; }

  /* ── Route table ── */
  .route-table { width: 100%; border-collapse: collapse; }
  .route-table th {
    text-align: left;
    padding: 10px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid var(--border);
  }
  .route-table td {
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
    vertical-align: middle;
  }
  .route-table tr:hover td { background: rgba(255,255,255,0.02); }
  .route-path {
    font-family: 'JetBrains Mono', monospace;
    color: var(--cyan);
    font-size: 13px;
  }

  /* ── Model cards ── */
  .model-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  @media(max-width:580px) { .model-grid { grid-template-columns: 1fr; } }

  .model-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
  }

  .model-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(124,58,237,0.25);
    border-color: rgba(124,58,237,0.4);
  }

  .model-card::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 120px; height: 120px;
    border-radius: 50%;
    opacity: 0.06;
  }
  .model-card.heart::after { background: var(--red); }
  .model-card.diabetes::after { background: var(--cyan); }

  .model-type {
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .model-card.heart .model-type { color: var(--red); }
  .model-card.diabetes .model-type { color: var(--cyan); }

  .model-name { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 700; color: white; margin-bottom: 16px; }

  .model-stats { display: flex; gap: 12px; margin-bottom: 16px; }
  .ms {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 10px;
    text-align: center;
  }
  .ms-val { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800; }
  .ms-key { font-size: 10px; color: var(--muted); margin-top: 2px; font-family: 'JetBrains Mono', monospace; }
  .model-card.heart .ms-val   { color: var(--red); }
  .model-card.diabetes .ms-val { color: var(--cyan); }

  .model-tags { display: flex; flex-wrap: wrap; gap: 6px; }
  .tag {
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--muted);
  }

  /* ── Code block ── */
  .code-block {
    background: #0d0d1f;
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
    overflow-x: auto;
    position: relative;
  }

  .code-block::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(124,58,237,0.5), transparent);
  }

  .code-comment { color: #4a4a6a; }
  .code-cmd     { color: var(--cyan); }
  .code-string  { color: var(--green); }
  .code-num     { color: var(--yellow); }

  /* ── Tech stack ── */
  .tech-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; }
  @media(max-width:580px) { .tech-grid { grid-template-columns: repeat(2,1fr); } }

  .tech-item {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.3s;
  }

  .tech-item:hover {
    border-color: rgba(0,212,255,0.3);
    box-shadow: 0 4px 16px rgba(0,212,255,0.1);
    transform: translateX(3px);
  }

  .tech-icon { font-size: 20px; }
  .tech-name { font-weight: 600; font-size: 13px; color: white; }
  .tech-role { font-size: 11px; color: var(--muted); }

  /* ── Structure tree ── */
  .tree {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 2;
    padding: 20px 24px;
    background: #0d0d1f;
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 12px;
  }

  .tree-dir  { color: var(--cyan); font-weight: 600; }
  .tree-file { color: var(--muted); }
  .tree-comment { color: #4a4a6a; }
  .tree-special { color: var(--green); }

  /* ── Disclaimer ── */
  .disclaimer {
    background: rgba(255,107,107,0.08);
    border: 1px solid rgba(255,107,107,0.2);
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 13px;
    color: #fca5a5;
    display: flex;
    gap: 10px;
    align-items: flex-start;
    margin-bottom: 56px;
  }

  /* ── Footer ── */
  .footer {
    text-align: center;
    padding: 40px 24px 60px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 13px;
  }

  .footer-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--cyan), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }

  /* ── Divider ── */
  .divider {
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(124,58,237,0.3), transparent);
    margin: 48px 0;
  }

  /* ── Glow line ── */
  .glow-line {
    height: 3px;
    background: linear-gradient(to right, var(--purple), var(--cyan), var(--green));
    border-radius: 999px;
    box-shadow: 0 0 20px rgba(124,58,237,0.6), 0 0 40px rgba(0,212,255,0.3);
    margin-bottom: 0;
  }

  /* ── Feedback section ── */
  .feedback-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(0,212,255,0.05));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 16px;
    padding: 24px;
    position: relative;
    overflow: hidden;
  }
  .feedback-card::before {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(124,58,237,0.15), transparent);
    pointer-events: none;
  }

  /* ── Admin section ── */
  .admin-card {
    background: linear-gradient(135deg, rgba(255,209,102,0.07), rgba(255,107,107,0.05));
    border: 1px solid rgba(255,209,102,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .admin-icon { font-size: 36px; }
  .admin-title { font-weight: 700; color: var(--yellow); margin-bottom: 4px; }
  .admin-desc  { font-size: 13px; color: var(--muted); }

  /* animations */
  @keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
  }

  .logo-wrap { animation: float 4s ease-in-out infinite; }
</style>
</head>
<body>

<div class="glow-line"></div>

<!-- HERO -->
<div class="hero wrap">
  <div class="logo-wrap">🩺</div>
  <h1>Healthy AI</h1>
  <p class="hero-sub">Advanced ML-powered health prediction platform. Predict Heart Disease & Diabetes risk with clinical-grade accuracy — instantly.</p>

  <div class="badges">
    <span class="badge badge-purple">Python Flask</span>
    <span class="badge badge-cyan">Gradient Boosting</span>
    <span class="badge badge-green">scikit-learn</span>
    <span class="badge badge-yellow">SQLite</span>
    <span class="badge badge-purple">ReportLab PDF</span>
    <span class="badge badge-cyan">Glassmorphism UI</span>
    <span class="badge badge-green">Live on Render</span>
  </div>

  <div class="stats">
    <div class="stat-card">
      <div class="stat-num">97.2%</div>
      <div class="stat-label">Diabetes Accuracy</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">83.7%</div>
      <div class="stat-label">Heart Accuracy</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">100K+</div>
      <div class="stat-label">Training Samples</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">2</div>
      <div class="stat-label">AI Models</div>
    </div>
  </div>
</div>

<div class="wrap">

  <!-- LIVE LINK -->
  <div class="section">
    <div class="card" style="background:linear-gradient(135deg,rgba(6,214,160,0.08),rgba(0,212,255,0.05));border-color:rgba(6,214,160,0.3);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
      <div>
        <div style="font-size:12px;color:var(--green);font-family:'JetBrains Mono',monospace;font-weight:600;letter-spacing:1px;margin-bottom:4px;">🟢 LIVE DEPLOYMENT</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:white;">healthyai-dlog.onrender.com</div>
        <div style="font-size:13px;color:var(--muted);margin-top:2px;">Deployed on Render Free Tier · Always available</div>
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--cyan);background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.2);padding:10px 18px;border-radius:10px;">
        https://healthyai-dlog.onrender.com
      </div>
    </div>
  </div>

  <!-- FEATURES -->
  <div class="section">
    <div class="section-title">✨ Features</div>
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feat-icon">❤️</div>
        <div class="feat-title">Heart Disease Detection</div>
        <div class="feat-desc">Predict 10-year cardiovascular risk using 14 clinical parameters with Gradient Boosting ML.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">💉</div>
        <div class="feat-title">Diabetes Detection</div>
        <div class="feat-desc">Detect diabetes risk from HbA1c, BMI, glucose & more with 97.2% accuracy on 100K records.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">📊</div>
        <div class="feat-title">EDA Visualizations</div>
        <div class="feat-desc">Deep exploratory analysis — feature importance, class distribution, correlations, age/BMI charts.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">📄</div>
        <div class="feat-title">PDF Report Generation</div>
        <div class="feat-desc">Professional health reports with risk gauge, patient info, parameters & personalized recommendations.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">📋</div>
        <div class="feat-title">Report History</div>
        <div class="feat-desc">All past predictions saved per user. Download any report anytime as PDF.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">🔐</div>
        <div class="feat-title">Auth & Security</div>
        <div class="feat-desc">Register/Login with SHA-256 hashed passwords. Session-based auth. Private per-user data.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">🎯</div>
        <div class="feat-title">Risk Gauge Chart</div>
        <div class="feat-desc">Beautiful animated gauge showing Low / Moderate / High risk with exact probability %.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">💬</div>
        <div class="feat-title">User Feedback System</div>
        <div class="feat-desc">Collect star ratings and comments from users. View feedback via secret admin panel.</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">🛡️</div>
        <div class="feat-title">Secret Admin Panel</div>
        <div class="feat-desc">Hidden admin route to view all users, reports, feedback & live stats — password protected.</div>
      </div>
    </div>
  </div>

  <!-- ML MODELS -->
  <div class="section">
    <div class="section-title">🧠 ML Models</div>
    <div class="model-grid">
      <div class="model-card heart">
        <div class="model-type">Heart Disease</div>
        <div class="model-name">Gradient Boosting Classifier</div>
        <div class="model-stats">
          <div class="ms"><div class="ms-val">83.7%</div><div class="ms-key">Accuracy</div></div>
          <div class="ms"><div class="ms-val">67.2%</div><div class="ms-key">ROC-AUC</div></div>
          <div class="ms"><div class="ms-val">3.6K</div><div class="ms-key">Records</div></div>
        </div>
        <div class="model-tags">
          <span class="tag">age</span><span class="tag">sysBP</span><span class="tag">glucose</span>
          <span class="tag">totChol</span><span class="tag">BMI</span><span class="tag">smoking</span>
          <span class="tag">+8 more</span>
        </div>
      </div>
      <div class="model-card diabetes">
        <div class="model-type">Diabetes</div>
        <div class="model-name">Gradient Boosting Classifier</div>
        <div class="model-stats">
          <div class="ms"><div class="ms-val">97.2%</div><div class="ms-key">Accuracy</div></div>
          <div class="ms"><div class="ms-val">97.6%</div><div class="ms-key">ROC-AUC</div></div>
          <div class="ms"><div class="ms-val">100K</div><div class="ms-key">Records</div></div>
        </div>
        <div class="model-tags">
          <span class="tag">HbA1c</span><span class="tag">glucose</span><span class="tag">BMI</span>
          <span class="tag">age</span><span class="tag">smoking</span><span class="tag">+3 more</span>
        </div>
      </div>
    </div>
  </div>

  <!-- ROUTES -->
  <div class="section">
    <div class="section-title">🌐 Routes & Pages</div>
    <div class="card" style="padding:0;overflow:hidden;">
      <table class="route-table">
        <tr>
          <th style="padding:14px 20px;">Route</th>
          <th>Description</th>
          <th>Auth</th>
        </tr>
        <tr><td class="route-path" style="padding-left:20px;">/</td><td>Landing page with features & stats</td><td style="color:var(--green);">Public</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/login</td><td>Login & Register page</td><td style="color:var(--green);">Public</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/dashboard</td><td>User dashboard — stats, quick actions, recent reports</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/predict/heart</td><td>❤️ Heart disease prediction form + result</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/predict/diabetes</td><td>💉 Diabetes prediction form + result</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/eda/heart</td><td>📊 Heart disease EDA charts & analysis</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/eda/diabetes</td><td>📊 Diabetes EDA charts & analysis</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/reports</td><td>📋 All saved reports — view & download</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/download/&lt;file&gt;</td><td>Download specific PDF report</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/api/stats</td><td>JSON API — user report stats</td><td style="color:var(--yellow);">Private</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/terms</td><td>Terms of Service</td><td style="color:var(--green);">Public</td></tr>
        <tr><td class="route-path" style="padding-left:20px;">/privacy</td><td>Privacy Policy</td><td style="color:var(--green);">Public</td></tr>
        <tr><td class="route-path" style="padding-left:20px;padding-bottom:14px;">/admin/[secret]</td><td>🔒 Admin panel — users, reports, feedback</td><td style="color:var(--red);">Secret</td></tr>
      </table>
    </div>
  </div>

  <!-- SETUP -->
  <div class="section">
    <div class="section-title">🚀 Setup & Run</div>
    <div class="code-block">
      <div><span class="code-comment"># 1. Clone the repository</span></div>
      <div><span class="code-cmd">git clone</span> <span class="code-string">https://github.com/BhavyaKansal20/healthy-ai.git</span></div>
      <div><span class="code-cmd">cd</span> healthy-ai</div>
      <br>
      <div><span class="code-comment"># 2. Install dependencies</span></div>
      <div><span class="code-cmd">pip install</span> -r requirements.txt</div>
      <br>
      <div><span class="code-comment"># 3. Train ML models (auto-runs on first launch too)</span></div>
      <div><span class="code-cmd">python</span> train_models.py</div>
      <br>
      <div><span class="code-comment"># 4. Launch the app</span></div>
      <div><span class="code-cmd">python</span> app.py</div>
      <br>
      <div><span class="code-comment"># Open browser at → http://localhost:5000</span></div>
    </div>
  </div>

  <!-- PROJECT STRUCTURE -->
  <div class="section">
    <div class="section-title">📁 Project Structure</div>
    <div class="tree">
      <div><span class="tree-dir">healthy-ai/</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-special">app.py</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-comment"># Main Flask app — all routes & logic</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-special">train_models.py</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-comment"># GBC training — heart & diabetes</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-file">requirements.txt</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-file">render.yaml</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-comment"># Render deploy config</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-file">README.html</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-comment"># This file</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-dir">data_files/</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-file">heart.csv</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-comment"># Framingham Heart Study (3.6K records)</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="tree-file">diabetes.csv</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-comment"># Diabetes dataset (100K records)</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-dir">models/</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-file">heart_model.pkl</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-file">heart_scaler.pkl</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-file">heart_meta.json</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-file">diabetes_model.pkl</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-file">diabetes_scaler.pkl</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="tree-file">diabetes_le_*.pkl</span></div>
      <div>&nbsp;&nbsp;├── <span class="tree-dir">static/</span></div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-dir">img/</span> logo.png</div>
      <div>&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="tree-dir">reports/</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-comment"># Generated PDFs (auto)</span></div>
      <div>&nbsp;&nbsp;└── <span class="tree-dir">templates/</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span class="tree-file">base.html, index.html, login.html</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span class="tree-file">dashboard.html, reports.html</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span class="tree-file">predict_heart.html, predict_diabetes.html</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span class="tree-file">eda.html</span></div>
      <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── <span class="tree-file">terms.html, privacy.html</span></div>
    </div>
  </div>

  <!-- TECH STACK -->
  <div class="section">
    <div class="section-title">⚙️ Tech Stack</div>
    <div class="tech-grid">
      <div class="tech-item"><div class="tech-icon">🐍</div><div><div class="tech-name">Python 3.11</div><div class="tech-role">Core language</div></div></div>
      <div class="tech-item"><div class="tech-icon">🌶️</div><div><div class="tech-name">Flask 3.x</div><div class="tech-role">Web framework</div></div></div>
      <div class="tech-item"><div class="tech-icon">🤖</div><div><div class="tech-name">scikit-learn</div><div class="tech-role">ML models</div></div></div>
      <div class="tech-item"><div class="tech-icon">🗃️</div><div><div class="tech-name">SQLite</div><div class="tech-role">Database</div></div></div>
      <div class="tech-item"><div class="tech-icon">📈</div><div><div class="tech-name">Matplotlib</div><div class="tech-role">Charts & EDA</div></div></div>
      <div class="tech-item"><div class="tech-icon">📄</div><div><div class="tech-name">ReportLab</div><div class="tech-role">PDF generation</div></div></div>
      <div class="tech-item"><div class="tech-icon">🎨</div><div><div class="tech-name">Glassmorphism</div><div class="tech-role">UI Design</div></div></div>
      <div class="tech-item"><div class="tech-icon">☁️</div><div><div class="tech-name">Render</div><div class="tech-role">Deployment</div></div></div>
      <div class="tech-item"><div class="tech-icon">🔒</div><div><div class="tech-name">SHA-256</div><div class="tech-role">Password hashing</div></div></div>
    </div>
  </div>

  <!-- FEEDBACK & ADMIN -->
  <div class="section">
    <div class="section-title">💬 Feedback & Admin</div>
    <div class="feedback-card" style="margin-bottom:16px;">
      <div style="font-weight:700;color:white;margin-bottom:8px;font-size:15px;">💬 User Feedback System</div>
      <div style="font-size:13px;color:var(--muted);line-height:1.7;">
        Users can submit star ratings (1–5) and written comments after using the platform.
        Feedback is stored in the database and visible only via the secret admin panel.
        Designed to be lightweight — no friction, no email required.
      </div>
    </div>
    <div class="admin-card">
      <div class="admin-icon">🛡️</div>
      <div>
        <div class="admin-title">Secret Admin Panel</div>
        <div class="admin-desc">Hidden route with password protection. View all registered users, generated reports, feedback ratings, and live stats. Only the developer has access — no link exists anywhere on the public site.</div>
      </div>
    </div>
  </div>

  <!-- DISCLAIMER -->
  <div class="disclaimer">
    <span style="font-size:18px;">⚠️</span>
    <div>
      <strong style="color:#fca5a5;">Medical Disclaimer</strong><br>
      Healthy AI is built for <strong>educational and research purposes only</strong>. All predictions are generated by ML models and do not constitute medical advice. Always consult a qualified healthcare professional for diagnosis and treatment.
    </div>
  </div>

  <div class="divider"></div>

</div>

<!-- FOOTER -->
<div class="footer">
  <div class="footer-logo">🩺 Healthy AI</div>
  <div>Built with ❤️ by <strong style="color:white;">Bhavya Kansal</strong> · Multimodex AI · 2026</div>
  <div style="margin-top:8px;">
    <a href="https://healthyai-dlog.onrender.com" style="color:var(--cyan);text-decoration:none;margin:0 12px;">🌐 Live Demo</a>
    <a href="https://github.com/BhavyaKansal20/healthy-ai" style="color:var(--purple);text-decoration:none;margin:0 12px;">⭐ GitHub</a>
  </div>
</div>

<div class="glow-line"></div>

</body>
</html>
