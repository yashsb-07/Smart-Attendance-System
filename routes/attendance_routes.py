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