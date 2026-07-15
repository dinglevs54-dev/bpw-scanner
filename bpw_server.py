import os
import random
import string
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- CHANGE THIS PASSWORD ---
ADMIN_PASSWORD = "DINGLE_012" 
# ----------------------------

sessions = {}

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BPW Command Center</title>
    <style>
        body { background: #0a0a0a; color: #fff; font-family: sans-serif; padding: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #00ff9d; border-bottom: 2px solid #00ff9d; padding-bottom: 10px; }
        .box { background: #1a1d24; padding: 25px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; }
        button { background: #00ff9d; color: #000; border: none; padding: 12px 24px; font-weight: bold; cursor: pointer; border-radius: 4px; font-size: 16px; }
        button:hover { background: #00cc7d; }
        input { background: #0a0a0a; border: 1px solid #333; color: #fff; padding: 12px; border-radius: 4px; width: 250px; font-size: 16px; }
        #pin-display { font-size: 48px; color: #00ff9d; font-weight: bold; letter-spacing: 10px; margin: 20px 0; text-align: center; background: #000; padding: 20px; border-radius: 8px; }
        #log-output { white-space: pre-wrap; background: #000; padding: 20px; border-radius: 4px; max-height: 500px; overflow-y: auto; font-family: monospace; font-size: 14px; color: #0f0; border: 1px solid #333; }
        h3 { color: #fff; margin-top: 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>BPW // COMMAND CENTER</h1>
        
        <div class="box">
            <h3>1. Generate Access Code</h3>
            <p style="color: #888;">Click below to get a 6-digit code. Give this code to the person you are scanning.</p>
            <button onclick="generatePin()">Generate New Code</button>
            <div id="pin-display">------</div>
        </div>

        <div class="box">
            <h3>2. Retrieve Logs</h3>
            <p style="color: #888;">Once they finish the scan, enter their code here to see their results.</p>
            <input type="text" id="fetch-pin" placeholder="Enter 6-digit code" maxlength="6">
            <button onclick="fetchLogs()">Fetch Logs</button>
            <div id="log-output" style="margin-top: 20px;">Logs will appear here...</div>
        </div>
    </div>

    <script>
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
            
            const res = await fetch(`/api/get-logs/${pin}`);
            const data = await res.json();
            
            if (data.status === 'success') {
                output.innerText = JSON.stringify(data.logs, null, 2);
            } else {
                output.innerText = "Error: " + data.message;
            }
        }
    </script>
</body>
</html>
"""

# Simple Password Protection
@app.route('/')
def dashboard():
    auth = request.authorization
    if not auth or auth.password != ADMIN_PASSWORD:
        return "Access Denied. Please enter your password.", 401
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/generate-pin', methods=['GET'])
def generate_pin():
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
    if pin in sessions:
        if sessions[pin]["logs"]:
            return jsonify({"status": "success", "logs": sessions[pin]["logs"]})
        else:
            return jsonify({"status": "waiting", "message": "Scan not completed yet. Tell them to run the scanner!"})
    return jsonify({"status": "error", "message": "Invalid code."}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)