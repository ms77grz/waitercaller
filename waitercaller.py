import config
import datetime
from bitlyhelper import BitlyHelper
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from user import User

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager = LoginManager(app)

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_password = DB.get_user(email)
    if stored_password and PH.validate_password(password, stored_password['salt'], stored_password['hashed']):
        user = User(email)
        login_user(user,remember=True)
        return redirect(url_for("account"))
    return redirect(url_for("home"))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for("home"))
    if DB.get_user(email):
        return redirect(url_for("home"))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for request in requests:
        deltaseconds = (now - request["time"]).seconds
        request["wait_minutes"] = "{}.{}".format(
            (deltaseconds / 60),
            str(deltaseconds % 60).zfill(2)
        )
    return render_template("dashboard.html", requests=requests)


@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for("dashboard"))


@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)


@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    tablename = request.form.get("tablenumber")
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = BH.shorten_url(config.BASE_URL + "newrequest/" + tableid)
    DB.update_table(tableid, new_url)
    return redirect(url_for("account"))


@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for("account"))


@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request has been logged and a waiter will be with you shortly"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
