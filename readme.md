# 🎓 University Complaint Management System

A web-based system that allows students to submit complaints and feedback, and enables the admin to manage and resolve those complaints. Built using **Flask (Python)** and **SQLite**, this project is ideal for **DBMS course work, portfolio projects**, or **university automation tasks**.


---

## 📌 Features

- 🔐 **Login System** for Admin and Students
- 📝 **Complaint Submission** with title, description & category
- 📂 **Student Dashboard** with complaint history & feedback form
- 🛠️ **Admin Dashboard** to accept/reject complaints & view feedback
- 📅 Auto timestamping for all complaints and feedback
- 📊 Role-based views (Admin/Student)
- 💬 Feedback system with 1-5 rating

---

## 🧠 Tech Stack

| Technology | Description               |
|------------|---------------------------|
| Flask      | Python web framework      |
| SQLite     | Lightweight DBMS          |
| HTML/CSS   | Frontend (Bootstrap 4.6)  |
| Jinja2     | Templating engine         |

---

## 📂 Folder Structure
saad_prj/
├── static/
│ └── images/uit_logo.png
├── templates/
│ ├── index.html
│ ├── admin_dashboard.html
│ └── student_dashboard.html
├── app.py
├── database.sql
├── complaint_management.db


---

## ⚙️ How to Run Locally

1. **Clone the repository**  
```bash
git clone https://github.com/saadparekh/university_complain_management_system.git
cd university_complain_management_system

2. Create virtual environment (optional but recommended):
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows

3.Install dependencies:
pip install flask

4.RUN the app:
python app.py

App runs on: http://127.0.0.1:5000/

🧪 Default Login Credentials
👨‍🎓 Students:
Email	Password
saad@gmail.com	saad123
maheen@gmail.com	maheen123
hisham@gmail.com	hisham123

🛡️ Admin:
Email: admin@gmail.com

Password: admin123

TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT UNIQUE,
  password TEXT,
  role TEXT CHECK(role IN ('student','admin'))
)

TABLE complaints (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  title TEXT,
  description TEXT,
  category TEXT,
  date TEXT,
  status TEXT DEFAULT 'Pending',
  remark TEXT
)

TABLE feedback (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  rating INTEGER CHECK(rating BETWEEN 1 AND 5),
  message TEXT,
  date TEXT
)

🚀 Future Enhancements
✅ Password hashing (for security)

📈 Complaint statistics chart (e.g., resolved vs pending)

📬 Email notifications on status change

🌐 Deployment on Render or Vercel

📜 License
This project is open-source and available under the MIT License.

🙋‍♂️ Author
Saad Parekh
📧 saadparekh3@gmail.com
🔗 https://www.linkedin.com/in/saad-parekh-847a06292/

