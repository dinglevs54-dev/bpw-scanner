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
        .stat-badge.warnings { background: linear-gradient(135deg, #f59e0b, #f97316); color: #fff; }
        .stat-badge.detections { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; }
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
        .stat-card-title { font-size: 14px; color: #888; margin-bottom: 10px; }
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
        }
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
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .badge {
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-critical { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; }
        .badge-high { background: linear-gradient(135deg, #f97316, #ea580c); color: #fff; }
        .badge-medium { background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; }
        .badge-info { background: linear-gradient(135deg, #06b6d4, #0891b2); color: #fff; }
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
        }
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
        <div class="nav-item" onclick="showPage('system')">
            <span>🖥️</span><span>System</span>
        </div>
        <div class="nav-item" onclick="showPage('files')">
            <span></span><span>File Activity</span>
        </div>
        <div class="nav-item" onclick="showPage('suspicious')">
            <span>⚠️</span><span>Suspicious</span>
        </div>
        <div class="nav-item" onclick="showPage('accounts')">
            <span>👤</span><span>Alt Accounts</span>
        </div>
        <a href="/logout" class="logout-btn">🚪 Logout</a>
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
                <div class="stat-card"><div class="stat-card-title">🎯 Detections</div><div class="stat-card-value" id="stat-detections">0</div></div>
                <div class="stat-card"><div class="stat-card-title">⚠️ Warnings</div><div class="stat-card-value" id="stat-warnings">0</div></div>
                <div class="stat-card"><div class="stat-card-title">ℹ️ Information</div><div class="stat-card-value" id="stat-information">0</div></div>
                <div class="stat-card"><div class="stat-card-title"> Total Logs</div><div class="stat-card-value" id="stat-total">0</div></div>
            </div>
            
            <div class="main-grid">
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title">Generate Access Code</div></div>
                    <button class="btn-primary" onclick="generatePin()"> Generate New Code</button>
                    <div class="code-display">
                        <div style="color: #888; margin-bottom: 10px;">YOUR 6-DIGIT CODE</div>
                        <div class="code-value" id="pin-display">------</div>
                    </div>
                </div>
                
                <div class="glass-panel">
                    <div class="panel-header"><div class="panel-title">Retrieve Logs</div></div>
                    <div class="input-group">
                        <input type="text" id="fetch-pin" placeholder="Enter 6-digit code" maxlength="6">
                        <button class="btn-primary" style="width: auto;" onclick="fetchLogs()">Fetch</button>
                    </div>
                    <div id="log-output" class="log-output">Logs will appear here...</div>
                </div>
            </div>
            
            <div class="glass-panel">
                <div class="panel-header"><div class="panel-title">Threat Analysis</div></div>
                <div class="chart-container"><canvas id="pieChart"></canvas></div>
            </div>
        </div>
        
        <div id="page-general" class="page">
            <div class="glass-panel"><div id="general-content"><p style="color:#666;text-align:center;padding:40px;">Fetch logs from Overview</p></div></div>
        </div>
        <div id="page-system" class="page">
            <div class="glass-panel"><p style="color:#666;text-align:center;padding:40px;">Fetch logs from Overview</p></div>
        </div>
        <div id="page-files" class="page">
            <div class="glass-panel"><div id="files-content"><p style="color:#666;text-align:center;padding:40px;">Fetch logs from Overview</p></div></div>
        </div>
        <div id="page-suspicious" class="page">
            <div class="glass-panel"><div id="suspicious-content"><p style="color:#666;text-align:center;padding:40px;">Fetch logs from Overview</p></div></div>
        </div>
        <div id="page-accounts" class="page">
            <div class="glass-panel"><div id="accounts-content"><p style="color:#666;text-align:center;padding:40px;">Fetch logs from Overview</p></div></div>
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
            if(pin.length !== 6) { alert("Enter 6-digit code"); return; }
            
            const output = document.getElementById('log-output');
            output.innerHTML = '<div style="color:#7877c6;text-align:center;padding:40px;">Fetching...</div>';
            
            try {
                const res = await fetch('/api/get-logs/' + pin);
                const data = await res.json();
                
                if (data.status === 'success') {
                    currentLogs = data.logs;
                    updateOverview(data.logs);
                    populateSections(data.logs);
                    output.innerHTML = '<div style="color:#06b6d4;text-align:center;padding:20px;">✅ Logs loaded!</div><pre style="color:#fff;margin-top:20px;">' + JSON.stringify(data.logs, null, 2) + '</pre>';
                } else {
                    output.innerText = "Error: " + data.message;
                }
            } catch (e) {
                output.innerText = "Error: " + e;
            }
        }
        
        function updateOverview(logs) {
            let detections = 0, warnings = 0, information = 0;
            if (logs.findings) {
                logs.findings.forEach(f => {
                    const s = f.severity || 'INFO';
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
        
        function populateSections(logs) {
            const cats = { discord: [], files: [], deleted: [], processes: [], general: [] };
            if (logs.findings) {
                logs.findings.forEach(f => {
                    const t = f.type || '';
                    if (t.includes('Discord')) cats.discord.push(f);
                    else if (t.includes('Deleted')) cats.deleted.push(f);
                    else if (t.includes('File')) cats.files.push(f);
                    else if (t.includes('Process')) cats.processes.push(f);
                    else cats.general.push(f);
                });
            }
            
            // General Info
            const gen = document.getElementById('general-content');
            if (gen) {
                let h = '<div style="background:rgba(120,119,198,0.1);padding:20px;border-radius:12px;margin-bottom:20px;">';
                h += '<div style="color:#888;font-size:12px;">Scan Time</div><div style="color:#fff;font-size:18px;">' + (logs.timestamp || 'N/A') + '</div></div>';
                h += '<div style="color:#fff;font-size:18px;margin-bottom:15px;">Findings</div>';
                (cats.general || []).forEach(item => {
                    h += '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:15px;margin-bottom:10px;">';
                    h += '<div style="color:#fff;font-weight:600;">' + item.type + '</div>';
                    h += '<div style="color:#888;font-size:13px;">' + item.file + '</div></div>';
                });
                gen.innerHTML = h;
            }
            
            // Files
            const files = document.getElementById('files-content');
            if (files) {
                let h = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">';
                h += '<div><div style="color:#fff;font-size:18px;margin-bottom:15px;">Suspicious Files</div>';
                (cats.files || []).forEach(f => {
                    h += '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:15px;margin-bottom:10px;">';
                    h += '<div style="color:#fff;font-family:monospace;">' + f.file + '</div>';
                    h += '<div style="color:#f59e0b;font-size:13px;">' + f.reason + '</div></div>';
                });
                h += '</div><div><div style="color:#fff;font-size:18px;margin-bottom:15px;">Deleted Files</div>';
                (cats.deleted || []).forEach(f => {
                    h += '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:15px;margin-bottom:10px;">';
                    h += '<div style="color:#fff;font-family:monospace;">' + f.file + '</div>';
                    h += '<div style="color:#06b6d4;font-size:13px;">' + (f.timestamp || '') + '</div></div>';
                });
                h += '</div></div>';
                files.innerHTML = h;
            }
        }
        
        function drawPieChart(d, w, i) {
            const ctx = document.getElementById('pieChart').getContext('2d');
            if (pieChart) pieChart.destroy();
            if (d + w + i === 0) return;
            pieChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Detections', 'Warnings', 'Information'],
                    datasets: [{
                        data: [d, w, i],
                        backgroundColor: ['rgba(239,68,68,0.8)', 'rgba(245,158,11,0.8)', 'rgba(6,182,212,0.8)'],
                        borderWidth: 2
                    }]
                },
                options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { color: '#fff' } } } }
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
