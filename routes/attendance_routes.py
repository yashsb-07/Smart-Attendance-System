from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from flask import Blueprint, render_template, request, send_file
from face_recognition.liveness_detection import detect_liveness
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from database.db import get_db_connection
from utils.face_utils import get_face_encoding
import numpy as np
from datetime import datetime
import pandas as pd
import os
import base64
import cv2

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():

    if request.method == "GET":
        return render_template("mark_attendance.html")

    data = request.get_json()
    frames = data["frames"]        # multiple frames now
    subject = data["subject"]
    session_number = data["session"]

    # ---------------- LIVENESS CHECK ----------------
    live_detected = False
    encoding = None

    for frame_data in frames:
        image_data = frame_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Check blink (liveness)
        if detect_liveness(frame):
            live_detected = True

        # Also get encoding from one of the frames
        if encoding is None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = get_face_encoding(frame_data)
            if encodings is not None:
                encoding = encodings

    if not live_detected:
        return "Liveness check failed. Please blink."

    if encoding is None:
        return "Face not detected properly."

    # ---------------- FACE MATCHING ----------------
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for student in students:

        if student["face_encoding"] is None:
            continue

        stored_encoding = np.frombuffer(student["face_encoding"], dtype=np.float64)
        match = np.linalg.norm(stored_encoding - encoding)

        if match < 0.6:
            now = datetime.now()

            # Check duplicate
            cursor.execute("""
                SELECT * FROM attendance
                WHERE student_id = %s AND date = %s AND session = %s
            """, (student["id"], now.date(), session_number))

            existing = cursor.fetchone()

            if existing:
                cursor.close()
                conn.close()
                return f"Attendance already marked for {student['name']} (Session {session_number})"

            # Insert attendance
            cursor.execute("""
                INSERT INTO attendance (student_id, date, time, subject, status, session)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
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

@attendance_bp.route("/export_pdf")
def export_pdf():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT students.name, students.roll_number, attendance.date, attendance.time,
               attendance.subject, attendance.session, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    file_path = "attendance_report.pdf"

    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(file_path, pagesize=letter)

    elements = []

    title = Paragraph("Attendance Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    table_data = [["Name", "Roll", "Date", "Time", "Subject", "Session", "Status"]]

    for row in data:
        table_data.append([
            row["name"],
            row["roll_number"],
            str(row["date"]),
            str(row["time"]),
            row["subject"],
            row["session"],
            row["status"]
        ])

    table = Table(table_data)
    elements.append(table)

    pdf.build(elements)

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