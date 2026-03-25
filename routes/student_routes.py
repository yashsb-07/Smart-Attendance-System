from flask import Blueprint, render_template, request
from database.db import get_db_connection
from utils.face_utils import get_face_encoding
import base64, os

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
    image_data = request.form.get("image_data")

    if not image_data:
        return render_template("register_student.html", error="Please capture face before registering.")

    encoding = get_face_encoding(image_data)

    if encoding is None:
        return render_template("register_student.html", error="No face detected. Please try again.")

    # -------- SAVE IMAGE --------
    image_data_split = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data_split)

    # Absolute path fix
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(BASE_DIR, "dataset", "student_faces")

    # Create folder if not exists
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    file_path = os.path.join(dataset_path, f"{roll_number}.jpg")

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    # -------- SAVE ENCODING --------
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

    return render_template("register_student.html", message="Student Registered Successfully!")