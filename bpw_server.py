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

LOGIN_HTML = """
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
"""

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
        .logout { float: right; background: #ff4757; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 14px; }
        .logout:hover { background: #ff3344; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/logout" class="logout">Logout</a>
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

@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_HTML, error="Wrong password!")
    return render_template_string(LOGIN_HTML, error=None)

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
