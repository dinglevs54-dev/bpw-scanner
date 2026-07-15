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
    <title>BPW - Forensic Scanner</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0a0a0a;
            color: #e0e0e0;
            display: flex;
            min-height: 100vh;
        }
        
        /* Sidebar */
        .sidebar {
            width: 260px;
            background-color: #0d1117;
            border-right: 1px solid #1a1d24;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }
        
        .sidebar-header {
            padding: 20px;
            border-bottom: 1px solid #1a1d24;
        }
        
        .sidebar-header h1 {
            color: #00ff9d;
            font-size: 24px;
            letter-spacing: 1px;
        }
        
        .nav-item {
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s;
            border-left: 3px solid transparent;
            color: #888;
        }
        
        .nav-item:hover {
            background-color: #1a1d24;
            color: #fff;
        }
        
        .nav-item.active {
            background-color: #0d2818;
            border-left-color: #00ff9d;
            color: #00ff9d;
        }
        
        .nav-icon {
            font-size: 18px;
            width: 24px;
            text-align: center;
        }
        
        /* Main Content */
        .main-content {
            margin-left: 260px;
            flex: 1;
            padding: 30px;
        }
        
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #00ff9d;
        }
        
        .top-bar h2 {
            color: #fff;
            font-size: 28px;
        }
        
        .top-stats {
            display: flex;
            gap: 15px;
        }
        
        .stat-badge {
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stat-badge.warnings {
            background-color: #f59e0b;
            color: #000;
        }
        
        .stat-badge.detections {
            background-color: #dc2626;
            color: #fff;
        }
        
        /* Page Content */
        .page {
            display: none;
        }
        
        .page.active {
            display: block;
        }
        
        /* Overview Stats */
        .overview-container {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background-color: #0d1117;
            border: 1px solid #1a1d24;
            border-radius: 12px;
            padding: 30px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .stat-card {
            padding: 25px;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .stat-card.detections {
            background-color: #dc2626;
        }
        
        .stat-card.warnings {
            background-color: #f59e0b;
        }
        
        .stat-card.information {
            background-color: #0ea5e9;
        }
        
        .stat-card.total {
            background-color: #1a1d24;
            border: 1px solid #2a2d34;
        }
        
        .stat-card-title {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .stat-card-value {
            font-size: 36px;
            font-weight: bold;
        }
        
        /* Two Column Layout */
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .column {
            background-color: #0d1117;
            border: 1px solid #1a1d24;
            border-radius: 12px;
            padding: 25px;
        }
        
        .column-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #00ff9d;
        }
        
        .column-title {
            font-size: 20px;
            color: #fff;
        }
        
        /* Collapsible Sections */
        .collapsible-section {
            background-color: #1a1d24;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
        }
        
        .collapsible-header {
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .collapsible-header:hover {
            background-color: #22252c;
        }
        
        .collapsible-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
        }
        
        .collapsible-arrow {
            transition: transform 0.3s;
        }
        
        .collapsible-section.open .collapsible-arrow {
            transform: rotate(90deg);
        }
        
        .collapsible-content {
            display: none;
            padding: 0 20px 20px;
        }
        
        .collapsible-section.open .collapsible-content {
            display: block;
        }
        
        .item-count {
            background-color: #2a2d34;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            color: #888;
        }
        
        /* Log Items */
        .log-item {
            background-color: #0d1117;
            border: 1px solid #1a1d24;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
        }
        
        .log-item-title {
            font-weight: 600;
            margin-bottom: 5px;
            color: #fff;
        }
        
        .log-item-path {
            font-size: 13px;
            color: #888;
            margin-bottom: 8px;
            font-family: monospace;
        }
        
        .log-item-meta {
            display: flex;
            gap: 15px;
            align-items: center;
            font-size: 12px;
            color: #888;
        }
        
        /* Badges */
        .badge {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .badge-information {
            background-color: #0ea5e9;
            color: white;
        }
        
        .badge-warning {
            background-color: #f59e0b;
            color: black;
        }
        
        .badge-detection {
            background-color: #dc2626;
            color: white;
        }
        
        /* Buttons */
        .btn-virustotal {
            background-color: #1a1d24;
            border: 1px solid #00ff9d;
            color: #00ff9d;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            text-decoration: none;
        }
        
        .btn-virustotal:hover {
            background-color: #00ff9d;
            color: #0a0a0a;
        }
        
        .btn-generate {
            background-color: #00ff9d;
            color: #0a0a0a;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 30px;
        }
        
        .btn-generate:hover {
            background-color: #00cc7d;
        }
        
        .btn-fetch {
            background-color: #00ff9d;
            color: #0a0a0a;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
        }
        
        .btn-fetch:hover {
            background-color: #00cc7d;
        }
        
        /* Input */
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        .input-group input {
            flex: 1;
            background-color: #0a0a0a;
            border: 1px solid #2a2d34;
            color: #fff;
            padding: 12px;
            border-radius: 6px;
            font-size: 16px;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #00ff9d;
        }
        
        #pin-display {
            font-size: 48px;
            color: #00ff9d;
            font-weight: bold;
            letter-spacing: 10px;
            text-align: center;
            background: #000;
            padding: 30px;
            border-radius: 12px;
            margin: 20px 0;
            border: 2px solid #00ff9d;
        }
        
        #log-output {
            white-space: pre-wrap;
            background: #0d1117;
            padding: 20px;
            border-radius: 8px;
            max-height: 600px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 13px;
            border: 1px solid #1a1d24;
        }
        
        .empty-state {
            background-color: #0d1117;
            border: 1px solid #1a1d24;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            color: #888;
        }
        
        .logout {
            background-color: #dc2626;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 14px;
        }
        
        .logout:hover {
            background-color: #b91c1c;
        }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>BPW // FORENSIC</h1>
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
            <span>Suspicious Entries</span>
        </div>
        
        <div class="nav-item" onclick="showPage('accounts')">
            <span class="nav-icon">👤</span>
            <span>Alt Accounts</span>
        </div>
        
        <div class="nav-item" onclick="showPage('tools')">
            <span class="nav-icon">🔧</span>
            <span>Tools</span>
        </div>
        
        <div style="padding: 20px;">
            <a href="/logout" class="logout">Logout</a>
        </div>
    </div>
    
    <!-- Main Content -->
    <div class="main-content">
        <div class="top-bar">
            <h2 id="page-title">Overview</h2>
            <div class="top-stats">
                <div class="stat-badge warnings">
                    <span>️</span>
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
            <div class="overview-container">
                <div class="chart-container">
                    <canvas id="pieChart"></canvas>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card detections">
                        <div class="stat-card-title">Detections</div>
                        <div class="stat-card-value" id="stat-detections">0</div>
                    </div>
                    
                    <div class="stat-card warnings">
                        <div class="stat-card-title">Warnings</div>
                        <div class="stat-card-value" id="stat-warnings">0</div>
                    </div>
                    
                    <div class="stat-card information">
                        <div class="stat-card-title">Information</div>
                        <div class="stat-card-value" id="stat-information">0</div>
                    </div>
                    
                    <div class="stat-card total">
                        <div class="stat-card-title">Total Logs</div>
                        <div class="stat-card-value" id="stat-total">0</div>
                    </div>
                </div>
            </div>
            
            <div class="column">
                <div class="column-header">
                    <h3 class="column-title">Generate Access Code</h3>
                </div>
                <button class="btn-generate" onclick="generatePin()">Generate New Code</button>
                <div id="pin-display">------</div>
                <p style="color: #888; text-align: center;">Give this 6-digit code to the person you're scanning</p>
            </div>
            
            <div class="column" style="margin-top: 30px;">
                <div class="column-header">
                    <h3 class="column-title">Retrieve Logs</h3>
                </div>
                <div class="input-group">
                    <input type="text" id="fetch-pin" placeholder="Enter 6-digit code" maxlength="6">
                    <button class="btn-fetch" onclick="fetchLogs()">Fetch Logs</button>
                </div>
                <div id="log-output">Logs will appear here...</div>
            </div>
        </div>
        
        <!-- General Info Page -->
        <div id="page-general" class="page">
            <div class="two-column">
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">General Information</h3>
                    </div>
                    <div id="general-info-content">
                        <div class="empty-state">No data available. Fetch logs first.</div>
                    </div>
                </div>
                
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">Key Indications</h3>
                    </div>
                    <div id="key-indications-content">
                        <div class="empty-state">No data available. Fetch logs first.</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- System Page -->
        <div id="page-system" class="page">
            <div class="two-column">
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">Devices Removed</h3>
                    </div>
                    <div class="empty-state">No logs found</div>
                </div>
                
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">Windows Defender History</h3>
                    </div>
                    <div class="empty-state">No logs found</div>
                </div>
            </div>
        </div>
        
        <!-- File Activity Page -->
        <div id="page-files" class="page">
            <div class="two-column">
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">Cheats Found</h3>
                    </div>
                    <div id="cheats-found-content">
                        <div class="empty-state">No logs found</div>
                    </div>
                </div>
                
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">Suspicious Executed Files Since User Logon</h3>
                    </div>
                    <div id="suspicious-executed-content">
                        <div class="empty-state">No logs found</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Suspicious Entries Page -->
        <div id="page-suspicious" class="page">
            <div class="two-column">
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">Deleted Executables</h3>
                    </div>
                    <div id="deleted-executables-content">
                        <div class="empty-state">No logs found</div>
                    </div>
                </div>
                
                <div class="column">
                    <div class="column-header">
                        <h3 class="column-title">Possible Suspicious Files</h3>
                    </div>
                    <div id="suspicious-files-content">
                        <div class="empty-state">No logs found</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Alt Accounts Page -->
        <div id="page-accounts" class="page">
            <div class="column">
                <div class="column-header">
                    <h3 class="column-title">Alternative Discord Accounts</h3>
                </div>
                <div id="alt-accounts-content">
                    <div class="empty-state">No logs found</div>
                </div>
            </div>
        </div>
        
        <!-- Tools Page -->
        <div id="page-tools" class="page">
            <div class="column">
                <div class="column-header">
                    <h3 class="column-title">Tools</h3>
                </div>
                <p style="color: #888; margin: 20px 0;">Use the Overview page to generate codes and fetch logs.</p>
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
            
            const titles = {
                'overview': 'Overview',
                'general': 'General Info',
                'system': 'System',
                'files': 'File Activity',
                'suspicious': 'Suspicious Entries',
                'accounts': 'Alt Accounts',
                'tools': 'Tools'
            };
            document.getElementById('page-title').innerText = titles[pageId];
            
            if (pageId === 'overview' && currentLogs) {
                updateOverview(currentLogs);
            }
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
            output.innerText = "Fetching...";
            
            try {
                const res = await fetch(`/api/get-logs/${pin}`);
                const data = await res.json();
                
                if (data.status === 'success') {
                    currentLogs = data.logs;
                    output.innerText = "Logs loaded successfully! Check the Overview and other tabs.";
                    updateOverview(data.logs);
                    populateAllPages(data.logs);
                } else {
                    output.innerText = "Error: " + data.message;
                }
            } catch (e) {
                output.innerText = "Error fetching logs: " + e;
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
                        backgroundColor: ['#dc2626', '#f59e0b', '#0ea5e9'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#fff', padding: 20 }
                        }
                    }
                }
            });
        }
        
        function populateAllPages(logs) {
            if (!logs.findings) return;
            
            // Group findings by type
            const grouped = {};
            logs.findings.forEach(finding => {
                const type = finding.type || 'Other';
                if (!grouped[type]) grouped[type] = [];
                grouped[type].push(finding);
            });
            
            // Populate General Info
            const generalContent = document.getElementById('general-info-content');
            const keyIndicationsContent = document.getElementById('key-indications-content');
            
            let generalHTML = '';
            let keyHTML = '';
            
            Object.entries(grouped).forEach(([type, items]) => {
                const severity = items[0].severity || 'INFO';
                const badgeClass = severity === 'CRITICAL' || severity === 'HIGH' ? 'badge-detection' : 
                                   severity === 'MEDIUM' ? 'badge-warning' : 'badge-information';
                
                const section = `
                    <div class="collapsible-section open">
                        <div class="collapsible-header" onclick="this.parentElement.classList.toggle('open')">
                            <div class="collapsible-title">
                                <span class="collapsible-arrow">›</span>
                                <span>${type}</span>
                                <span class="item-count">${items.length} items</span>
                            </div>
                            <span class="badge ${badgeClass}">${severity}</span>
                        </div>
                        <div class="collapsible-content">
                            ${items.map(item => `
                                <div class="log-item">
                                    <div class="log-item-title">${item.file || 'Unknown'}</div>
                                    <div class="log-item-path">${item.path || item.reason || ''}</div>
                                    <div class="log-item-meta">
                                        <span>⏱️ ${item.timestamp || logs.timestamp || ''}</span>
                                        ${item.hash ? `<span>🔐 ${item.hash.substring(0, 16)}...</span>` : ''}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
                
                if (type.includes('Discord') || type.includes('Process') || type.includes('Device')) {
                    keyHTML += section;
                } else {
                    generalHTML += section;
                }
            });
            
            generalContent.innerHTML = generalHTML || '<div class="empty-state">No general information found</div>';
            keyIndicationsContent.innerHTML = keyHTML || '<div class="empty-state">No key indications found</div>';
            
            // Populate File Activity
            const cheatsFound = logs.findings.filter(f => 
                f.type.includes('Cheat') || f.type.includes('Suspicious File')
            );
            document.getElementById('cheats-found-content').innerHTML = cheatsFound.length > 0 ? 
                cheatsFound.map(f => `
                    <div class="log-item">
                        <div class="log-item-title">${f.file}</div>
                        <div class="log-item-path">${f.path || ''}</div>
                        <div class="log-item-meta">
                            <span class="badge badge-${f.severity === 'CRITICAL' || f.severity === 'HIGH' ? 'detection' : 'warning'}">${f.severity}</span>
                            ${f.hash ? `<a href="https://www.virustotal.com/gui/file/${f.hash}" target="_blank" class="btn-virustotal"> VirusTotal</a>` : ''}
                        </div>
                    </div>
                `).join('') : '<div class="empty-state">No cheats found</div>';
            
            // Populate Suspicious Entries
            const deletedExes = logs.findings.filter(f => f.type.includes('Deleted'));
            const suspiciousFiles = logs.findings.filter(f => 
                f.type.includes('Suspicious') && !f.type.includes('Deleted')
            );
            
            document.getElementById('deleted-executables-content').innerHTML = deletedExes.length > 0 ?
                deletedExes.map(f => `
                    <div class="log-item">
                        <div class="log-item-title">${f.file}</div>
                        <div class="log-item-path">${f.path || ''}</div>
                        <div class="log-item-meta">
                            <span>⏱️ ${f.timestamp || 'Unknown'}</span>
                            <span class="badge badge-information">INFO</span>
                        </div>
                    </div>
                `).join('') : '<div class="empty-state">No deleted executables found</div>';
            
            document.getElementById('suspicious-files-content').innerHTML = suspiciousFiles.length > 0 ?
                suspiciousFiles.map(f => `
                    <div class="log-item">
                        <div class="log-item-title">${f.file}</div>
                        <div class="log-item-path">${f.path || f.reason || ''}</div>
                        <div class="log-item-meta">
                            <span class="badge badge-warning">WARNING</span>
                            ${f.hash ? `<a href="https://www.virustotal.com/gui/file/${f.hash}" target="_blank" class="btn-virustotal">🔍 VirusTotal</a>` : ''}
                        </div>
                    </div>
                `).join('') : '<div class="empty-state">No suspicious files found</div>';
            
            // Populate Alt Accounts
            const discordAccounts = logs.findings.filter(f => f.type.includes('Discord'));
            document.getElementById('alt-accounts-content').innerHTML = discordAccounts.length > 0 ?
                discordAccounts.map(f => `
                    <div class="log-item">
                        <div class="log-item-title">${f.file}</div>
                        <div class="log-item-path">${f.reason || ''}</div>
                        <div class="log-item-meta">
                            <span class="badge badge-information">INFO</span>
                        </div>
                    </div>
                `).join('') : '<div class="empty-state">No alternative accounts found</div>';
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
        else:
            return render_template_string("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>BPW Login</title>
                    <style>
                        body { background: #0a0a0a; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                        .login-box { background: #1a1d24; padding: 40px; border-radius: 12px; border: 2px solid #00ff9d; text-align: center; }
                        h1 { color: #00ff9d; margin-bottom: 30px; }
                        input { background: #0a0a0a; border: 1px solid #333; color: #fff; padding: 12px; border-radius: 6px; width: 250px; margin-bottom: 20px; font-size: 16px; }
                        button { background: #00ff9d; color: #000; border: none; padding: 12px 30px; font-weight: bold; cursor: pointer; border-radius: 6px; font-size: 16px; }
                        button:hover { background: #00cc7d; }
                        .error { color: #ff4757; margin-bottom: 20px; }
                    </style>
                </head>
                <body>
                    <div class="login-box">
                        <h1>BPW // ADMIN LOGIN</h1>
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
                body { background: #0a0a0a; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-box { background: #1a1d24; padding: 40px; border-radius: 12px; border: 2px solid #00ff9d; text-align: center; }
                h1 { color: #00ff9d; margin-bottom: 30px; }
                input { background: #0a0a0a; border: 1px solid #333; color: #fff; padding: 12px; border-radius: 6px; width: 250px; margin-bottom: 20px; font-size: 16px; }
                button { background: #00ff9d; color: #000; border: none; padding: 12px 30px; font-weight: bold; cursor: pointer; border-radius: 6px; font-size: 16px; }
                button:hover { background: #00cc7d; }
                .error { color: #ff4757; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h1>BPW // ADMIN LOGIN</h1>
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
