from flask import Blueprint, render_template, request, redirect, session
from database.db import get_db_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM admins WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))

    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin:
        session["admin_id"] = admin["id"]
        return redirect("/dashboard")

    return "Invalid username or password"

@auth_bp.route("/dashboard")
def dashboard():

    if "admin_id" not in session:
        return redirect("/")

    return render_template("dashboard.html")

@auth_bp.route("/logout")
def logout():

    session.pop("admin_id", None)

    return redirect("/")