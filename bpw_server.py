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
    <title>BPW // FORENSIC SCANNER</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            min-height: 100vh;
        }
        .sidebar {
            width: 280px;
            background: rgba(15, 12, 41, 0.8);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            position: fixed;
            height: 100vh;
            padding: 30px 0;
            overflow-y: auto;
        }
        .sidebar-header {
            padding: 0 25px 30px;
            border-bottom: 2px solid rgba(120, 119, 198, 0.3);
        }
        .sidebar-header h1 {
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 28px;
            font-weight: 800;
        }
        .sidebar-header p { color: #888; font-size: 12px; margin-top: 5px; }
        .nav-item {
            padding: 15px 25px;
            margin: 5px 15px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 15px;
            border-radius: 12px;
            color: #888;
            font-weight: 600;
            transition: all 0.3s;
        }
        .nav-item:hover { background: rgba(120, 119, 198, 0.1); color: #fff; }
        .nav-item.active {
            background: linear-gradient(135deg, rgba(120, 119, 198, 0.3), rgba(255, 119, 198, 0.3));
            color: #fff;
        }
        .main-content { margin-left: 280px; padding: 40px; }
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding: 20px 30px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .top-bar h2 {
            background: linear-gradient(135deg, #fff, #7877c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 32px;
        }
        .stat-badge {
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-left: 10px;
        }
        .stat-badge.detections { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; }
        .stat-badge.warnings { background: linear-gradient(135deg, #f59e0b, #f97316); color: #fff; }
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
        }
        .stat-card.detections { border-left: 4px solid #ef4444; }
        .stat-card.warnings { border-left: 4px solid #f59e0b; }
        .stat-card.information { border-left: 4px solid #06b6d4; }
        .stat-card-title { font-size: 14px; color: #888; margin-bottom: 10px; text-transform: uppercase; }
        .stat-card-value { font-size: 48px; font-weight: 800; color: #fff; }
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
        }
        .panel-header {
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 2px solid rgba(120, 119, 198, 0.3);
        }
        .panel-title { font-size: 22px; font-weight: 700; color: #fff; }
        .btn-primary {
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            color: #fff;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 700;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(120, 119, 198, 0.4); }
        .code-display {
            background: linear-gradient(135deg, rgba(15, 12, 41, 0.8), rgba(48, 43, 99, 0.8));
            border: 2px solid rgba(120, 119, 198, 0.5);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
        }
        .code-value {
            font-size: 64px;
            font-weight: 800;
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 10px;
        }
        .input-group { display: flex; gap: 15px; margin: 20px 0; }
        .input-group input {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 15px 20px;
            border-radius: 12px;
            font-size: 16px;
        }
        .log-output {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(120, 119, 198, 0.3);
            border-radius: 12px;
            padding: 20px;
            max-height: 500px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }
        .chart-container { position: relative; height: 300px; margin: 20px 0; }
        .page { display: none; animation: fadeIn 0.5s; }
        .page.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        .finding-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .finding-card.critical { border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.05); }
        .finding-card.high { border-left: 4px solid #f97316; background: rgba(249, 115, 22, 0.05); }
        .finding-card.medium { border-left: 4px solid #f59e0b; background: rgba(245, 158, 11, 0.05); }
        .finding-card.info { border-left: 4px solid #06b6d4; }
        
        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .finding-title { font-weight: 700; color: #fff; font-size: 16px; }
        .badge {
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .badge-critical { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; }
        .badge-high { background: linear-gradient(135deg, #f97316, #ea580c); color: #fff; }
        .badge-medium { background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; }
        .badge-info { background: linear-gradient(135deg, #06b6d4, #0891b2); color: #fff; }
        
        .finding-detail { color: #888; font-size: 14px; margin: 8px 0; }
        .finding-path { color: #06b6d4; font-family: 'JetBrains Mono', monospace; font-size: 12px; word-break: break-all; }
        .finding-hash { color: #666; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); }
        
        .section-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .empty-state { color: #666; text-align: center; padding: 60px 20px; }
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
        .logout-btn:hover { background: rgba(239, 68, 68, 0.3); transform: translateY(-2px); }
        .info-box {
            background: rgba(120, 119, 198, 0.1);
            border: 1px solid rgba(120, 119, 198, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .info-item { margin-bottom: 10px; }
        .info-label { color: #888; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }
        .info-value { color: #fff; font-weight: 600; font-size: 16px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>⚡ BPW</h1>
            <p>FORENSIC SCANNER v2.0</p>
        </div>
        <div class="nav-item active" onclick="showPage('overview')">
            <span>📊</span><span>Overview</span>
        </div>
        <div class="nav-item" onclick="showPage('general')">
            <span>ℹ️</span><span>General Info</span>
        </div>
        <div class="nav-item" onclick="showPage('files')">
            <span></span><span>File Activity</span>
        </div>
        <div class="nav-item" onclick="showPage('suspicious')">
            <span>⚠️</span><span>Suspicious</span>
        </div>
        <div class="nav-item" onclick="showPage('accounts')">
            <span></span><span>Alt Accounts</span>
        </div>
        <a href="/logout" class="logout-btn"> Logout</a>
    </div>
    
    <div class="main-content">
        <div class="top-bar">
            <h2>🎯 Overview</h2>
            <div>
                <span class="stat-badge warnings">️ <span id="top-warnings">0</span></span>
                <span class="stat-badge detections">🎯 <span id="top-detections">0</span></span>
            </div>
        </div>
        
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
                    <div class="stat-card-title">️ Information</div>
                    <div class="stat-card-value" id="stat-information">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"> Total Logs</div>
                    <div class="stat-card-value" id="stat-total">0</div>
                </div>
            </div>
            
            <div class="main-grid">
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title"> Generate Access Code</div></div>
                    <button class="btn-primary" onclick="generatePin()">Generate New Code</button>
                    <div class="code-display">
                        <div style="color: #888; margin-bottom: 10px; font-size: 14px;">YOUR 6-DIGIT CODE</div>
                        <div class="code-value" id="pin-display">------</div>
                    </div>
                    <p style="color: #888; text-align: center; font-size: 14px;">Share this code with the target PC</p>
                </div>
                
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title">📥 Retrieve Logs</div></div>
                    <div class="input-group">
                        <input type="text" id="fetch-pin" placeholder="Enter 6-digit code" maxlength="6">
                        <button class="btn-primary" style="width: auto;" onclick="fetchLogs()">Fetch</button>
                    </div>
                    <div id="log-output" class="log-output">
                        <div style="color: #666; text-align: center; padding: 40px;">Logs will appear here after fetching...</div>
                    </div>
                </div>
            </div>
            
            <div class="glass-panel">
                <div class="panel-header"><div class="panel-title">📈 Threat Analysis</div></div>
                <div class="chart-container"><canvas id="pieChart"></canvas></div>
            </div>
        </div>
        
        <div id="page-general" class="page">
            <div class="glass-panel">
                <div class="panel-header"><div class="panel-title">ℹ️ General Information</div></div>
                <div id="general-content">
                    <div class="empty-state">Fetch logs from Overview to see system information</div>
                </div>
            </div>
        </div>
        
        <div id="page-files" class="page">
            <div class="section-grid">
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title">📄 Suspicious Files</div></div>
                    <div id="files-content">
                        <div class="empty-state">No suspicious files found</div>
                    </div>
                </div>
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title">🗑️ Deleted Executables</div></div>
                    <div id="deleted-content">
                        <div class="empty-state">No deleted executables found</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="page-suspicious" class="page">
            <div class="section-grid">
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title">️ Processes</div></div>
                    <div id="processes-content">
                        <div class="empty-state">No suspicious processes found</div>
                    </div>
                </div>
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title">💾 DMA Devices</div></div>
                    <div id="dma-content">
                        <div class="empty-state">No suspicious DMA devices found</div>
                    </div>
                </div>
            </div>
            <div class="glass-panel" style="margin-top: 20px;">
                <div class="panel-header"><div class="panel-title">📀 Prefetch Artifacts</div></div>
                <div id="prefetch-content">
                    <div class="empty-state">No prefetch artifacts found</div>
                </div>
            </div>
        </div>
        
        <div id="page-accounts" class="page">
            <div class="glass-panel">
                <div class="panel-header"><div class="panel-title">👤 Discord Accounts</div></div>
                <div id="discord-content">
                    <div class="empty-state">No Discord accounts or modifications found</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentLogs = null;
        let pieChart = null;
        
        function showPage(pageId) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('page-' + pageId).classList.add('active');
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
            output.innerHTML = '<div style="color:#7877c6;text-align:center;padding:40px;">⏳ Fetching logs...</div>';
            
            try {
                const res = await fetch('/api/get-logs/' + pin);
                const data = await res.json();
                
                if (data.status === 'success') {
                    currentLogs = data.logs;
                    updateOverview(data.logs);
                    populateAllSections(data.logs);
                    output.innerHTML = '<div style="color:#06b6d4;text-align:center;padding:20px;">✅ Logs loaded!<br>Click on sidebar sections to view findings.</div>';
                } else {
                    output.innerText = "❌ Error: " + data.message;
                }
            } catch (e) {
                output.innerText = "❌ Connection error: " + e;
            }
        }
        
        function updateOverview(logs) {
            let detections = 0, warnings = 0, information = 0;
            
            if (logs.findings) {
                logs.findings.forEach(f => {
                    const s = (f.severity || 'INFO').toUpperCase();
                    if (s === 'CRITICAL' || s === 'HIGH') detections++;
                    else if (s === 'MEDIUM') warnings++;
                    else information++;
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
        
        function createFindingCard(item) {
            const severity = (item.severity || 'INFO').toUpperCase();
            const sevClass = severity === 'CRITICAL' ? 'critical' : 
                            severity === 'HIGH' ? 'high' : 
                            severity === 'MEDIUM' ? 'medium' : 'info';
            const badgeClass = 'badge-' + sevClass;
            
            let html = '<div class="finding-card ' + sevClass + '">';
            html += '<div class="finding-header">';
            html += '<div class="finding-title">' + (item.type || 'Finding') + '</div>';
            html += '<span class="badge ' + badgeClass + '">' + severity + '</span>';
            html += '</div>';
            
            if (item.file) {
                html += '<div class="finding-detail" style="color:#fff;margin:8px 0;">📄 ' + item.file + '</div>';
            }
            if (item.reason) {
                html += '<div class="finding-detail" style="color:#888;margin:5px 0;">' + item.reason + '</div>';
            }
            if (item.path) {
                html += '<div class="finding-path">📍 ' + item.path + '</div>';
            }
            if (item.hash) {
                html += '<div class="finding-hash">🔐 ' + item.hash + '</div>';
            }
            if (item.timestamp) {
                html += '<div class="finding-detail" style="color:#06b6d4;margin:5px 0;">⏰ ' + item.timestamp + '</div>';
            }
            if (item.note) {
                html += '<div class="finding-detail" style="color:#f59e0b;margin:5px 0;">️ ' + item.note + '</div>';
            }
            
            html += '</div>';
            return html;
        }
        
        function populateAllSections(logs) {
            if (!logs.findings || logs.findings.length === 0) {
                console.log('No findings to display');
                return;
            }
            
            console.log('Populating sections with', logs.findings.length, 'findings');
            
            const categories = {
                discord: [],
                files: [],
                deleted: [],
                processes: [],
                dma: [],
                prefetch: [],
                logs: [],
                general: []
            };
            
            logs.findings.forEach(f => {
                const type = (f.type || '').toLowerCase();
                
                if (type.includes('discord')) {
                    categories.discord.push(f);
                } else if (type.includes('deleted')) {
                    categories.deleted.push(f);
                } else if (type.includes('process')) {
                    categories.processes.push(f);
                } else if (type.includes('dma') || type.includes('device')) {
                    categories.dma.push(f);
                } else if (type.includes('prefetch')) {
                    categories.prefetch.push(f);
                } else if (type.includes('log')) {
                    categories.logs.push(f);
                } else if (type.includes('file')) {
                    categories.files.push(f);
                } else {
                    categories.general.push(f);
                }
            });
            
            console.log('Categories:', {
                discord: categories.discord.length,
                files: categories.files.length,
                deleted: categories.deleted.length,
                processes: categories.processes.length,
                dma: categories.dma.length,
                prefetch: categories.prefetch.length,
                logs: categories.logs.length,
                general: categories.general.length
            });
            
            // General Info
            const generalDiv = document.getElementById('general-content');
            if (generalDiv) {
                let html = '<div class="info-box"><div class="info-grid">';
                html += '<div class="info-item"><div class="info-label">📅 Scan Time</div><div class="info-value">' + (logs.timestamp || 'N/A') + '</div></div>';
                html += '<div class="info-item"><div class="info-label">💻 Hostname</div><div class="info-value">' + (logs.hostname || 'Unknown') + '</div></div>';
                html += '<div class="info-item"><div class="info-label"> Username</div><div class="info-value">' + (logs.username || 'Unknown') + '</div></div>';
                html += '<div class="info-item"><div class="info-label">📊 Total Findings</div><div class="info-value">' + (logs.total_findings || 0) + '</div></div>';
                html += '</div></div>';
                
                if (categories.logs.length > 0) {
                    html += '<h3 style="color:#fff;margin:20px 0 15px;">⚠️ Log Tampering</h3>';
                    categories.logs.forEach(item => { html += createFindingCard(item); });
                }
                
                if (categories.general.length > 0) {
                    html += '<h3 style="color:#fff;margin:20px 0 15px;"> Other Findings</h3>';
                    categories.general.forEach(item => { html += createFindingCard(item); });
                }
                
                if (categories.logs.length === 0 && categories.general.length === 0) {
                    html += '<div class="empty-state">No general findings</div>';
                }
                
                generalDiv.innerHTML = html;
            }
            
            // Files
            const filesDiv = document.getElementById('files-content');
            if (filesDiv) {
                if (categories.files.length > 0) {
                    let html = '';
                    categories.files.forEach(f => { html += createFindingCard(f); });
                    filesDiv.innerHTML = html;
                } else {
                    filesDiv.innerHTML = '<div class="empty-state">No suspicious files found</div>';
                }
            }
            
            // Deleted
            const deletedDiv = document.getElementById('deleted-content');
            if (deletedDiv) {
                if (categories.deleted.length > 0) {
                    let html = '';
                    categories.deleted.forEach(f => {
                        html += '<div class="finding-card info">';
                        html += '<div class="finding-header"><div class="finding-title">🗑️ ' + (f.file || 'Unknown') + '</div><span class="badge badge-info">DELETED</span></div>';
                        if (f.reason) html += '<div class="finding-detail">' + f.reason + '</div>';
                        if (f.timestamp) html += '<div class="finding-detail" style="color:#06b6d4;">⏰ ' + f.timestamp + '</div>';
                        if (f.note) html += '<div class="finding-detail" style="color:#f59e0b;">️ ' + f.note + '</div>';
                        html += '</div>';
                    });
                    deletedDiv.innerHTML = html;
                } else {
                    deletedDiv.innerHTML = '<div class="empty-state">No deleted executables found</div>';
                }
            }
            
            // Processes
            const processesDiv = document.getElementById('processes-content');
            if (processesDiv) {
                if (categories.processes.length > 0) {
                    let html = '';
                    categories.processes.forEach(f => { html += createFindingCard(f); });
                    processesDiv.innerHTML = html;
                } else {
                    processesDiv.innerHTML = '<div class="empty-state">No suspicious processes found</div>';
                }
            }
            
            // DMA
            const dmaDiv = document.getElementById('dma-content');
            if (dmaDiv) {
                if (categories.dma.length > 0) {
                    let html = '';
                    categories.dma.forEach(f => {
                        html += '<div class="finding-card critical">';
                        html += '<div class="finding-header"><div class="finding-title">🔌 ' + (f.file || 'Unknown Device') + '</div><span class="badge badge-critical">CRITICAL</span></div>';
                        if (f.reason) html += '<div class="finding-detail">' + f.reason + '</div>';
                        if (f.device_id) html += '<div class="finding-detail" style="color:#888;font-family:monospace;">ID: ' + f.device_id + '</div>';
                        html += '</div>';
                    });
                    dmaDiv.innerHTML = html;
                } else {
                    dmaDiv.innerHTML = '<div class="empty-state">No suspicious DMA devices found</div>';
                }
            }
            
            // Prefetch
            const prefetchDiv = document.getElementById('prefetch-content');
            if (prefetchDiv) {
                if (categories.prefetch.length > 0) {
                    let html = '';
                    categories.prefetch.forEach(f => { html += createFindingCard(f); });
                    prefetchDiv.innerHTML = html;
                } else {
                    prefetchDiv.innerHTML = '<div class="empty-state">No prefetch artifacts found</div>';
                }
            }
            
            // Discord
            const discordDiv = document.getElementById('discord-content');
            if (discordDiv) {
                if (categories.discord.length > 0) {
                    let html = '';
                    categories.discord.forEach(f => { html += createFindingCard(f); });
                    discordDiv.innerHTML = html;
                } else {
                    discordDiv.innerHTML = '<div class="empty-state">No Discord accounts or modifications found</div>';
                }
            }
            
            console.log('Sections populated successfully');
        }
        
        function drawPieChart(d, w, i) {
            const ctx = document.getElementById('pieChart').getContext('2d');
            if (pieChart) pieChart.destroy();
            
            const total = d + w + i;
            if (total === 0) {
                document.querySelector('.chart-container').innerHTML = '<div style="color:#666;text-align:center;padding:40px;">No data to display</div>';
                return;
            }
            
            pieChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Detections', 'Warnings', 'Information'],
                    datasets: [{
                        data: [d, w, i],
                        backgroundColor: ['rgba(239,68,68,0.8)', 'rgba(245,158,11,0.8)', 'rgba(6,182,212,0.8)'],
                        borderColor: ['rgba(239,68,68,1)', 'rgba(245,158,11,1)', 'rgba(6,182,212,1)'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { position: 'bottom', labels: { color: '#fff', font: { family: 'Inter', size: 14 } } }
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
    return render_template_string(PROFESSIONAL_DASHBOARD)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template_string('<!DOCTYPE html><html><head><style>body{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:sans-serif}.box{background:rgba(255,255,255,0.03);padding:50px;border-radius:20px;border:2px solid rgba(120,119,198,0.3);text-align:center}h1{background:linear-gradient(135deg,#7877c6,#ff77c6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:30px}input{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.2);color:#fff;padding:15px;border-radius:10px;width:300px;margin-bottom:20px;font-size:16px}button{background:linear-gradient(135deg,#7877c6,#ff77c6);color:#fff;border:none;padding:15px 40px;font-weight:bold;cursor:pointer;border-radius:10px;font-size:16px}.error{color:#ef4444;margin-bottom:20px}</style></head><body><div class="box"><h1>⚡ BPW FORENSIC</h1>{% if error %}<div class="error">{{error}}</div>{% endif %}<form method="POST"><input type="password" name="password" placeholder="Password" required><button>Login</button></form></div></body></html>', error="Wrong password!" if request.form else None)
    return render_template_string('<!DOCTYPE html><html><head><style>body{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:sans-serif}.box{background:rgba(255,255,255,0.03);padding:50px;border-radius:20px;border:2px solid rgba(120,119,198,0.3);text-align:center}h1{background:linear-gradient(135deg,#7877c6,#ff77c6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:30px}input{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.2);color:#fff;padding:15px;border-radius:10px;width:300px;margin-bottom:20px;font-size:16px}button{background:linear-gradient(135deg,#7877c6,#ff77c6);color:#fff;border:none;padding:15px 40px;font-weight:bold;cursor:pointer;border-radius:10px;font-size:16px}</style></head><body><div class="box"><h1>⚡ BPW FORENSIC</h1><form method="POST"><input type="password" name="password" placeholder="Password" required><button>Login</button></form></div></body></html>')

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
        return jsonify({"status": "waiting", "message": "Scan not completed yet"})
    return jsonify({"status": "error", "message": "Invalid code"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
