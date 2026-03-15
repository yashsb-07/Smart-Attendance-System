from flask import Blueprint, render_template

student_bp = Blueprint("student", __name__)

@student_bp.route("/register_student")
def register_student():
    return render_template("register_student.html")