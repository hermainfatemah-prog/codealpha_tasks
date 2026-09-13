# Intentionally vulnerable demo application for security review.
# CodeAlpha Internship — Task 3

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_user(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # FINDING: SQL injection risk — user input is concatenated into SQL.
    query = "SELECT id, username FROM users WHERE username = '" + username + "'"
    cur.execute(query)

    row = cur.fetchone()
    conn.close()
    return row

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # FINDING: Hard-coded/demo plaintext credential check.
    # FINDING: No rate limiting or account lockout.
    if username == "admin" and password == "admin123":
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/user")
def user():
    username = request.args.get("username", "")
    row = get_user(username)

    if not row:
        return jsonify({"error": "User not found"}), 404

    # FINDING: Detailed database-derived information is returned directly.
    return jsonify({"id": row[0], "username": row[1]})

if __name__ == "__main__":
    app.run(debug=True)
