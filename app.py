import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong, random secret key for production

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('complaint_management.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the database and tables if they do not exist (safe for production)
def init_db():
    if not os.path.exists('complaint_management.db'):
        conn = get_db_connection()
        with open('database.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print("Database initialized.")
    else:
        print("Database already exists. Skipping initialization.")

# Home route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('index.html')

# Student dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    conn = get_db_connection()
    complaints = conn.execute('SELECT * FROM complaints WHERE student_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('student_dashboard.html', complaints=complaints, name=session.get('name'))

# Submit complaint
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    description = request.form['description']
    category = request.form['category']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Validate input
    if not title or not description or not category:
        flash('All fields are required.')
        return redirect(url_for('student_dashboard'))

    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO complaints (student_id, title, description, category, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], title, description, category, date))
        conn.commit()
        conn.close()
        flash('Complaint submitted successfully!')
    except sqlite3.Error as e:
        print("DB Error (submit_complaint):", e)
        flash(f'Error submitting complaint: {str(e)}')

    return redirect(url_for('student_dashboard'))

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    complaints = conn.execute('SELECT * FROM complaints ORDER BY date DESC').fetchall()
    feedbacks = conn.execute('SELECT * FROM feedback ORDER BY date DESC').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', complaints=complaints, feedbacks=feedbacks, name=session.get('name'))

# Accept or reject complaint
@app.route('/update_complaint/<int:complaint_id>', methods=['POST'])
def update_complaint(complaint_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    status = request.form['status']
    remark = request.form.get('remark', '')

    if not status:
        flash('Please choose Accept or Reject.')
        return redirect(url_for('admin_dashboard'))

    try:
        conn = get_db_connection()
        conn.execute('UPDATE complaints SET status = ?, remark = ? WHERE id = ?', (status, remark, complaint_id))
        conn.commit()
        conn.close()
        flash('Complaint status updated successfully!')
    except sqlite3.Error as e:
        print("DB Error (update_complaint):", e)
        flash(f'Error updating complaint: {str(e)}')

    return redirect(url_for('admin_dashboard'))

# Submit feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    rating = request.form['rating']
    message = request.form['message']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not rating:
        flash('Please select a rating.')
        return redirect(url_for('student_dashboard'))

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO feedback (student_id, rating, message, date) VALUES (?, ?, ?, ?)',
                     (session['user_id'], rating, message, date))
        conn.commit()
        conn.close()
        flash('Feedback submitted successfully!')
    except sqlite3.Error as e:
        print("DB Error (submit_feedback):", e)
        flash(f'Error submitting feedback: {str(e)}')

    return redirect(url_for('student_dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  # Only creates DB if it doesn't exist (safe for production)
    app.run(debug=True)  # Set debug=False for production