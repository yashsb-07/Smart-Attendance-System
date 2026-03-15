from flask import Flask
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp

app = Flask(__name__)
app.config.from_object("config.Config")

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(attendance_bp)

if __name__ == "__main__":
    app.run(debug=True)