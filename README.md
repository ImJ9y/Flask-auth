# Flask Auth App 🔐

A lightweight Flask-based authentication system with registration, login, logout, and protected routes. Ideal as a starting point for building secure web applications with user login features.

## 🚀 Features

- User registration with email, name, and hashed passwords
- Secure login/logout with session management
- Passwords stored using `pbkdf2:sha256` hashing
- Protected routes accessible only to authenticated users
- File download feature restricted to logged-in users
- Built with `Flask`, `Flask-Login`, and `SQLAlchemy`

## 🛠️ Technologies

- Python 3.10+
- Flask
- Flask-Login
- SQLAlchemy
- SQLite (default database)

## 📁 Project Structure


## ⚙️ Setup Instructions

### 1. Clone the Repository
bash
git clone https://github.com/yourusername/flask-auth-app.git
cd flask-auth-app

### 2. Create a Virtual Environment
bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

### 3. Install Dependencies
bash
pip install -r requirements.txt
If you don’t have a requirements.txt, here’s a sample:

txt
Flask
Flask-Login
Flask-SQLAlchemy

### 4. Run the Application
bash
python app.py
Access it at: http://localhost:5000

### 🔐 Authentication Flow
1. Navigate to /register to create a new account.
2. Go to /login to log in.
3. Authenticated users can access /secrets and download from /download.
4. Use /logout to end the session.

### 📦 Database Schema
A simple User model is used:
python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

The database is automatically created on first run via db.create_all().

### 💡 Future Improvements
- Add email verification
- Use Flask-Migrate for database migrations
- Improve styling with Bootstrap or Tailwind
- Add unit tests and CI/CD integration

📄 License
MIT License
