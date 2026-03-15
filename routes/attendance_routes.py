from flask import Blueprint, render_template

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark_attendance")
def mark_attendance():
    return render_template("mark_attendance.html")