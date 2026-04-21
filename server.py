from flask import Flask, jsonify, request
import hashlib
from datetime import date
import os

app = Flask(__name__)
users = {
    "admin": {
        "password": hashlib.sha256("az1x@d0s".encode()).hexdigest(),
        "max_attacks": 11333,
        "attacks_today": 0,
        "last_date": str(date.today())
    },
    "free": {
        "password": hashlib.sha256("8974".encode()).hexdigest(),
        "max_attacks": 25,
        "attacks_today": 0,
        "last_date": str(date.today())
    }
}

@app.route('/')
def home():
    return """
    <h1>Ultimate DoS Test Server</h1>
    <p>Сервер работает нормально.</p>
    <p>Test server</p>
    <p>1234567</p>
    """

@app.route('/api/users', methods=['GET'])
def get_users():
    today = str(date.today())
    for u in users:
        if users[u].get("last_date") != today:
            users[u]["attacks_today"] = 0
            users[u]["last_date"] = today
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def update_users():
    global users
    try:
        data = request.get_json()
        if data:
            users = data
            return jsonify({"status": "ok", "message": "База обновлена"})
        return jsonify({"status": "error"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[+] Test Server started on port {port}")
    print(f"[+] Главная страница: http://0.0.0.0:{port}/")
    print(f"[+] API: http://0.0.0.0:{port}/api/users")
    app.run(host="0.0.0.0", port=port)
