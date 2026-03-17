from flask import Blueprint, render_template, request
from database.db import get_db_connection
from utils.face_utils import get_face_encoding

student_bp = Blueprint("student", __name__)

@student_bp.route("/register_student", methods=["GET", "POST"])
def register_student():

    if request.method == "GET":
        return render_template("register_student.html")

    name = request.form["name"]
    roll_number = request.form["roll_number"]
    department = request.form["department"]
    student_class = request.form["class"]
    semester = request.form["semester"]
    image_data = request.form["image_data"]

    encoding = get_face_encoding(image_data)

    if encoding is None:
        return "No face detected. Please try again."

    encoding_bytes = encoding.tobytes()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO students (name, roll_number, department, class, semester, face_encoding)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        name,
        roll_number,
        department,
        student_class,
        semester,
        encoding_bytes
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return "Student Registered Successfully with Face Encoding"