CREATE DATABASE attendance_system;

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

ALTER TABLE attendance
ADD COLUMN session INT;

SHOW TABLES;