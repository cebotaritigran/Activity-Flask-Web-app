import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_ckeditor import CKEditor
from wtforms import StringField, SubmitField


# configuring application
app = Flask(__name__)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use sqlite database
db = SQL("sqlite:///save.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    #logging user
    session.clear()
    if request.method == "POST":
        errorName = "Please enter an user name"
        errorPassword = "Please enter a valid password"
        errorWrong = "invalid username and/or password"
        if not request.form.get("username"):
            return render_template("login.html", errorName = errorName)
        elif not request.form.get("password"):
            return render_template("login.html", errorPassword = errorPassword)
    
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", errorWrong = errorWrong)
    
        session["user_id"] = rows[0]["id"]

        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    # registering user
    name = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    userName = db.execute("SELECT username FROM users WHERE username = ?", name)

    errorName = "Please enter an user name"
    errorPassword = "Please enter a valid password"
    errorPasswordC = "Please confirm your password"
    errorExists = "User name entered already exists"
    if request.method == "POST":
        if not name:
            return render_template("register.html", errorName = errorName, name = name)
        if not password:
            return render_template("register.html", errorPassword = errorPassword, name = name)
        if len(userName) > 0:
            return render_template("register.html", errorExists = errorExists, name = name)
        if not password == confirmation:
            return render_template("register.html", errorPasswordC = errorPasswordC, name = name)
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", name, generate_password_hash(password))
        return login()
    return render_template("register.html")

@app.route ("/home", methods=["GET","POST"])
def home():
    user_id = session["user_id"]
    text = request.form.get("ckeditor")
    if request.method == "POST":
        currentTime = db.execute("SELECT CURRENT_TIMESTAMP")[0]["CURRENT_TIMESTAMP"]
        db.execute("INSERT INTO users_text (text_id, text, d1) VALUES(?,?,?)",user_id, text, currentTime)
        text = db.execute("SELECT * FROM users_text WHERE text_id = ?", user_id)
        return render_template("home.html",text = text)
    if request.method == "GET":
        text = db.execute("SELECT * FROM users_text WHERE text_id = ?", user_id)
        return render_template("home.html",text = text)