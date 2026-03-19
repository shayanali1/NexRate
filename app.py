from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "nexrate_secret_key")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

def get_exchange_rates(base_currency="USD"):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        if data["result"] == "success":
            return data["conversion_rates"]
        return None
    except:
        return None

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nexrate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", error="Email already registered!")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid email or password!")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    print("API KEY:", EXCHANGE_API_KEY)
    rates = get_exchange_rates("USD")
    print("RATES:", rates)
    
    featured_pairs = {}
    if rates:
        featured_pairs = {
            "PKR": rates.get("PKR"),
            "EUR": rates.get("EUR"),
            "GBP": rates.get("GBP"),
            "SAR": rates.get("SAR"),
            "AED": rates.get("AED"),
            "CAD": rates.get("CAD"),
        }
    
    return render_template("dashboard.html", 
                         featured_pairs=featured_pairs,
                         rates=rates,
                         username=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)