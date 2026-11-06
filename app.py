from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import uuid

app = Flask(__name__)
CORS(app)

DATABASE = "civicguard.db"


# Create database
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# Home
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "CivicGuard AI Backend Running!"
    })


# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Backend connected successfully"
    })


# Submit report
@app.route("/reports", methods=["POST"])
def create_report():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No report data received"}), 400

    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    category = str(data.get("category", "")).strip()
    location = str(data.get("location", "")).strip()

    if not all([title, description, category, location]):
        return jsonify({
            "error": "Please fill all required fields"
        }), 400

    report = (
        str(uuid.uuid4()),
        title,
        description,
        category,
        location,
        "Pending",
        datetime.now().isoformat()
    )

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO reports
        (id, title, description, category, location, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, report)

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Report submitted successfully!",
        "report": {
            "id": report[0],
            "title": report[1],
            "description": report[2],
            "category": report[3],
            "location": report[4],
            "status": report[5],
            "created_at": report[6]
        }
    }), 201


# Get all reports
@app.route("/reports", methods=["GET"])
def get_reports():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM reports ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)