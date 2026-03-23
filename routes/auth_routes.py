from flask import Blueprint, render_template, request, redirect, session
from database.db import get_db_connection
from werkzeug.security import check_password_hash

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

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@auth_bp.route("/dashboard")
def dashboard():

    if "admin_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total students
    cursor.execute("SELECT COUNT(*) as total FROM students")
    total_students = cursor.fetchone()["total"] or 0

    # Attendance today
    cursor.execute("SELECT COUNT(*) as total FROM attendance WHERE date = CURDATE()")
    attendance_today = cursor.fetchone()["total"] or 0

    # Present today
    cursor.execute("SELECT COUNT(DISTINCT student_id) as total FROM attendance WHERE date = CURDATE()")
    present_today = cursor.fetchone()["total"] or 0

    # 👉 ADD THIS (IMPORTANT FIX)
    absent_today = total_students - present_today

    # Attendance percentage
    if total_students > 0:
        attendance_percentage = int((present_today / total_students) * 100)
    else:
        attendance_percentage = 0

    # Recent attendance
    cursor.execute("""
        SELECT students.name, attendance.date, attendance.time, attendance.subject, attendance.session
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        ORDER BY attendance.id DESC
        LIMIT 10
    """)
    recent_attendance = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dashboard.html",
                       total_students=total_students,
                       attendance_today=attendance_today,
                       present_today=present_today,
                       attendance_percentage=attendance_percentage,
                       recent_attendance=recent_attendance,
                       admin_name="Admin")