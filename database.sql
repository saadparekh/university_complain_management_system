-- SQLite database schema for University Complaint Management System

-- Drop existing tables if they exist (for reinitialization)
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS feedback;

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('student','admin')) NOT NULL
);

-- Complaints table
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT CHECK(category IN ('Hostel','WiFi','Canteen','Faculty','Library','Classroom')) NOT NULL,
    date TEXT NOT NULL,
    status TEXT CHECK(status IN ('Pending','Accepted','Rejected')) NOT NULL DEFAULT 'Pending',
    remark TEXT,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- Feedback table
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5) NOT NULL,
    message TEXT,
    date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- Insert sample admin and student users with plain text passwords
INSERT INTO users (name, email, password, role) VALUES
('Admin', 'admin@gmail.com', 'admin123', 'admin'),
('Saad', 'saad@gmail.com', 'saad123', 'student'),
('maheen', 'maheen@gmail.com', 'maheen123', 'student'),
('hafsa', 'hafsa@gmail.com', 'hafsa123', 'student'),
('ali', 'ali@gmail.com', 'ali123', 'student'),
('sana', 'sana@gmail.com', 'sana123', 'student'),
('sara', 'sara@gmail.com', 'sara123', 'student'),
('jaweria', 'jaweria@gmail.com', 'jaweria123', 'student'),
('ahsan', 'ahsan@gmail.com', 'ahsan123', 'student'),
('zohaib', 'zohaib@gmail.com', 'zohaib123', 'student'),
('sadia', 'sadia@gmail.com', 'sadia123', 'student'),
('hisham', 'hisham@gmail.com', 'hisham123', 'student');
