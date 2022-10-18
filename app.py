import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# configuring application
app = Flask(__name__)

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
    session.clear()
    #if request.method == "POST":


    return render_template("index.html") 

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