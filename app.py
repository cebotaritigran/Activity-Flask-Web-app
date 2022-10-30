import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_ckeditor import CKEditor
from wtforms import StringField, SubmitField

from login import login_required

# configuring application
app = Flask(__name__)
app.secret_key = "test123"
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
    # log in user if all the error checks went ok
    session.clear()
    if request.method == "POST":
        errorName = "Please enter a user name"
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

        return render_template("index.html")
    # else direct to login page 
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET","POST"])
def register():
    # getting data
    name = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    userName = db.execute("SELECT username FROM users WHERE username = ?", name)

    # error messages if user couldn't sign up
    errorName = "Please enter an user name"
    errorPassword = "Please enter a valid password"
    errorPasswordC = "Please confirm your password"
    errorExists = "User name entered already exists"

    # error checking
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

# page tht displays posts
@app.route ("/posts", methods=["GET","POST"])
@login_required
def posts():
    user_id = session["user_id"]
    texts = db.execute("SELECT * FROM users_text WHERE text_id = ?", user_id)
    return render_template("posts.html",text = texts)

@app.route ("/createpost", methods=["GET","POST"])
@login_required
def createpost():
    # TO DO creating post
    user_id = session["user_id"]
    title = request.form.get("title")
    text = request.form.get("ckeditor")
    if request.method == "POST":
        currentTime = db.execute("SELECT CURRENT_TIMESTAMP")[0]["CURRENT_TIMESTAMP"]
        db.execute("INSERT INTO users_text (text_id, text, d1, title) VALUES(?,?,?,?)",user_id, text, currentTime, title)
        texts = db.execute("SELECT * FROM users_text WHERE text_id = ?", user_id)
        return redirect ("/posts")
    return render_template("createpost.html")

@app.route ("/deletepost", methods=["POST"])
@login_required
def deletepost():
    # history id is an id that is different for every post so that we can delete a post easily
    historyid = request.form.get("id")
    if id:
        db.execute("DELETE FROM users_text WHERE history_id = ?", historyid)
    return redirect("/posts")

@app.route ("/createtodo", methods=["GET","POST"])
@login_required
def createtodo():
    # TO DO creating post
    user_id = session["user_id"]
    title = request.form.get("title")
    todo = request.form.get("todo")
    day = request.form.get("day")
    month = request.form.get("month")
    year = request.form.get("year")
    if request.method == "POST":
        db.execute("INSERT INTO users_todo (todo_id, todo, title, month, day, year) VALUES(?,?,?,?,?,?)",user_id, todo, title, month, day, year)
        todos = db.execute("SELECT * FROM users_todo WHERE todo_id = ?", user_id)
        return redirect ("/todos")
    return render_template("createtodo.html")

@app.route ("/todos", methods=["GET","POST"])
@login_required
def todos():
    user_id = session["user_id"]
    todos = db.execute("SELECT * FROM users_todo WHERE todo_id = ?", user_id)
    return render_template("todos.html",todo = todos)

@app.route ("/deletetodo", methods=["POST"])
@login_required
def deletetodo():
    # history id is an id that is different for every post so that we can delete a post easily
    historyid = request.form.get("id")
    if id:
        db.execute("DELETE FROM users_todo WHERE history_id_todo = ?", historyid)
    return redirect("/todos")

@app.route("/timer", methods=["GET", "POST"])
@login_required
def timer():
    if request.method == "POST":
        seconds = int(request.form["seconds"])
        session["seconds"] = seconds
        minutes = int(request.form["minutes"])
        session["minutes"] = minutes
        return redirect("/timer2")
    if request.method == "GET":
        return render_template("timer.html")

@app.route("/timer2", methods=["GET","POST"])
@login_required
def timer2():
    return render_template("timer2.html", seconds = session["seconds"], minutes = session["minutes"])