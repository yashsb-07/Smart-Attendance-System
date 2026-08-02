import cv2
import face_recognition
import numpy as np
from database import get_db_connection
import os
import time

def mark_attendance():
    try:
        # Open webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "❌ Error: Could not open webcam."

        print("📸 Opening webcam for attendance...")

        start_time = time.time()
        student_found = False
        student_name = None

        while not student_found:
            ret, frame = cap.read()
            if not ret:
                return "❌ Error: Failed to capture frame."

            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if face_encodings:
                print("✅ Face detected, recognizing...")
                conn = get_db_connection()
                cursor = conn.cursor()

                # Fetch student data
                cursor.execute("SELECT roll_number, name, face_encoding FROM students")
                students = cursor.fetchall()

                for student in students:
                    roll_number, name, face_encoding_str = student
                    stored_encoding = np.array([float(val) for val in face_encoding_str.split(",")])

                    # Compare face
                    match = face_recognition.compare_faces([stored_encoding], face_encodings[0])[0]

                    if match:
                        student_found = True
                        student_name = name
                        print(f"✅ Match Found: {name} (Roll No: {roll_number})")

                        # Mark Attendance
                        current_date = time.strftime('%Y-%m-%d')
                        cursor.execute("SELECT * FROM attendance WHERE roll_number = %s AND date = %s", (roll_number, current_date))
                        if cursor.fetchone():
                            conn.close()
                            return f"✅ Attendance Already Marked for {name}."
                        
                        cursor.execute("INSERT INTO attendance (roll_number, name, date, status) VALUES (%s, %s, %s, %s)",
                                       (roll_number, name, current_date, 'Present'))
                        conn.commit()
                        conn.close()
                        return f"✅ Attendance Marked Successfully for {name}."

                conn.close()
                return "❌ Error: Face not recognized. Please register first."

            if time.time() - start_time > 10:
                return "⚠️ No face detected. Try again with better lighting."

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    print(mark_attendance())
