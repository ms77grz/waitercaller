import config
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user
from mockdbhelper import MockDBHelper as DBHelper
from user import User

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager = LoginManager(app)

DB = DBHelper()


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = DB.get_user(email)
    if user_password and user_password == password:
        user = User(email)
        login_user(user)
        return redirect(url_for('account'))
    return home()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/account")
@login_required
def account():
    return "You are logged in"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
