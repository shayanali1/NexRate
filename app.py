from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User

app = Flask(__name__)
app.secret_key = "nexrate_secret_key"

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)