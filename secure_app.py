# Remediated version for the CodeAlpha Secure Coding Review.
# CodeAlpha Internship — Task 3

import os
import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash

app = Flask(__name__)

DB_PATH = os.environ.get("APP_DB_PATH", "users.db")

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # REMEDIATION: Parameterized query prevents SQL injection.
    cur.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    )

    row = cur.fetchone()
    conn.close()
    return row

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    row = get_user(username)

    # REMEDIATION: Passwords should be stored as strong salted hashes.
    # In production, add rate limiting/lockout and generic error responses.
    if row and check_password_hash(row[2], password):
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid username or password"}), 401

@app.route("/user")
def user():
    username = request.args.get("username", "")
    row = get_user(username)

    if not row:
        return jsonify({"error": "User not found"}), 404

    # REMEDIATION: Return only data required by the client.
    return jsonify({"id": row[0], "username": row[1]})

if __name__ == "__main__":
    app.run(debug=False)
