import cv2
import face_recognition
import numpy as np
from database import get_db_connection
import os
import base64

def is_face_partially_covered(face_landmarks):
    """Check if the nose and mouth are visible."""
    required_features = ["nose_bridge", "nose_tip", "top_lip", "bottom_lip"]
    for feature in required_features:
        if feature not in face_landmarks:
            return True  # Face is covered (mask/hanky detected)
    return False  # Face is clear

def register_student(name, roll_number, department, student_class, semester, image_data):
    if not all([name, roll_number, department, student_class, semester, image_data]):
        return "❌ Error: Name, Roll Number, Department, Class, Semester, and Image are required."

    try:
        # Decode the base64 image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Ensure the 'face_data' directory exists
        os.makedirs("face_data", exist_ok=True)
        image_path = f"face_data/{roll_number}_{department}_{student_class}_{semester}.jpg"

        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_landmarks_list = face_recognition.face_landmarks(rgb_frame)

        # Check if face is detected
        if face_locations:
            print("✅ Face detected, verifying visibility...")

            # Check for mask or covered face
            if not face_landmarks_list or is_face_partially_covered(face_landmarks_list[0]):
                return "❌ Error: Face is partially covered! Please remove mask/hanky."
        else:
            return "⚠️ No face detected. Please try again with better lighting."

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Step 1: Check if student with the roll number exists
        cursor.execute("""
            SELECT * FROM students
            WHERE roll_number = %s AND department = %s AND student_class = %s AND semester = %s
        """, (roll_number, department, student_class, semester))

        if cursor.fetchone():
            return "⚠️ Error: A student with this roll number already exists in this department, class, and semester."

        # Perform face encoding
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            encoding_str = ",".join(map(str, face_encoding))

            # ✅ Step 2: Check if face is already registered
            cursor.execute("""
                SELECT face_encoding FROM students 
                WHERE department = %s AND student_class = %s
            """, (department, student_class))

            registered_faces = cursor.fetchall()
            for row in registered_faces:
                stored_encoding = np.array([float(val) for val in row[0].split(",")])
                match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]
                if match:
                    return "❌ Error: This face is already registered in this department and class."

            # ✅ Step 3: Register student if all checks pass
            cv2.imwrite(image_path, frame)
            print(f"✅ Face verified and saved as {image_path}")

            cursor.execute("""
                INSERT INTO students (name, roll_number, department, student_class, semester, face_encoding, image_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, roll_number, department, student_class, semester, encoding_str, image_path))
            
            conn.commit()
            conn.close()
            return "✅ Student registered successfully!"
        else:
            return "⚠️ No face detected! Try again with better lighting."

    except Exception as e:
        return f"❌ Error processing face image: {e}"
