# dashboard.py - BPW Forensic Scanner Dashboard v3.0 (Redesigned)
import os
import random
import string
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- CHANGE THIS PASSWORD ---
ADMIN_PASSWORD = "DINGLE_012" 
# ----------------------------

sessions = {}

PROFESSIONAL_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BPW // FORENSIC SCANNER v3.0</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0a1a;
            --bg-secondary: #111128;
            --bg-card: rgba(255,255,255,0.03);
            --border-color: rgba(255,255,255,0.06);
            --text-primary: #ffffff;
            --text-secondary: #8888b8;
            --text-muted: #555577;
            --accent-purple: #7877c6;
            --accent-pink: #ff77c6;
            --accent-blue: #4facfe;
            --accent-teal: #00f2fe;
            --gradient-main: linear-gradient(135deg, #7877c6, #ff77c6);
            --gradient-blue: linear-gradient(135deg, #4facfe, #00f2fe);
            --shadow-glow: 0 0 40px rgba(120, 119, 198, 0.15);
            --radius: 16px;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(120,119,198,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(255,119,198,0.05) 0%, transparent 50%);
        }
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--accent-purple); border-radius: 10px; }
        
        /* ===== SIDEBAR ===== */
        .sidebar {
            width: 280px;
            min-height: 100vh;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            padding: 30px 0 20px;
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            overflow-y: auto;
            z-index: 100;
            backdrop-filter: blur(20px);
            transition: transform 0.3s ease;
        }
        
        .sidebar-brand {
            padding: 0 24px 30px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
        }
        
        .sidebar-brand h1 {
            font-size: 26px;
            font-weight: 900;
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        
        .sidebar-brand span {
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .nav-item {
            padding: 14px 24px;
            margin: 4px 12px;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 14px;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 14px;
            transition: all 0.25s ease;
            position: relative;
        }
        
        .nav-item:hover {
            background: rgba(255,255,255,0.04);
            color: #fff;
        }
        
        .nav-item.active {
            background: rgba(120,119,198,0.15);
            color: #fff;
            box-shadow: inset 3px 0 0 var(--accent-purple);
        }
        
        .nav-item .icon {
            width: 20px;
            text-align: center;
            font-size: 16px;
        }
        
        .nav-item .badge-nav {
            margin-left: auto;
            background: rgba(239,68,68,0.2);
            color: #ef4444;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 10px;
            border-radius: 20px;
        }
        
        .sidebar-footer {
            position: absolute;
            bottom: 20px;
            left: 12px;
            right: 12px;
            padding: 16px 20px;
            background: rgba(239,68,68,0.08);
            border: 1px solid rgba(239,68,68,0.15);
            border-radius: 12px;
            text-align: center;
        }
        
        .sidebar-footer a {
            color: #ef4444;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .sidebar-footer a:hover { opacity: 0.8; }
        
        /* ===== MAIN ===== */
        .main-content {
            margin-left: 280px;
            padding: 30px 40px 40px;
            flex: 1;
            min-height: 100vh;
        }
        
        /* ===== TOP BAR ===== */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px 28px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            backdrop-filter: blur(10px);
        }
        
        .top-bar-left h2 {
            font-size: 22px;
            font-weight: 700;
            background: var(--gradient-blue);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .top-bar-left p {
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 2px;
            -webkit-text-fill-color: var(--text-secondary);
        }
        
        .top-bar-right {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .stat-badge {
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stat-badge.detections {
            background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(220,38,38,0.1));
            color: #ef4444;
            border: 1px solid rgba(239,68,68,0.2);
        }
        
        .stat-badge.warnings {
            background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(217,119,6,0.1));
            color: #f59e0b;
            border: 1px solid rgba(245,158,11,0.2);
        }
        
        /* ===== STATS GRID ===== */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            padding: 24px 28px;
            border-radius: var(--radius);
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-glow);
            border-color: rgba(120,119,198,0.2);
        }
        
        .stat-card .icon-bg {
            position: absolute;
            right: -10px;
            bottom: -10px;
            font-size: 60px;
            opacity: 0.04;
        }
        
        .stat-card .label {
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        
        .stat-card .value {
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -1px;
        }
        
        .stat-card .value.detections { color: #ef4444; }
        .stat-card .value.warnings { color: #f59e0b; }
        .stat-card .value.information { color: var(--accent-blue); }
        .stat-card .value.total { color: #fff; }
        
        .stat-card .sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }
        
        .stat-card.detections { border-left: 3px solid #ef4444; }
        .stat-card.warnings { border-left: 3px solid #f59e0b; }
        .stat-card.information { border-left: 3px solid var(--accent-blue); }
        .stat-card.total { border-left: 3px solid var(--accent-purple); }
        
        /* ===== MAIN GRID ===== */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 30px;
        }
        
        .glass-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 28px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .glass-panel:hover {
            border-color: rgba(120,119,198,0.15);
        }
        
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .panel-title {
            font-size: 18px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .panel-title .emoji { font-size: 20px; }
        
        /* ===== BUTTONS ===== */
        .btn-primary {
            background: var(--gradient-main);
            color: #fff;
            border: none;
            padding: 14px 28px;
            font-size: 15px;
            font-weight: 700;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(120,119,198,0.35);
        }
        
        .btn-primary:active { transform: scale(0.97); }
        
        .btn-secondary {
            background: rgba(255,255,255,0.05);
            color: #fff;
            border: 1px solid var(--border-color);
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-secondary:hover {
            background: rgba(255,255,255,0.1);
        }
        
        /* ===== CODE DISPLAY ===== */
        .code-display {
            background: linear-gradient(135deg, rgba(15,12,41,0.8), rgba(48,43,99,0.6));
            border: 2px solid rgba(120,119,198,0.25);
            border-radius: 14px;
            padding: 28px;
            text-align: center;
            margin: 20px 0 16px;
            position: relative;
            overflow: hidden;
        }
        
        .code-display::before {
            content: '';
            position: absolute;
            inset: -2px;
            background: var(--gradient-main);
            opacity: 0.1;
            border-radius: 14px;
            z-index: -1;
        }
        
        .code-display .label {
            font-size: 12px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }
        
        .code-value {
            font-size: 56px;
            font-weight: 900;
            font-family: 'Inter', monospace;
            letter-spacing: 12px;
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            user-select: all;
        }
        
        .code-display .hint {
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 8px;
        }
        
        /* ===== INPUT ===== */
        .input-group {
            display: flex;
            gap: 12px;
            margin: 16px 0;
        }
        
        .input-group input {
            flex: 1;
            background: rgba(255,255,255,0.04);
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 14px 18px;
            border-radius: 10px;
            font-size: 16px;
            font-family: 'Inter', monospace;
            letter-spacing: 4px;
            transition: all 0.3s ease;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: var(--accent-purple);
            box-shadow: 0 0 20px rgba(120,119,198,0.1);
        }
        
        .input-group input::placeholder {
            color: var(--text-muted);
            letter-spacing: 0;
            font-family: 'Inter', sans-serif;
        }
        
        .input-group .btn-primary {
            width: auto;
            padding: 14px 32px;
        }
        
        /* ===== LOG OUTPUT ===== */
        .log-output {
            background: rgba(0,0,0,0.4);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Inter', monospace;
            font-size: 13px;
            min-height: 150px;
        }
        
        .log-output .empty {
            color: var(--text-muted);
            text-align: center;
            padding: 40px 20px;
        }
        
        .log-output .success {
            color: #34d399;
            text-align: center;
            padding: 30px 20px;
        }
        
        .log-output .success i { font-size: 32px; display: block; margin-bottom: 12px; }
        
        /* ===== FINDING CARDS ===== */
        .finding-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 12px;
            transition: all 0.2s ease;
        }
        
        .finding-card:hover {
            background: rgba(255,255,255,0.04);
        }
        
        .finding-card.detection { border-left: 4px solid #ef4444; }
        .finding-card.warning { border-left: 4px solid #f59e0b; }
        .finding-card.info { border-left: 4px solid var(--accent-blue); }
        
        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .finding-title {
            font-weight: 600;
            font-size: 14px;
            color: #fff;
        }
        
        .badge {
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        
        .badge-detection {
            background: rgba(239,68,68,0.2);
            color: #ef4444;
            border: 1px solid rgba(239,68,68,0.2);
        }
        
        .badge-warning {
            background: rgba(245,158,11,0.2);
            color: #f59e0b;
            border: 1px solid rgba(245,158,11,0.2);
        }
        
        .badge-info {
            background: rgba(79,172,254,0.15);
            color: var(--accent-blue);
            border: 1px solid rgba(79,172,254,0.15);
        }
        
        .finding-detail {
            color: var(--text-secondary);
            font-size: 13px;
            margin: 4px 0;
            word-break: break-all;
        }
        
        .finding-detail .highlight {
            color: var(--accent-blue);
            font-family: 'Inter', monospace;
            font-size: 12px;
        }
        
        .finding-meta {
            display: flex;
            gap: 16px;
            margin-top: 8px;
            font-size: 11px;
            color: var(--text-muted);
        }
        
        .finding-meta i { margin-right: 4px; }
        
        /* ===== CHART ===== */
        .chart-container {
            position: relative;
            height: 260px;
            margin: 10px 0;
        }
        
        /* ===== PAGES ===== */
        .page { display: none; animation: fadeSlide 0.4s ease; }
        .page.active { display: block; }
        
        @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* ===== EMPTY STATE ===== */
        .empty-state {
            color: var(--text-muted);
            text-align: center;
            padding: 50px 20px;
        }
        
        .empty-state i { font-size: 40px; margin-bottom: 16px; opacity: 0.3; }
        .empty-state h4 { color: var(--text-secondary); margin-bottom: 6px; }
        .empty-state p { font-size: 14px; }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 1200px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .main-grid { grid-template-columns: 1fr; }
        }
        
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
                width: 280px;
            }
            .sidebar.open { transform: translateX(0); }
            .main-content { margin-left: 0; padding: 20px; }
            .top-bar { flex-direction: column; align-items: flex-start; gap: 12px; }
            .stats-grid { grid-template-columns: 1fr 1fr; }
            .code-value { font-size: 36px; letter-spacing: 8px; }
            .input-group { flex-direction: column; }
            .input-group .btn-primary { width: 100%; }
        }
        
        /* ===== SECTION GRID ===== */
        .section-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 900px) {
            .section-grid { grid-template-columns: 1fr; }
        }
        
        /* ===== AI BADGE ===== */
        .ai-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 600;
            color: var(--accent-teal);
            background: rgba(0,242,254,0.08);
            padding: 4px 14px;
            border-radius: 20px;
            border: 1px solid rgba(0,242,254,0.1);
        }
        
        /* ===== FILTER ===== */
        .filter-bar {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 6px 16px;
            border-radius: 20px;
            border: 1px solid var(--border-color);
            background: transparent;
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .filter-btn:hover {
            background: rgba(255,255,255,0.05);
            color: #fff;
        }
        
        .filter-btn.active {
            background: rgba(120,119,198,0.2);
            color: #fff;
            border-color: var(--accent-purple);
        }
        
        /* ===== MOBILE TOGGLE ===== */
        .mobile-toggle {
            display: none;
            background: none;
            border: none;
            color: #fff;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
        }
        
        @media (max-width: 768px) {
            .mobile-toggle { display: block; }
        }
    </style>
</head>
<body>

<!-- ===== SIDEBAR ===== -->
<nav class="sidebar" id="sidebar">
    <div class="sidebar-brand">
        <h1>⚡ BPW</h1>
        <span>Forensic Scanner v3.0</span>
    </div>
    
    <div class="nav-item active" onclick="showPage('overview')">
        <span class="icon">📊</span> Overview
    </div>
    <div class="nav-item" onclick="showPage('general')">
        <span class="icon">ℹ️</span> General Info
    </div>
    <div class="nav-item" onclick="showPage('files')">
        <span class="icon">📄</span> File Activity
    </div>
    <div class="nav-item" onclick="showPage('suspicious')">
        <span class="icon">⚠️</span> Suspicious
        <span class="badge-nav" id="suspicious-count">0</span>
    </div>
    <div class="nav-item" onclick="showPage('accounts')">
        <span class="icon">👤</span> Alt Accounts
    </div>
    
    <div class="sidebar-footer">
        <a href="/logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </div>
</nav>

<!-- ===== MAIN ===== -->
<div class="main-content">

    <!-- Mobile Toggle -->
    <button class="mobile-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">
        <i class="fas fa-bars"></i>
    </button>

    <!-- ===== TOP BAR ===== -->
    <div class="top-bar">
        <div class="top-bar-left">
            <h2>🎯 Dashboard</h2>
            <p>Real-time forensic analysis & threat detection</p>
        </div>
        <div class="top-bar-right">
            <span class="stat-badge warnings"><i class="fas fa-exclamation-triangle"></i> <span id="top-warnings">0</span></span>
            <span class="stat-badge detections"><i class="fas fa-crosshairs"></i> <span id="top-detections">0</span></span>
            <span class="ai-badge"><i class="fas fa-brain"></i> AI-Powered</span>
        </div>
    </div>

    <!-- ===== PAGE: OVERVIEW ===== -->
    <div id="page-overview" class="page active">
        
        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card detections">
                <div class="icon-bg"><i class="fas fa-bug"></i></div>
                <div class="label">🎯 Detections</div>
                <div class="value detections" id="stat-detections">0</div>
                <div class="sub">High-confidence threats</div>
            </div>
            <div class="stat-card warnings">
                <div class="icon-bg"><i class="fas fa-exclamation-circle"></i></div>
                <div class="label">⚠️ Warnings</div>
                <div class="value warnings" id="stat-warnings">0</div>
                <div class="sub">Suspicious activity</div>
            </div>
            <div class="stat-card information">
                <div class="icon-bg"><i class="fas fa-info-circle"></i></div>
                <div class="label">ℹ️ Information</div>
                <div class="value information" id="stat-information">0</div>
                <div class="sub">System context</div>
            </div>
            <div class="stat-card total">
                <div class="icon-bg"><i class="fas fa-database"></i></div>
                <div class="label">📊 Total Logs</div>
                <div class="value total" id="stat-total">0</div>
                <div class="sub">All findings combined</div>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="main-grid">
            <!-- Generate Code -->
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title"><span class="emoji">🔑</span> Generate Access Code</div>
                </div>
                <button class="btn-primary" onclick="generatePin()">
                    <i class="fas fa-sync-alt"></i> Generate New Code
                </button>
                <div class="code-display">
                    <div class="label">Your 6-Digit Code</div>
                    <div class="code-value" id="pin-display">------</div>
                    <div class="hint">Share this code with the target PC</div>
                </div>
            </div>

            <!-- Retrieve Logs -->
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title"><span class="emoji">📥</span> Retrieve Logs</div>
                </div>
                <div class="input-group">
                    <input type="text" id="fetch-pin" placeholder="Enter 6-digit code" maxlength="6">
                    <button class="btn-primary" onclick="fetchLogs()">
                        <i class="fas fa-search"></i> Fetch
                    </button>
                </div>
                <div id="log-output" class="log-output">
                    <div class="empty">
                        <i class="fas fa-inbox"></i>
                        <p>Logs will appear here after fetching...</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Chart -->
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">📈</span> Threat Analysis</div>
            </div>
            <div class="chart-container">
                <canvas id="pieChart"></canvas>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: GENERAL ===== -->
    <div id="page-general" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">ℹ️</span> General Information</div>
            </div>
            <div id="general-content">
                <div class="empty-state">
                    <i class="fas fa-folder-open"></i>
                    <h4>No Data Loaded</h4>
                    <p>Fetch logs from Overview to see system information</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: FILES ===== -->
    <div id="page-files" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">📄</span> Suspicious Files</div>
            </div>
            <div id="files-content">
                <div class="empty-state">
                    <i class="fas fa-file"></i>
                    <h4>No Suspicious Files</h4>
                    <p>No suspicious files detected on this system</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: SUSPICIOUS ===== -->
    <div id="page-suspicious" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">⚠️</span> Suspicious Findings</div>
                <span class="ai-badge"><i class="fas fa-robot"></i> AI Verified</span>
            </div>
            <div class="filter-bar">
                <button class="filter-btn active" data-filter="all" onclick="filterFindings('all')">All</button>
                <button class="filter-btn" data-filter="detection" onclick="filterFindings('detection')">🎯 Detections</button>
                <button class="filter-btn" data-filter="warning" onclick="filterFindings('warning')">⚠️ Warnings</button>
            </div>
            <div id="suspicious-content">
                <div class="empty-state">
                    <i class="fas fa-shield-alt"></i>
                    <h4>No Suspicious Findings</h4>
                    <p>System appears clean</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: ACCOUNTS ===== -->
    <div id="page-accounts" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">👤</span> Alt Accounts</div>
            </div>
            <div id="accounts-content">
                <div class="empty-state">
                    <i class="fas fa-user-circle"></i>
                    <h4>No Alt Accounts Found</h4>
                    <p>No alternative accounts detected on this system</p>
                </div>
            </div>
        </div>
    </div>

</div>

<!-- ===== JAVASCRIPT ===== -->
<script>
    let currentLogs = null;
    let allFindings = [];
    let pieChart = null;
    let currentFilter = 'all';

    // ===== NAVIGATION =====
    function showPage(pageId) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.getElementById('page-' + pageId).classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => {
            if (n.textContent.trim().toLowerCase().includes(pageId.toLowerCase())) {
                n.classList.add('active');
            }
        });
        // Close mobile sidebar
        document.getElementById('sidebar').classList.remove('open');
    }

    // ===== GENERATE PIN =====
    async function generatePin() {
        const res = await fetch('/api/generate-pin');
        const data = await res.json();
        document.getElementById('pin-display').innerText = data.pin;
    }

    // ===== FETCH LOGS =====
    async function fetchLogs() {
        const pin = document.getElementById('fetch-pin').value;
        if (pin.length !== 6) { alert("Please enter a 6-digit code"); return; }

        const output = document.getElementById('log-output');
        output.innerHTML = `<div style="text-align:center;padding:40px;color:var(--accent-purple);">
            <i class="fas fa-spinner fa-spin" style="font-size:30px;"></i>
            <p style="margin-top:12px;">Fetching logs...</p>
        </div>`;

        try {
            const res = await fetch('/api/get-logs/' + pin);
            const data = await res.json();

            if (data.status === 'success') {
                currentLogs = data.logs;
                allFindings = data.logs.findings || [];
                updateOverview(data.logs);
                populateAllSections(data.logs);
                output.innerHTML = `<div class="success">
                    <i class="fas fa-check-circle"></i>
                    <p>✅ Logs loaded! Click sidebar sections to view findings.</p>
                    <p style="font-size:12px;color:var(--text-muted);margin-top:4px;">${allFindings.length} findings found</p>
                </div>`;
            } else {
                output.innerHTML = `<div style="color:#ef4444;text-align:center;padding:30px;">
                    <i class="fas fa-times-circle" style="font-size:30px;"></i>
                    <p style="margin-top:8px;">${data.message}</p>
                </div>`;
            }
        } catch (e) {
            output.innerHTML = `<div style="color:#ef4444;text-align:center;padding:30px;">
                <i class="fas fa-exclamation-circle" style="font-size:30px;"></i>
                <p style="margin-top:8px;">Connection error: ${e}</p>
            </div>`;
        }
    }

    // ===== UPDATE OVERVIEW =====
    function updateOverview(logs) {
        let detections = 0, warnings = 0, information = 0;

        if (logs.findings) {
            logs.findings.forEach(f => {
                const tier = (f.tier || 'Information').toLowerCase();
                if (tier === 'detection') detections++;
                else if (tier === 'warning') warnings++;
                else information++;
            });
        }

        document.getElementById('stat-detections').innerText = detections;
        document.getElementById('stat-warnings').innerText = warnings;
        document.getElementById('stat-information').innerText = information;
        document.getElementById('stat-total').innerText = logs.total_findings || 0;
        document.getElementById('top-warnings').innerText = warnings;
        document.getElementById('top-detections').innerText = detections;
        document.getElementById('suspicious-count').innerText = detections + warnings;

        drawPieChart(detections, warnings, information);
    }

    // ===== CREATE FINDING CARD =====
    function createFindingCard(item) {
        const tier = (
