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

CYBER_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BPW // FORENSIC SCANNER</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }
        
        /* Sidebar */
        .sidebar {
            width: 280px;
            background: rgba(15, 12, 41, 0.8);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            padding: 30px 0;
        }
        
        .sidebar-header {
            padding: 0 25px 30px;
            border-bottom: 2px solid rgba(120, 119, 198, 0.3);
        }
        
        .sidebar-header h1 {
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 2px;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .sidebar-header p {
            color: #888;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .nav-item {
            padding: 15px 25px;
            margin: 5px 15px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s;
            border-radius: 12px;
            color: #888;
            font-weight: 600;
        }
        
        .nav-item:hover {
            background: rgba(120, 119, 198, 0.1);
            color: #fff;
            transform: translateX(5px);
        }
        
        .nav-item.active {
            background: linear-gradient(135deg, rgba(120, 119, 198, 0.3), rgba(255, 119, 198, 0.3));
            color: #fff;
            box-shadow: 0 4px 15px rgba(120, 119, 198, 0.3);
        }
        
        .nav-icon {
            font-size: 20px;
            width: 24px;
            text-align: center;
        }
        
        /* Main Content */
        .main-content {
            margin-left: 280px;
            padding: 40px;
        }
        
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding: 20px 30px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .top-bar h2 {
            color: #fff;
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, #7877c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .top-stats {
            display: flex;
            gap: 15px;
        }
        
        .stat-badge {
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: 'JetBrains Mono', monospace;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .stat-badge.warnings {
            background: linear-gradient(135deg, #f59e0b, #f97316);
            color: #fff;
        }
        
        .stat-badge.detections {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: #fff;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            padding: 30px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #7877c6, #ff77c6);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(120, 119, 198, 0.2);
        }
        
        .stat-card.detections::before {
            background: linear-gradient(90deg, #ef4444, #f97316);
        }
        
        .stat-card.warnings::before {
            background: linear-gradient(90deg, #f59e0b, #eab308);
        }
        
        .stat-card.information::before {
            background: linear-gradient(90deg, #06b6d4, #3b82f6);
        }
        
        .stat-card-title {
            font-size: 14px;
            color: #888;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-card-value {
            font-size: 48px;
            font-weight: 800;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* Main Grid */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .glass-panel {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
        }
        
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 2px solid rgba(120, 119, 198, 0.3);
        }
        
        .panel-title {
            font-size: 22px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .panel-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        
        /* Buttons */
        .btn-primary {
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            color: #fff;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 700;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 15px rgba(120, 119, 198, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(120, 119, 198, 0.4);
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* Code Display */
        .code-display {
            background: linear-gradient(135deg, rgba(15, 12, 41, 0.8), rgba(48, 43, 99, 0.8));
            border: 2px solid rgba(120, 119, 198, 0.5);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }
        
        .code-display::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(120, 119, 198, 0.03) 10px,
                rgba(120, 119, 198, 0.03) 20px
            );
            animation: slide 20s linear infinite;
        }
        
        @keyframes slide {
            0% { transform: translate(-50%, -50%); }
            100% { transform: translate(0, 0); }
        }
        
        .code-label {
            color: #888;
            font-size: 14px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .code-value {
            font-size: 64px;
            font-weight: 800;
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 10px;
            position: relative;
            z-index: 1;
        }
        
        /* Input Group */
        .input-group {
            display: flex;
            gap: 15px;
            margin: 20px 0;
        }
        
        .input-group input {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 15px 20px;
            border-radius: 12px;
            font-size: 16px;
            font-family: 'JetBrains Mono', monospace;
            transition: all 0.3s;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #7877c6;
            box-shadow: 0 0 20px rgba(120, 119, 198, 0.2);
        }
        
        /* Log Output */
        .log-output {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(120, 119, 198, 0.3);
            border-radius: 12px;
            padding: 20px;
            max-height: 500px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            line-height: 1.6;
        }
        
        .log-output::-webkit-scrollbar {
            width: 8px;
        }
        
        .log-output::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }
        
        .log-output::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            border-radius: 4px;
        }
        
        /* Chart Container */
        .chart-container {
            position: relative;
            height: 300px;
            margin: 20px 0;
        }
        
        /* Collapsible */
        .collapsible {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            margin-bottom: 15px;
            overflow: hidden;
        }
        
        .collapsible-header {
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
        }
        
        .collapsible-header:hover {
            background: rgba(120, 119, 198, 0.1);
        }
        
        .collapsible-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            color: #fff;
        }
        
        .collapsible-arrow {
            transition: transform 0.3s;
            color: #7877c6;
        }
        
        .collapsible.open .collapsible-arrow {
            transform: rotate(90deg);
        }
        
        .collapsible-content {
            display: none;
            padding: 0 20px 20px;
        }
        
        .collapsible.open .collapsible-content {
            display: block;
        }
        
        .badge {
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .badge-critical {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: #fff;
        }
        
        .badge-high {
            background: linear-gradient(135deg, #f97316, #ea580c);
            color: #fff;
        }
        
        .badge-medium {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #fff;
        }
        
        .badge-info {
            background: linear-gradient(135deg, #06b6d4, #0891b2);
            color: #fff;
        }
        
        .logout-btn {
            position: fixed;
            bottom: 30px;
            left: 30px;
            right: 30px;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.2));
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fff;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .logout-btn:hover {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(220, 38, 38, 0.3));
            transform: translateY(-2px);
        }
        
        .page {
            display: none;
        }
        
        .page.active {
            display: block;
            animation: fadeIn 0.5s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>⚡ BPW</h1>
            <p>FORENSIC SCANNER v2.0</p>
        </div>
        
        <div class="nav-item active" onclick="showPage('overview')">
            <span class="nav-icon">📊</span>
            <span>Overview</span>
        </div>
        
        <div class="nav-item" onclick="showPage('general')">
            <span class="nav-icon">ℹ️</span>
            <span>General Info</span>
        </div>
        
        <div class="nav-item" onclick="showPage('system')">
            <span class="nav-icon">🖥️</span>
            <span>System</span>
        </div>
        
        <div class="nav-item" onclick="showPage('files')">
            <span class="nav-icon">📄</span>
            <span>File Activity</span>
        </div>
        
        <div class="nav-item" onclick="showPage('suspicious')">
            <span class="nav-icon">⚠️</span>
            <span>Suspicious</span>
        </div>
        
        <div class="nav-item" onclick="showPage('accounts')">
            <span class="nav-icon"></span>
            <span>Alt Accounts</span>
        </div>
        
        <div class="nav-item" onclick="showPage('tools')">
            <span class="nav-icon">🔧</span>
            <span>Tools</span>
        </div>
        
        <a href="/logout" class="logout-btn">🚪 Logout</a>
    </div>
    
    <!-- Main Content -->
    <div class="main-content">
        <div class="top-bar">
            <h2>🎯 Overview</h2>
            <div class="top-stats">
                <div class="stat-badge warnings">
                    <span>⚠️</span>
                    <span id="top-warnings">0</span>
                </div>
                <div class="stat-badge detections">
                    <span></span>
                    <span id="top-detections">0</span>
                </div>
            </div>
        </div>
        
        <!-- Overview Page -->
        <div id="page-overview" class="page active">
            <div class="stats-grid">
                <div class="stat-card detections">
                    <div class="stat-card-title">🎯 Detections</div>
                    <div class="stat-card-value" id="stat-detections">0</div>
                </div>
                
                <div class="stat-card warnings">
                    <div class="stat-card-title">⚠️ Warnings</div>
                    <div class="stat-card-value" id="stat-warnings">0</div>
                </div>
                
                <div class="stat-card information">
                    <div class="stat-card-title">ℹ️ Information</div>
                    <div class="stat-card-value" id="stat-information">0</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-card-title"> Total Logs</div>
                    <div class="stat-card-value" id="stat-total">0</div>
                </div>
            </div>
            
            <div class="main-grid">
                <div class="glass-panel">
                    <div class="panel-header">
                        <div class="panel-title">
                            <div class="panel-icon"></div>
                            <span>Generate Access Code</span>
                        </div>
                    </div>
                    <button class="btn-primary" onclick="generatePin()" style="width: 100%;">
                        ⚡ Generate New Code
                    </button>
                    <div class="code-display">
                        <div class="code-label">Your 6-Digit Code</div>
                        <div class="code-value" id="pin-display">------</div>
                    </div>
                    <p style="color: #888; text-align: center; font-size: 14px;">
                        Share this code with the target PC
                    </p>
                </div>
                
                <div class="glass-panel">
                    <div class="panel-header">
                        <div class="panel-title">
                            <div class="panel-icon">📥</div>
                            <span>Retrieve Logs</span>
                        </div>
                    </div>
                    <div class="input-group">
                        <input type="text" id="fetch-pin" placeholder="Enter 6-digit code" maxlength="6">
                        <button class="btn-primary" onclick="fetchLogs()">Fetch</button>
                    </div>
                    <div id="log-output" class="log-output">
                        <div style="color: #666; text-align: center; padding: 40px;">
                            Logs will appear here...
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <div class="panel-icon"></div>
                        <span>Threat Analysis</span>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="pieChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Other Pages (General, System, Files, etc.) -->
        <div id="page-general" class="page">
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <div class="panel-icon">ℹ️</div>
                        <span>General Information</span>
                    </div>
                </div>
                <div id="general-content">
                    <p style="color: #666; text-align: center; padding: 40px;">
                        Fetch logs from Overview to see data
                    </p>
                </div>
            </div>
        </div>
        
        <div id="page-system" class="page">
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <div class="panel-icon">️</div>
                        <span>System Information</span>
                    </div>
                </div>
                <p style="color: #666; text-align: center; padding: 40px;">
                    Fetch logs from Overview to see data
                </p>
            </div>
        </div>
        
        <div id="page-files" class="page">
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <div class="panel-icon"></div>
                        <span>File Activity</span>
                    </div>
                </div>
                <p style="color: #666; text-align: center; padding: 40px;">
                    Fetch logs from Overview to see data
                </p>
            </div>
        </div>
        
        <div id="page-suspicious" class="page">
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <div class="panel-icon">⚠️</div>
                        <span>Suspicious Entries</span>
                    </div>
                </div>
                <p style="color: #666; text-align: center; padding: 40px;">
                    Fetch logs from Overview to see data
                </p>
            </div>
        </div>
        
        <div id="page-accounts" class="page">
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <div class="panel-icon">👤</div>
                        <span>Alternative Accounts</span>
                    </div>
                </div>
                <p style="color: #666; text-align: center; padding: 40px;">
                    Fetch logs from Overview to see data
                </p>
            </div>
        </div>
        
        <div id="page-tools" class="page">
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <div class="panel-icon"></div>
                        <span>Tools</span>
                    </div>
                </div>
                <p style="color: #666; text-align: center; padding: 40px;">
                    Use the Overview page to generate codes and fetch logs
                </p>
            </div>
        </div>
    </div>
    
    <script>
        let currentLogs = null;
        let pieChart = null;
        
        function showPage(pageId) {
            document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            
            document.getElementById(`page-${pageId}`).classList.add('active');
            event.currentTarget.classList.add('active');
        }
        
        async function generatePin() {
            const res = await fetch('/api/generate-pin');
            const data = await res.json();
            document.getElementById('pin-display').innerText = data.pin;
        }
        
        async function fetchLogs() {
            const pin = document.getElementById('fetch-pin').value;
            if(pin.length !== 6) { alert("Please enter a 6-digit code"); return; }
            
            const output = document.getElementById('log-output');
            output.innerHTML = '<div style="color: #7877c6; text-align: center; padding: 40px;">Fetching logs...</div>';
            
            try {
                const res = await fetch(`/api/get-logs/${pin}`);
                const data = await res.json();
                
                if (data.status === 'success') {
                    currentLogs = data.logs;
                    updateOverview(data.logs);
                    output.innerHTML = '<div style="color: #06b6d4; text-align: center; padding: 20px;">✅ Logs loaded successfully!</div>' + 
                        '<pre style="color: #fff; margin-top: 20px;">' + JSON.stringify(data.logs, null, 2) + '</pre>';
                } else {
                    output.innerText = " Error: " + data.message;
                }
            } catch (e) {
                output.innerText = "❌ Error fetching logs: " + e;
            }
        }
        
        function updateOverview(logs) {
            let detections = 0;
            let warnings = 0;
            let information = 0;
            
            if (logs.findings) {
                logs.findings.forEach(finding => {
                    const severity = finding.severity || 'INFO';
                    if (severity === 'CRITICAL' || severity === 'HIGH') {
                        detections++;
                    } else if (severity === 'MEDIUM') {
                        warnings++;
                    } else {
                        information++;
                    }
                });
            }
            
            document.getElementById('stat-detections').innerText = detections;
            document.getElementById('stat-warnings').innerText = warnings;
            document.getElementById('stat-information').innerText = information;
            document.getElementById('stat-total').innerText = logs.total_findings || 0;
            document.getElementById('top-warnings').innerText = warnings;
            document.getElementById('top-detections').innerText = detections;
            
            drawPieChart(detections, warnings, information);
        }
        
        function drawPieChart(detections, warnings, information) {
            const ctx = document.getElementById('pieChart').getContext('2d');
            
            if (pieChart) {
                pieChart.destroy();
            }
            
            pieChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Detections', 'Warnings', 'Information'],
                    datasets: [{
                        data: [detections, warnings, information],
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.8)',
                            'rgba(245, 158, 11, 0.8)',
                            'rgba(6, 182, 212, 0.8)'
                        ],
                        borderColor: [
                            'rgba(239, 68, 68, 1)',
                            'rgba(245, 158, 11, 1)',
                            'rgba(6, 182, 212, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { 
                                color: '#fff', 
                                padding: 20,
                                font: { family: 'Inter', size: 14 }
                            }
                        }
                    }
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(CYBER_DASHBOARD)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template_string("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>BPW Login</title>
                    <style>
                        body { 
                            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                            color: #fff; 
                            font-family: 'Inter', sans-serif;
                            display: flex; 
                            justify-content: center; 
                            align-items: center; 
                            height: 100vh; 
                            margin: 0; 
                        }
                        .login-box { 
                            background: rgba(255, 255, 255, 0.03);
                            backdrop-filter: blur(10px);
                            padding: 50px; 
                            border-radius: 20px; 
                            border: 2px solid rgba(120, 119, 198, 0.3);
                            text-align: center;
                            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                        }
                        h1 { 
                            background: linear-gradient(135deg, #7877c6, #ff77c6);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            margin-bottom: 30px;
                            font-size: 32px;
                        }
                        input { 
                            background: rgba(255, 255, 255, 0.05);
                            border: 1px solid rgba(255, 255, 255, 0.2); 
                            color: #fff; 
                            padding: 15px; 
                            border-radius: 10px; 
                            width: 300px; 
                            margin-bottom: 20px; 
                            font-size: 16px; 
                        }
                        button { 
                            background: linear-gradient(135deg, #7877c6, #ff77c6);
                            color: #fff; 
                            border: none; 
                            padding: 15px 40px; 
                            font-weight: bold; 
                            cursor: pointer; 
                            border-radius: 10px; 
                            font-size: 16px;
                            transition: all 0.3s;
                        }
                        button:hover { 
                            transform: translateY(-2px);
                            box-shadow: 0 10px 30px rgba(120, 119, 198, 0.4);
                        }
                        .error { 
                            color: #ef4444; 
                            margin-bottom: 20px; 
                        }
                    </style>
                </head>
                <body>
                    <div class="login-box">
                        <h1>⚡ BPW FORENSIC</h1>
                        {% if error %}<div class="error">{{ error }}</div>{% endif %}
                        <form method="POST" action="/login">
                            <input type="password" name="password" placeholder="Enter Admin Password" required><br>
                            <button type="submit">Login</button>
                        </form>
                    </div>
                </body>
                </html>
            """, error="Wrong password!")
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>BPW Login</title>
            <style>
                body { 
                    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                    color: #fff; 
                    font-family: 'Inter', sans-serif;
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    height: 100vh; 
                    margin: 0; 
                }
                .login-box { 
                    background: rgba(255, 255, 255, 0.03);
                    backdrop-filter: blur(10px);
                    padding: 50px; 
                    border-radius: 20px; 
                    border: 2px solid rgba(120, 119, 198, 0.3);
                    text-align: center;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                }
                h1 { 
                    background: linear-gradient(135deg, #7877c6, #ff77c6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 30px;
                    font-size: 32px;
                }
                input { 
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.2); 
                    color: #fff; 
                    padding: 15px; 
                    border-radius: 10px; 
                    width: 300px; 
                    margin-bottom: 20px; 
                    font-size: 16px; 
                }
                button { 
                    background: linear-gradient(135deg, #7877c6, #ff77c6);
                    color: #fff; 
                    border: none; 
                    padding: 15px 40px; 
                    font-weight: bold; 
                    cursor: pointer; 
                    border-radius: 10px; 
                    font-size: 16px;
                    transition: all 0.3s;
                }
                button:hover { 
                    transform: translateY(-2px);
                    box-shadow: 0 10px 30px rgba(120, 119, 198, 0.4);
                }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h1>⚡ BPW FORENSIC</h1>
                <form method="POST" action="/login">
                    <input type="password" name="password" placeholder="Enter Admin Password" required><br>
                    <button type="submit">Login</button>
                </form>
            </div>
        </body>
        </html>
    """)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/generate-pin', methods=['GET'])
def generate_pin():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    pin = ''.join(random.choices(string.digits, k=6))
    sessions[pin] = {"status": "waiting", "logs": None}
    return jsonify({"pin": pin})

@app.route('/api/check-pin/<pin>', methods=['GET'])
def check_pin(pin):
    if pin in sessions and sessions[pin]["status"] == "waiting":
        return jsonify({"status": "valid"}), 200
    return jsonify({"status": "invalid"}), 404

@app.route('/api/submit-logs/<pin>', methods=['POST'])
def submit_logs(pin):
    if pin in sessions:
        sessions[pin]["logs"] = request.json
        sessions[pin]["status"] = "completed"
        return jsonify({"status": "received"}), 200
    return jsonify({"status": "invalid pin"}), 404

@app.route('/api/get-logs/<pin>', methods=['GET'])
def get_logs(pin):
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    if pin in sessions:
        if sessions[pin]["logs"]:
            return jsonify({"status": "success", "logs": sessions[pin]["logs"]})
        else:
            return jsonify({"status": "waiting", "message": "Scan not completed yet. Tell them to run the scanner!"})
    return jsonify({"status": "error", "message": "Invalid code."}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
