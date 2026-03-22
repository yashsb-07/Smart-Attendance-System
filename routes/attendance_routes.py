from flask import Blueprint, render_template, request, send_file
from database.db import get_db_connection
from utils.face_utils import get_face_encoding
import numpy as np
from datetime import datetime
import pandas as pd

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():

    if request.method == "GET":
        return render_template("mark_attendance.html")

    data = request.get_json()
    image_data = data["image"]
    subject = data["subject"]
    session_number = data["session"]

    encoding = get_face_encoding(image_data)

    if encoding is None:
        return "No face detected"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for student in students:

        if student["face_encoding"] is None:
            continue  # skip invalid records

        stored_encoding = np.frombuffer(student["face_encoding"], dtype=np.float64)

        match = np.linalg.norm(stored_encoding - encoding)

        if match < 0.6:

            # Mark attendance
            now = datetime.now()

            # Check if already marked
            cursor.execute("""
                SELECT * FROM attendance
                WHERE student_id = %s AND date = %s AND session = %s
            """, (student["id"], now.date(), session_number))

            existing = cursor.fetchone()

            if existing:
                cursor.close()
                conn.close()
                return f"Attendance already marked for {student['name']} (Session {session_number})"

            cursor.execute("""
                INSERT INTO attendance (student_id, date, time, subject, status, session)
                VALUES (%s, %s, %s, %s, %s, %s)""", (
                    student["id"],
                    now.date(),
                    now.time(),
                    subject,
                    "Present",
                    session_number
            ))

            conn.commit()

            cursor.close()
            conn.close()

            return f"Attendance Marked for {student['name']}"

    cursor.close()
    conn.close()

    return "Face not recognized"

@attendance_bp.route("/export_excel")
def export_excel():

    conn = get_db_connection()

    query = """
        SELECT students.name, students.roll_number, attendance.date, attendance.time,
               attendance.subject, attendance.session, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
    """

    df = pd.read_sql(query, conn)

    file_path = "attendance.xlsx"
    df.to_excel(file_path, index=False)

    conn.close()

    return send_file(file_path, as_attachment=True)

@attendance_bp.route("/attendance_report")
def attendance_report():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            students.name,
            students.roll_number,
            COUNT(attendance.id) as total_present,
            (
                SELECT COUNT(DISTINCT date, session) 
                FROM attendance
            ) as total_sessions
        FROM students
        LEFT JOIN attendance ON students.id = attendance.student_id
        GROUP BY students.id
    """

    cursor.execute(query)
    data = cursor.fetchall()

    # Calculate percentage
    for row in data:
        if row["total_sessions"] == 0:
            row["percentage"] = 0
        else:
            row["percentage"] = int((row["total_present"] / row["total_sessions"]) * 100)

    cursor.close()
    conn.close()

    return render_template("attendance_report.html", report=data)

@attendance_bp.route("/search_student", methods=["GET", "POST"])
def search_student():

    if request.method == "GET":
        return render_template("search_student.html")

    roll_number = request.form["roll_number"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get student
    cursor.execute("SELECT * FROM students WHERE roll_number = %s", (roll_number,))
    student = cursor.fetchone()

    if not student:
        cursor.close()
        conn.close()
        return "Student not found"

    # Get attendance
    cursor.execute("""
        SELECT date, time, subject, session, status
        FROM attendance
        WHERE student_id = %s
    """, (student["id"],))

    attendance = cursor.fetchall()

    # Total present
    total_present = len(attendance)

    # Total sessions
    cursor.execute("SELECT COUNT(DISTINCT date, session) as total FROM attendance")
    total_sessions = cursor.fetchone()["total"]

    if total_sessions == 0:
        percentage = 0
    else:
        percentage = int((total_present / total_sessions) * 100)

    cursor.close()
    conn.close()

    return render_template("search_student.html",
                           student=student,
                           attendance=attendance,
                           percentage=percentage)