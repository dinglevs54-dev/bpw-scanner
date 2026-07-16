import os
import json
import random
import string
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for, send_file
import io

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- CHANGE THIS PASSWORD ---
ADMIN_PASSWORD = "DINGLE_012" 
# ----------------------------

LOGS_FILE = "logs.json"
logs_cache = {}
sessions = {}

# ============================================================================
# LOAD / SAVE LOGS
# ============================================================================

def load_logs():
    global logs_cache
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, 'r') as f:
                logs_cache = json.load(f)
        except:
            logs_cache = {}
    else:
        logs_cache = {}

def save_logs():
    with open(LOGS_FILE, 'w') as f:
        json.dump(logs_cache, f, indent=2)

def cleanup_old_logs():
    now = datetime.now()
    to_delete = []
    for pin, entry in logs_cache.items():
        if entry.get('status') == 'completed':
            timestamp = entry.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    if now - dt > timedelta(days=7):
                        to_delete.append(pin)
                except:
                    pass
    for pin in to_delete:
        del logs_cache[pin]
    if to_delete:
        save_logs()

load_logs()
cleanup_old_logs()

# ============================================================================
# ROUTES
# ============================================================================

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
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    background: #0a0e1a;
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: 'Segoe UI', sans-serif;
                    background-image: radial-gradient(ellipse at 10% 20%, rgba(6,182,212,0.08) 0%, transparent 50%);
                }
                .box {
                    background: rgba(255,255,255,0.03);
                    padding: 50px;
                    border-radius: 20px;
                    border: 1px solid rgba(255,255,255,0.06);
                    text-align: center;
                    max-width: 400px;
                    width: 90%;
                    backdrop-filter: blur(10px);
                }
                h1 {
                    background: linear-gradient(135deg, #06b6d4, #8b5cf6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 28px;
                    margin-bottom: 8px;
                }
                .sub { color: #4a5568; font-size: 14px; margin-bottom: 30px; }
                input {
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.1);
                    color: #fff;
                    padding: 16px;
                    border-radius: 12px;
                    width: 100%;
                    margin-bottom: 20px;
                    font-size: 16px;
                    transition: 0.3s;
                }
                input:focus { outline: none; border-color: #06b6d4; box-shadow: 0 0 30px rgba(6,182,212,0.1); }
                button {
                    background: linear-gradient(135deg, #06b6d4, #8b5cf6);
                    color: #fff;
                    border: none;
                    padding: 16px 40px;
                    font-weight: 700;
                    border-radius: 12px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 100%;
                    transition: 0.3s;
                }
                button:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(6,182,212,0.35); }
                .error { color: #ef4444; margin-bottom: 15px; font-size: 14px; }
                .lock { font-size: 40px; margin-bottom: 16px; }
            </style>
            </head>
            <body>
            <div class="box">
                <div class="lock">🔒</div>
                <h1>BPW Forensic</h1>
                <div class="sub">Secure Access Required</div>
                {% if error %}<div class="error">{{error}}</div>{% endif %}
                <form method="POST">
                    <input type="password" name="password" placeholder="Password" required>
                    <button>Access Dashboard</button>
                </form>
            </div>
            </body></html>
        ''', error="Wrong password!" if request.form else None)
    return render_template_string('''
        <!DOCTYPE html>
        <html><head><title>Login</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: #0a0e1a;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Segoe UI', sans-serif;
                background-image: radial-gradient(ellipse at 10% 20%, rgba(6,182,212,0.08) 0%, transparent 50%);
            }
            .box {
                background: rgba(255,255,255,0.03);
                padding: 50px;
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.06);
                text-align: center;
                max-width: 400px;
                width: 90%;
                backdrop-filter: blur(10px);
            }
            h1 {
                background: linear-gradient(135deg, #06b6d4, #8b5cf6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 28px;
                margin-bottom: 8px;
            }
            .sub { color: #4a5568; font-size: 14px; margin-bottom: 30px; }
            input {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                color: #fff;
                padding: 16px;
                border-radius: 12px;
                width: 100%;
                margin-bottom: 20px;
                font-size: 16px;
                transition: 0.3s;
            }
            input:focus { outline: none; border-color: #06b6d4; box-shadow: 0 0 30px rgba(6,182,212,0.1); }
            button {
                background: linear-gradient(135deg, #06b6d4, #8b5cf6);
                color: #fff;
                border: none;
                padding: 16px 40px;
                font-weight: 700;
                border-radius: 12px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
                transition: 0.3s;
            }
            button:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(6,182,212,0.35); }
            .lock { font-size: 40px; margin-bottom: 16px; }
        </style>
        </head>
        <body>
        <div class="box">
            <div class="lock">🔒</div>
            <h1>BPW Forensic</h1>
            <div class="sub">Secure Access Required</div>
            <form method="POST">
                <input type="password" name="password" placeholder="Password" required>
                <button>Access Dashboard</button>
            </form>
        </div>
        </body></html>
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
    if pin in logs_cache and logs_cache[pin].get('status') == 'completed':
        return jsonify({"status": "valid"}), 200
    return jsonify({"status": "invalid"}), 404

@app.route('/api/submit-logs/<pin>', methods=['POST'])
def submit_logs(pin):
    if pin in sessions or pin not in logs_cache:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "logs": request.json
        }
        logs_cache[pin] = log_entry
        if pin in sessions:
            sessions[pin]["status"] = "completed"
        save_logs()
        return jsonify({"status": "received"}), 200
    return jsonify({"status": "invalid pin"}), 404

@app.route('/api/get-logs/<pin>', methods=['GET'])
def get_logs(pin):
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    if pin in logs_cache and logs_cache[pin].get('status') == 'completed':
        return jsonify({"status": "success", "logs": logs_cache[pin]["logs"]})
    elif pin in sessions and sessions[pin]["status"] == "waiting":
        return jsonify({"status": "waiting", "message": "Scan not completed yet"})
    return jsonify({"status": "error", "message": "Invalid code"}), 404

@app.route('/api/list-logs', methods=['GET'])
def list_logs():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    summary = []
    for pin, entry in logs_cache.items():
        if entry.get('status') == 'completed':
            logs = entry.get('logs', {})
            summary.append({
                "pin": pin,
                "timestamp": entry.get('timestamp'),
                "hostname": logs.get('hostname', 'Unknown'),
                "username": logs.get('username', 'Unknown'),
                "findings": len(logs.get('findings', []))
            })
    return jsonify(summary)

# ============================================================================
# DOWNLOAD LOGS AS JSON
# ============================================================================

@app.route('/api/download-logs/<pin>', methods=['GET'])
def download_logs(pin):
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    if pin in logs_cache and logs_cache[pin].get('status') == 'completed':
        logs_data = logs_cache[pin]["logs"]
        json_str = json.dumps(logs_data, indent=2)
        return send_file(
            io.BytesIO(json_str.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'scan_logs_{pin}.json'
        )
    return jsonify({"error": "Logs not found"}), 404

# ============================================================================
# DASHBOARD HTML (with Download Button)
# ============================================================================

PROFESSIONAL_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BPW // FORENSIC SCANNER</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        /* ... (all existing styles, plus a new download button) ... */
        /* I'll keep the same styles as before, just add a new class for the download button */
        .download-btn {
            background: #8b5cf6;
            color: #fff;
            border: none;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            margin-left: 10px;
            transition: 0.3s;
        }
        .download-btn:hover {
            background: #7c3aed;
            transform: scale(1.02);
        }
        /* ... rest of styles from previous version ... */
    </style>
</head>
<body>
    <!-- SIDEBAR (same as before) -->
    <!-- MAIN CONTENT -->
    <div class="main-content">
        <div class="top-bar">
            <div class="top-bar-left">
                <h2>🎯 Dashboard</h2>
                <p>Real‑time forensic analysis & threat detection</p>
            </div>
            <div class="top-bar-right">
                <div class="live-indicator">
                    <span class="live-dot"></span>
                    <span>Live</span>
                </div>
                <span class="stat-badge warnings">
                    <span class="pulse-dot"></span>
                    <span id="top-warnings">0</span>
                </span>
                <span class="stat-badge detections">
                    <span class="pulse-dot"></span>
                    <span id="top-detections">0</span>
                </span>
                <span class="ai-badge"><i class="fas fa-brain"></i> AI-Powered</span>
            </div>
        </div>

        <!-- Overview Page -->
        <div id="page-overview" class="page active">
            <!-- stats grid etc -->
            <div class="main-grid">
                <!-- Generate PIN -->
                <div class="glass-panel">
                    <div class="panel-header">
                        <div class="panel-title"><span class="emoji">🔑</span> Generate Access Code</div>
                    </div>
                    <button class="btn-primary" onclick="generatePin()">
                        <i class="fas fa-sync-alt"></i> Generate New Code
                    </button>
                    <div class="code-display">
                        <div class="label">Your 6‑Digit Code</div>
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
                        <input type="text" id="fetch-pin" placeholder="Enter 6‑digit code" maxlength="6">
                        <button class="btn-primary" onclick="fetchLogs()">
                            <i class="fas fa-search"></i> Fetch
                        </button>
                        <button class="download-btn" onclick="downloadLogs()" id="download-btn" style="display:none;">
                            <i class="fas fa-download"></i> Download
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
                    <span class="live-indicator" style="font-size:11px;">
                        <span class="live-dot"></span> Updated
                    </span>
                </div>
                <div class="chart-container"><canvas id="pieChart"></canvas></div>
            </div>
        </div>

        <!-- Other pages (All Logs, Suspicious, etc.) -->
        <!-- ... (same as before) ... -->
    </div>

    <script>
        let currentLogs = null;
        let allFindings = [];
        let pieChart = null;
        let currentFilter = 'all';
        let currentPin = '';

        // ... (all existing JavaScript) ...

        // Modified fetchLogs to show download button
        async function fetchLogs() {
            const pin = document.getElementById('fetch-pin').value;
            if (pin.length !== 6) { alert("Please enter a 6-digit code"); return; }
            currentPin = pin;

            const output = document.getElementById('log-output');
            output.innerHTML = `<div style="text-align:center;padding:40px;color:var(--accent-cyan);">
                <div class="spinner" style="width:40px;height:40px;border-width:3px;margin:0 auto 16px;"></div>
                <p>Fetching logs...</p>
            </div>`;
            document.getElementById('download-btn').style.display = 'none';

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
                        <p>✅ Logs loaded!</p>
                        <p style="font-size:12px;color:var(--text-muted);margin-top:4px;">${allFindings.length} findings found</p>
                    </div>`;
                    document.getElementById('download-btn').style.display = 'inline-block';
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

        async function downloadLogs() {
            if (!currentPin) {
                alert("No logs loaded. Please fetch logs first.");
                return;
            }
            try {
                const res = await fetch('/api/download-logs/' + currentPin);
                if (res.status === 200) {
                    const blob = await res.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `scan_logs_${currentPin}.json`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                } else {
                    alert("Failed to download logs.");
                }
            } catch (e) {
                alert("Error downloading: " + e);
            }
        }

        // ... rest of the JavaScript functions (updateOverview, populateAllSections, drawPieChart, etc.) ...
        // They are the same as before, so I'll skip repeating them here.
        // But they must be present in the final dashboard.
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
