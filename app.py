from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify, Response
import face_registration
import attendance_recognition
from database import get_db_connection
import bcrypt
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import numpy as np
import dlib
import cv2
import base64

app = Flask(__name__)
app.secret_key = 'yashsb-07'

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Admin Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Validate admin credentials
            cursor.execute("SELECT password FROM admins WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    session['admin_logged_in'] = True
                    session['admin_username'] = username
                    flash('✅ Login successful!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('❌ Invalid password!', 'danger')
            else:
                flash('❌ Admin not found!', 'danger')
        except Exception as e:
            flash(f"❌ Error: {e}", 'danger')
        finally:
            conn.close()
    return render_template('login.html')

# Admin Logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'success')
    return redirect('/')

# Student Registration Page
@app.route('/register-student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        department = request.form.get('department')
        student_class = request.form.get('class')
        semester = request.form.get('semester')
        image_data = request.form.get('image_data')

        # Check for missing fields
        if not all([name, roll_number, department, student_class, semester, image_data]):
            return render_template('register_student.html', message="❌ Please provide all details including the captured image.")
        
        try:
            # Pass all fields including image_data to face_registration
            result_message = face_registration.register_student(name, roll_number, department, student_class, semester, image_data)
            return render_template('register_student.html', message=result_message)
        except Exception as e:
            return render_template('register_student.html', message=f"❌ Error: {e}")

    return render_template('register_student.html')

# Video streaming generator function
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Mark Attendance Page
@app.route('/mark-attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        try:
            result_message = attendance_recognition.mark_attendance()
            return render_template('mark_attendance.html', message=result_message)
        except Exception as e:
            return render_template('mark_attendance.html', message=f"❌ Error: {e}")

    return render_template('mark_attendance.html')

# Admin Dashboard Page and Percentage Calculation 
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        flash('❌ Please log in first!', 'warning')
        return redirect('/login')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Total Students
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        # Total Present Today
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'Present' AND date = CURDATE()")
        total_present = cursor.fetchone()[0]

        # Total Absent Today
        total_absent = total_students - total_present

        # Recent Attendance Records (Last 10)
        cursor.execute("""
            SELECT a.roll_number, s.name, a.status, a.date
            FROM attendance a
            JOIN students s ON a.roll_number = s.roll_number
            ORDER BY a.date DESC
            LIMIT 10
        """)
        recent_attendance = cursor.fetchall()

         # Attendance Percentage Calculation

        cursor.execute("""

            SELECT s.roll_number, s.name,

            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS total_present,

            COUNT(a.date) AS total_days,

            ROUND((SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(a.date)) * 100, 2) AS percentage

            FROM students s

            LEFT JOIN attendance a ON s.roll_number = a.roll_number

            GROUP BY s.roll_number, s.name

        """)

        attendance_percentage = cursor.fetchall()

        conn.close()

        return render_template(
            'admin_dashboard.html',
            total_students=total_students,
            total_present=total_present,
            total_absent=total_absent,
            recent_attendance=recent_attendance,
            attendance_percentage=attendance_percentage
        )
    
    except Exception as e:
        return render_template('admin_dashboard.html', error=f"❌ Error: {e}")

#view all attendance
@app.route('/view-all-attendance')
def view_all_attendance():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch Present Students
        cursor.execute("""
            SELECT s.roll_number, s.name, a.status, DATE(a.Timestamp) AS date, TIME(a.Timestamp) AS time
            FROM students s
            JOIN attendance a ON s.roll_number = a.roll_number
            WHERE a.status = 'Present'
            ORDER BY a.Timestamp DESC
        """)
        present_students = cursor.fetchall()

        # Fetch Absent Students (No attendance record or marked Absent)
        cursor.execute("""
            SELECT s.roll_number, s.name, 'Absent' AS status, '-' AS date, '-' AS time
            FROM students s
            LEFT JOIN attendance a ON s.roll_number = a.roll_number
            WHERE a.roll_number IS NULL OR a.status = 'Absent'
            ORDER BY s.roll_number
        """)
        absent_students = cursor.fetchall()

        conn.close()

        return render_template('view_all_attendance.html', present_students=present_students, absent_students=absent_students)

    except Exception as e:
        return render_template('view_all_attendance.html', error=f"❌ Error: {e}")

#attendance overview
@app.route('/attendance-overview', methods=['GET', 'POST'])
def attendance_overview():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch unique departments, subjects, and semesters for filters
        cursor.execute("SELECT DISTINCT department FROM students")
        departments = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT subject FROM students")
        subjects = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT semester FROM students")
        semesters = [row[0] for row in cursor.fetchall()]

        # Handle Filtering
        department_filter = request.form.get('department')
        subject_filter = request.form.get('subject')
        semester_filter = request.form.get('semester')

        query = """
        SELECT s.roll_number, s.name, s.department, s.semester, s.subject, a.status, a.date
        FROM attendance a
        JOIN students s ON a.roll_number = s.roll_number
        WHERE 1=1
        """
        params = []

        if department_filter:
            query += " AND s.department = %s"
            params.append(department_filter)
        if subject_filter:
            query += " AND s.subject = %s"
            params.append(subject_filter)
        if semester_filter:
            query += " AND s.semester = %s"
            params.append(semester_filter)

        cursor.execute(query, params)
        attendance_data = cursor.fetchall()
        
        conn.close()

        return render_template(
            'attendance_overview.html',
            departments=departments,
            subjects=subjects,
            semesters=semesters,
            attendance_data=attendance_data,
            department_filter=department_filter,
            subject_filter=subject_filter,
            semester_filter=semester_filter
        )
    
    except Exception as e:
        return render_template('attendance_overview.html', error=f"❌ Error: {e}")
    
# search attendance
@app.route('/search-attendance', methods=['GET', 'POST'])
def search_attendance():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        attendance_data = []

        if request.method == 'POST':
            search_type = request.form.get('search_type')
            roll_number = request.form.get('roll_number')
            name = request.form.get('name')

            if search_type == 'roll_number':
                if not roll_number:
                    return render_template('search_attendance.html', error="❌ Please enter a Roll Number.")

                cursor.execute("""
                    SELECT s.roll_number, s.name, a.status, a.date
                    FROM attendance a
                    JOIN students s ON a.roll_number = s.roll_number
                    WHERE s.roll_number = %s
                    ORDER BY a.date DESC
                """, (roll_number,))
            
            elif search_type == 'name':
                if not name:
                    return render_template('search_attendance.html', error="❌ Please enter a Name.")

                cursor.execute("""
                    SELECT s.roll_number, s.name, a.status, a.date
                    FROM attendance a
                    JOIN students s ON a.roll_number = s.roll_number
                    WHERE s.name LIKE %s
                    ORDER BY a.date DESC
                """, (f"%{name}%",))

            attendance_data = cursor.fetchall()

            if not attendance_data:
                return render_template('search_attendance.html', error="❌ No attendance records found.")

        conn.close()

        return render_template('search_attendance.html', attendance_data=attendance_data)

    except Exception as e:
        return render_template('search_attendance.html', error=f"❌ Error: {e}")

# Export to Excel (Present and Absent Students)
@app.route('/export-excel')
def export_excel():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch Present Students with time in 24-hour format
        cursor.execute("""
            SELECT a.roll_number, s.name, a.status, a.date, 
                   DATE_FORMAT(a.Timestamp, '%H:%i:%s') AS Time
            FROM attendance a
            JOIN students s ON a.roll_number = s.roll_number
        """)
        present_data = cursor.fetchall()

        # Fetch Absent Students (Set Time as N/A)
        cursor.execute("""
            SELECT s.roll_number, s.name, 'Absent' AS Status, CURDATE() AS Date, 'N/A' AS Time
            FROM students s
            LEFT JOIN attendance a ON s.roll_number = a.roll_number AND a.date = CURDATE()
            WHERE a.roll_number IS NULL
        """)
        absent_data = cursor.fetchall()

        # Combine Present and Absent Data
        all_data = present_data + absent_data

        # Convert to DataFrame
        df = pd.DataFrame(all_data, columns=['Roll Number', 'Name', 'Status', 'Date', 'Time'])

        # Save to Excel
        excel_path = 'attendance_records.xlsx'
        df.to_excel(excel_path, index=False)

        return send_file(excel_path, as_attachment=True)

    except Exception as e:
        return f"❌ Error: {e}"

# Export to PDF (Present and Absent Students)
@app.route('/export-pdf')
def export_pdf():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch Present Students
        cursor.execute("""
            SELECT a.roll_number, s.name, a.status, a.date, TIME(a.Timestamp)
            FROM attendance a
            JOIN students s ON a.roll_number = s.roll_number
        """)
        present_data = cursor.fetchall()

        # Fetch Absent Students
        cursor.execute("""
            SELECT s.roll_number, s.name, 'Absent', CURDATE(), 'N/A'
            FROM students s
            LEFT JOIN attendance a ON s.roll_number = a.roll_number AND a.date = CURDATE()
            WHERE a.roll_number IS NULL
        """)
        absent_data = cursor.fetchall()

        # Combine Both Data
        all_data = present_data + absent_data

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Attendance Records (Present & Absent)", ln=True, align='C')
        pdf.ln(10)

        # Table Headers
        headers = ['Roll Number', 'Name', 'Status', 'Date', 'Time']
        pdf.set_font("Arial", size=10)
        pdf.set_fill_color(200, 220, 255)

        for header in headers:
            pdf.cell(38, 10, header, 1, 0, 'C', fill=True)
        pdf.ln()

        # Table Data
        for record in all_data:
            for item in record:
                pdf.cell(38, 10, str(item), 1)
            pdf.ln()

        pdf_path = 'attendance_records.pdf'
        pdf.output(pdf_path)

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        return f"❌ Error: {e}"   
    
# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
