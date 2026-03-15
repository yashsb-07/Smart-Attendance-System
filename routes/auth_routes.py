from flask import Blueprint, render_template
from database.db import get_db_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return render_template("index.html")

# @auth_bp.route("/login")
# def login():
#     return render_template("login.html")

@auth_bp.route("/test_db")
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1")

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return f"Database Connected Successfully: {result}"