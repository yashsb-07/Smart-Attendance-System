from flask import Flask
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp

app = Flask(__name__)

app.secret_key = "attendance_secret_key"

app.config.from_object("config.Config")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit



# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(attendance_bp)

if __name__ == "__main__":
    app.run(debug=True)