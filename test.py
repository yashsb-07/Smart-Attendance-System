# import cv2

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow
# if not cap.isOpened():
#     print("❌ Error: Could not open webcam.")
#     exit()

# print("📸 Opening webcam... Press 'q' to exit.")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("❌ Error: Failed to capture frame.")
#         break

#     cv2.imshow("Camera Test", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# import bcrypt

# hashed_password = b"$2b$12$LHwwwpUCsdTMxF8BAR/C9.te2.g0CGkgEW1S7njTtwImoPdupwYxq"
# plain_password = b"yashsb07"  # Try your guess

# if bcrypt.checkpw(plain_password, hashed_password):
#     print("✅ Password matches!")
# else:
#     print("❌ Password does not match.")

"""CREATE DATABASE attendance_system;

USE attendance_system;

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO admins (username, password)
VALUES ('yash', 'yash123');

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50),
    class VARCHAR(20),
    semester VARCHAR(10),
    face_encoding LONGBLOB
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    date DATE,
    time TIME,
    subject VARCHAR(50),
    status VARCHAR(10),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

ALTER TABLE students ADD COLUMN photo_path VARCHAR(255);
ALTER TABLE students DROP COLUMN photo_path;
ADD COLUMN session INT;

SHOW TABLES;

SELECT * FROM students;
SELECT * FROM attendance;
DROP DATABASE attendance_system;
DELETE FROM students WHERE face_encoding IS NULL;
"""
