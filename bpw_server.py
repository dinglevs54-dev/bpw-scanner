# dashboard.py - BPW Forensic Scanner Dashboard (Fixed for Deployment)
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
<html>
<head>
    <title>BPW // FORENSIC SCANNER</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0a0a1a;
            color: #e0e0e0;
            min-height: 100vh;
        }
        .sidebar {
            width: 260px;
            background: #111128;
            position: fixed;
            height: 100vh;
            padding: 30px 0;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        .sidebar h1 {
            padding: 0 25px 30px;
            font-size: 24px;
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .nav-item {
            padding: 14px 25px;
            cursor: pointer;
            color: #666;
            font-weight: 600;
            transition: 0.3s;
        }
        .nav-item:hover { background: rgba(255,255,255,0.03); color: #fff; }
        .nav-item.active { color: #fff; background: rgba(120,119,198,0.1); border-right: 3px solid #7877c6; }
        .main { margin-left: 260px; padding: 30px; }
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 25px;
            background: rgba(255,255,255,0.02);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 30px;
        }
        .top-bar h2 { color: #fff; font-size: 26px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            padding: 25px;
            background: rgba(255,255,255,0.02);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .stat-card .label { color: #666; font-size: 13px; text-transform: uppercase; }
        .stat-card .value { font-size: 36px; font-weight: 800; color: #fff; margin-top: 5px; }
        .stat-card.detections { border-left: 4px solid #ef4444; }
        .stat-card.warnings { border-left: 4px solid #f59e0b; }
        .stat-card.information { border-left: 4px solid #4facfe; }
        .stat-card.total { border-left: 4px solid #7877c6; }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 30px;
        }
        .glass-panel {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 25px;
        }
        .panel-title { color: #fff; font-size: 18px; font-weight: 700; margin-bottom: 20px; }
        .btn-primary {
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            color: #fff;
            border: none;
            padding: 14px;
            font-weight: 700;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            font-size: 15px;
            transition: 0.3s;
        }
        .btn-primary:hover { opacity: 0.85; transform: translateY(-2px); }
        .code-display {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            margin: 20px 0;
            border: 2px solid rgba(120,119,198,0.2);
        }
        .code-value {
            font-size: 48px;
            font-weight: 900;
            font-family: monospace;
            letter-spacing: 10px;
            background: linear-gradient(135deg, #7877c6, #ff77c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .input-group { display: flex; gap: 12px; margin: 15px 0; }
        .input-group input {
            flex: 1;
            padding: 12px 16px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.05);
            color: #fff;
            font-size: 16px;
            letter-spacing: 4px;
        }
        .input-group input:focus { outline: none; border-color: #7877c6; }
        .log-output {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            max-height: 350px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 13px;
            min-height: 120px;
        }
        .empty { color: #666; text-align: center; padding: 30px; }
        .badge {
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-detection { background: rgba(239,68,68,0.2); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); }
        .badge-warning { background: rgba(245,158,11,0.2); color: #f59e0b; border: 1px solid rgba(245,158,11,0.2); }
        .badge-info { background: rgba(79,172,254,0.15); color: #4facfe; border: 1px solid rgba(79,172,254,0.15); }
        .finding-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px 18px;
            margin-bottom: 10px;
        }
        .finding-card.detection { border-left: 4px solid #ef4444; }
        .finding-card.warning { border-left: 4px solid #f59e0b; }
        .finding-card.info { border-left: 4px solid #4facfe; }
        .finding-header { display: flex; justify-content: space-between; align-items: center; }
        .finding-title { font-weight: 600; color: #fff; }
        .finding-detail { color: #888; font-size: 13px; margin-top: 5px; }
        .finding-meta { color: #555; font-size: 11px; margin-top: 5px; }
        .logout-btn {
            padding: 12px 25px;
            background: rgba(239,68,68,0.1);
            border: 1px solid rgba(239,68,68,0.2);
            border-radius: 10px;
            text-align: center;
            margin-top: 30px;
        }
        .logout-btn a { color: #ef4444; text-decoration: none; font-weight: 600; }
        .page { display: none; }
        .page.active { display: block; }
        .chart-container { height: 250px; }
        .section-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) {
            .sidebar { width: 200px; }
            .main { margin-left: 200px; padding: 15px; }
            .stats-grid { grid-template-columns: 1fr 1fr; }
            .main-grid { grid-template-columns: 1fr; }
            .section-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h1>⚡ BPW</h1>
        <div class="nav-item active" onclick="showPage('overview')">📊 Overview</div>
        <div class="nav-item" onclick="showPage('general')">ℹ️ General</div>
        <div class="nav-item" onclick="showPage('suspicious')">⚠️ Suspicious</div>
        <div class="nav-item" onclick="showPage('files')">📄 Files</div>
        <div class="nav-item" onclick="showPage('accounts')">👤 Accounts</div>
        <div class="logout-btn"><a href="/logout">🚪 Logout</a></div>
    </div>
    
    <div class="main">
        <div class="top-bar">
            <h2>🎯 Dashboard</h2>
            <div>
                <span style="color:#f59e0b;">⚠️ <span id="top-warnings">0</span></span>
                <span style="color:#ef4444;margin-left:15px;">🎯 <span id="top-detections">0</span></span>
            </div>
        </div>
        
        <div id="page-overview" class="page active">
            <div class="stats-grid">
                <div class="stat-card detections"><div class="label">🎯 Detections</div><div class="value" id="stat-detections">0</div></div>
                <div class="stat-card warnings"><div class="label">⚠️ Warnings</div><div class="value" id="stat-warnings">0</div></div>
                <div class="stat-card information"><div class="label">ℹ️ Information</div><div class="value" id="stat-information">0</div></div>
                <div class="stat-card total"><div class="label">📊 Total</div><div class="value" id="stat-total">0</div></div>
            </div>
            
            <div class="main-grid">
                <div class="glass-panel">
                    <div class="panel-title">🔑 Generate Code</div>
                    <button class="btn-primary" onclick="generatePin()">Generate New Code</button>
                    <div class="code-display">
                        <div style="color:#666;font-size:12px;">YOUR 6-DIGIT CODE</div>
                        <div class="code-value" id="pin-display">------</div>
                    </div>
                </div>
                <div class="glass-panel">
                    <div class="panel-title">📥 Retrieve Logs</div>
                    <div class="input-group">
                        <input type="text" id="fetch-pin" placeholder="Code" maxlength="6">
                        <button class="btn-primary" style="width:auto;padding:12px 25px;" onclick="fetchLogs()">Fetch</button>
                    </div>
                    <div id="log-output" class="log-output"><div class="empty">Logs will appear here...</div></div>
                </div>
            </div>
            
            <div class="glass-panel">
                <div class="panel-title">📈 Threat Analysis</div>
                <div class="chart-container"><canvas id="pieChart"></canvas></div>
            </div>
        </div>
        
        <div id="page-general" class="page">
            <div class="glass-panel">
                <div class="panel-title">ℹ️ General Info</div>
                <div id="general-content"><div class="empty">Fetch logs to see data</div></div>
            </div>
        </div>
        
        <div id="page-suspicious" class="page">
            <div class="glass-panel">
                <div class="panel-title">⚠️ Suspicious Findings</div>
                <div id="suspicious-content"><div class="empty">No suspicious findings</div></div>
            </div>
        </div>
        
        <div id="page-files" class="page">
            <div class="glass-panel">
                <div class="panel-title">📄 Suspicious Files</div>
                <div id="files-content"><div class="empty">No suspicious files</div></div>
            </div>
        </div>
        
        <div id="page-accounts" class="page">
            <div class="glass-panel">
                <div class="panel-title">👤 Alt Accounts</div>
                <div id="accounts-content"><div class="empty">No alt accounts</div></div>
            </div>
        </div>
    </div>
    
    <script>
        let currentLogs = null;
        let allFindings = [];
        let pieChart = null;
        
        function showPage(id) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('page-' + id).classList.add('active');
            document.querySelectorAll('.nav-item').forEach(n => {
                if (n.textContent.toLowerCase().includes(id)) n.classList.add('active');
            });
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
            output.innerHTML = '<div style="color:#7877c6;text-align:center;padding:20px;">⏳ Fetching...</div>';
            try {
                const res = await fetch('/api/get-logs/' + pin);
                const data = await res.json();
                if (data.status === 'success') {
                    currentLogs = data.logs;
                    allFindings = data.logs.findings || [];
                    updateOverview(data.logs);
                    populateAllSections(data.logs);
                    output.innerHTML = '<div style="color:#34d399;text-align:center;padding:20px;">✅ Logs loaded!</div>';
                } else {
                    output.innerText = "❌ " + data.message;
                }
            } catch(e) { output.innerText = "❌ Connection error"; }
        }
        
        function updateOverview(logs) {
            let d=0,w=0,i=0;
            if(logs.findings) {
                logs.findings.forEach(f => {
                    const t = (f.tier || 'Information').toLowerCase();
                    if(t === 'detection') d++;
                    else if(t === 'warning') w++;
                    else i++;
                });
            }
            document.getElementById('stat-detections').innerText = d;
            document.getElementById('stat-warnings').innerText = w;
            document.getElementById('stat-information').innerText = i;
            document.getElementById('stat-total').innerText = logs.total_findings || 0;
            document.getElementById('top-warnings').innerText = w;
            document.getElementById('top-detections').innerText = d;
            drawPieChart(d,w,i);
        }
        
        function createCard(item) {
            const tier = (item.tier || 'Information').toLowerCase();
            const cls = tier === 'detection' ? 'detection' : tier === 'warning' ? 'warning' : 'info';
            const badge = tier === 'detection' ? 'badge-detection' : tier === 'warning' ? 'badge-warning' : 'badge-info';
            const label = tier.toUpperCase();
            return `<div class="finding-card ${cls}">
                <div class="finding-header">
                    <div class="finding-title">${item.flag || item.category || 'Finding'}</div>
                    <span class="badge ${badge}">${label}</span>
                </div>
                <div class="finding-detail">${item.details || ''}</div>
                <div class="finding-meta">${item.category || ''} • ${item.timestamp || ''}</div>
            </div>`;
        }
        
        function populateAllSections(logs) {
            const general = document.getElementById('general-content');
            if(general) {
                let html = `<div style="background:rgba(120,119,198,0.1);padding:15px;border-radius:10px;margin-bottom:15px;">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                        <div><span style="color:#666;">Scan Time:</span> ${logs.timestamp || 'N/A'}</div>
                        <div><span style="color:#666;">Hostname:</span> ${logs.hostname || 'Unknown'}</div>
                        <div><span style="color:#666;">Username:</span> ${logs.username || 'Unknown'}</div>
                        <div><span style="color:#666;">Total Findings:</span> ${logs.total_findings || 0}</div>
                    </div>
                </div>`;
                logs.findings.forEach(f => { html += createCard(f); });
                general.innerHTML = html;
            }
            
            const suspicious = document.getElementById('suspicious-content');
            if(suspicious) {
                const s = logs.findings.filter(f => f.tier && (f.tier.toLowerCase() === 'detection' || f.tier.toLowerCase() === 'warning'));
                if(s.length > 0) {
                    let html = `<div style="color:#888;margin-bottom:10px;">Found ${s.length} suspicious findings</div>`;
                    s.forEach(f => { html += createCard(f); });
                    suspicious.innerHTML = html;
                } else { suspicious.innerHTML = '<div class="empty">No suspicious findings</div>'; }
            }
            
            const files = document.getElementById('files-content');
            if(files) {
                const f = logs.findings.filter(item => item.category && (item.category.includes('File') || item.category.includes('Disk')));
                if(f.length > 0) {
                    let html = `<div style="color:#888;margin-bottom:10px;">Found ${f.length} file-related findings</div>`;
                    f.forEach(item => { html += createCard(item); });
                    files.innerHTML = html;
                } else { files.innerHTML = '<div class="empty">No suspicious files</div>'; }
            }
            
            const accounts = document.getElementById('accounts-content');
            if(accounts) {
                const a = logs.findings.filter(f => f.category && f.category.includes('Account'));
                if(a.length > 0) {
                    let html = '';
                    a.forEach(f => { html += createCard(f); });
                    accounts.innerHTML = html;
                } else { accounts.innerHTML = '<div class="empty">No alt accounts</div>'; }
            }
        }
        
        function drawPieChart(d,w,i) {
            const ctx = document.getElementById('pieChart').getContext('2d');
            if(pieChart) pieChart.destroy();
            if(d+w+i === 0) {
                document.querySelector('.chart-container').innerHTML = '<div style="color:#666;text-align:center;padding:30px;">No data</div>';
                return;
            }
            pieChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Detections', 'Warnings', 'Information'],
                    datasets: [{
                        data: [d,w,i],
                        backgroundColor: ['rgba(239,68,68,0.8)', 'rgba(245,158,11,0.8)', 'rgba(79,172,254,0.8)'],
                        borderColor: ['#ef4444', '#f59e0b', '#4facfe'],
                        borderWidth: 2
                    }]
                },
                options: { responsive: true, maintainAspectRatio: true }
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
        return render_template_string('''
            <!DOCTYPE html>
            <html><head><title>Login</title>
            <style>body{background:#0a0a1a;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;}
            .box{background:rgba(255,255,255,0.03);padding:50px;border-radius:20px;border:1px solid rgba(255,255,255,0.05);text-align:center;}
            h1{background:linear-gradient(135deg,#7877c6,#ff77c6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
            input{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:15px;border-radius:10px;width:300px;margin-bottom:20px;font-size:16px;}
            button{background:linear-gradient(135deg,#7877c6,#ff77c6);color:#fff;border:none;padding:15px 40px;font-weight:bold;border-radius:10px;cursor:pointer;font-size:16px;}
            .error{color:#ef4444;margin-bottom:15px;}
            </style></head>
            <body><div class="box"><h1>⚡ BPW FORENSIC</h1>
            {% if error %}<div class="error">{{error}}</div>{% endif %}
            <form method="POST"><input type="password" name="password" placeholder="Password" required><br><button>Login</button></form>
            </div></body></html>
        ''', error="Wrong password!")
    return render_template_string('''
        <!DOCTYPE html>
        <html><head><title>Login</title>
        <style>body{background:#0a0a1a;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;}
        .box{background:rgba(255,255,255,0.03);padding:50px;border-radius:20px;border:1px solid rgba(255,255,255,0.05);text-align:center;}
        h1{background:linear-gradient(135deg,#7877c6,#ff77c6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
        input{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:15px;border-radius:10px;width:300px;margin-bottom:20px;font-size:16px;}
        button{background:linear-gradient(135deg,#7877c6,#ff77c6);color:#fff;border:none;padding:15px 40px;font-weight:bold;border-radius:10px;cursor:pointer;font-size:16px;}
        </style></head>
        <body><div class="box"><h1>⚡ BPW FORENSIC</h1>
        <form method="POST"><input type="password" name="password" placeholder="Password" required><br><button>Login</button></form>
        </div></body></html>
    ''')

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
    app.run(host='0.0.0.0', port=port, debug=False)
