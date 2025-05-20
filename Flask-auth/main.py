import flask
from django.utils.http import url_has_allowed_host_and_scheme
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# CREATE DATABASE
# class Base(DeclarativeBase):
    # pass
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
 
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with that email already exists. Please log in instead.")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )

        try:
            new_user = User(
                email=email,
                password=hash_and_salted_password,
                name=request.form.get('name')
            )
            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database
            login_user(new_user)
            return redirect(url_for("secrets"))

        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed. Please try again.")
            print(f"Error: {e}")

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Check if user exists
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif check_password_hash(user.password, password):
            login_user(user)  # Not User (the class)
            flash('Logged in Successfully.')
            return redirect(url_for("secrets"))
        else:
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", user=current_user, logged_in=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    return send_from_directory(directory='static', path='files/cheat_sheet.pdf')

if __name__ == "__main__":
    app.run(debug=True)
