from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Watchlist
import requests
import os
from dotenv import load_dotenv
import random

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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nexrate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

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
    rates = get_exchange_rates("USD")

    featured_pairs = {}
    trend_data = {}

    if rates:
        featured_pairs = {
            "PKR": rates.get("PKR"),
            "EUR": rates.get("EUR"),
            "GBP": rates.get("GBP"),
            "SAR": rates.get("SAR"),
            "AED": rates.get("AED"),
            "CAD": rates.get("CAD"),
        }

        for currency in ["PKR", "EUR", "GBP", "SAR"]:
            base_rate = rates.get(currency, 1)
            trend_data[currency] = [
                round(base_rate * (1 + random.uniform(-0.02, 0.02)), 4)
                for _ in range(7)
            ]
            trend_data[currency][-1] = round(base_rate, 4)

    return render_template("dashboard.html",
                         featured_pairs=featured_pairs,
                         rates=rates,
                         trend_data=trend_data,
                         username=current_user.username)

@app.route("/profile")
@login_required
def profile():
    watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", watchlist=watchlist)

@app.route("/watchlist/add", methods=["POST"])
@login_required
def add_watchlist():
    base_currency = request.form.get("base_currency")
    target_currency = request.form.get("target_currency")

    existing = Watchlist.query.filter_by(
        user_id=current_user.id,
        base_currency=base_currency,
        target_currency=target_currency
    ).first()

    if not existing:
        new_pair = Watchlist(
            user_id=current_user.id,
            base_currency=base_currency,
            target_currency=target_currency
        )
        db.session.add(new_pair)
        db.session.commit()

    return redirect(url_for("profile"))

@app.route("/watchlist/delete/<int:id>")
@login_required
def delete_watchlist(id):
    pair = Watchlist.query.get_or_404(id)
    if pair.user_id == current_user.id:
        db.session.delete(pair)
        db.session.commit()
    return redirect(url_for("profile"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)