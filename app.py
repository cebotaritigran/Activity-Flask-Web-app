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


# home page
@app.route("/")
def index():
    return render_template("index.html")


# LOGIN PAGE
@app.route("/login", methods=["GET","POST"])
def login():
    # log in user if all the error checks went ok
    session.clear()
    if request.method == "POST":
        errorName = "Please enter a user name"
        errorPassword = "Please enter a valid password"
        errorWrong = "invalid username and/or password"
        # checks if user entered a username
        if not request.form.get("username"):
            return render_template("login.html", errorName = errorName)
        #checks if user entered a password
        elif not request.form.get("password"):
            return render_template("login.html", errorPassword = errorPassword)
        
        # searching if username exist
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # checking if username exist
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", errorWrong = errorWrong)
    
        session["user_id"] = rows[0]["id"]

        return redirect("/posts")
    # else direct to login page 
    else:
        return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# REGISTER PAGE
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


# POSTS PAGE
@app.route ("/posts", methods=["GET","POST"])
@login_required
def posts():
    user_id = session["user_id"]
    texts = db.execute("SELECT * FROM users_text WHERE text_id = ?", user_id)
    return render_template("posts.html",text = texts)


# CREATING POSTS
@app.route ("/createpost", methods=["GET","POST"])
@login_required
def createpost():
    user_id = session["user_id"]
    title = request.form.get("title")
    text = request.form.get("ckeditor")

    # error checking
    if request.method == "POST":
        errorNoTitle = "Please enter a title"
        errorNoText = "Please write something before submitting"
        
        if not title:
            title = "No Title"
        if not text:
            return render_template("createpost.html", errorNoText = errorNoText, title = title)
        currentTime = db.execute("SELECT CURRENT_TIMESTAMP")[0]["CURRENT_TIMESTAMP"]
        db.execute("INSERT INTO users_text (text_id, text, d1, title) VALUES(?,?,?,?)",user_id, text, currentTime, title)
        texts = db.execute("SELECT * FROM users_text WHERE text_id = ?", user_id)
        return redirect ("/posts")
    return render_template("createpost.html")


# BUTTON TO EDIT POSTS
@app.route ("/editpostbutton", methods=["GET","POST"])
@login_required
def editpostbutton():
    user_id = session["user_id"]
    historyid = request.form.get("id")
    if id:
        title = db.execute("SELECT title FROM users_text WHERE history_id = ? AND text_id = ?", historyid, user_id)[0]["title"]
        text = db.execute("SELECT text FROM users_text WHERE history_id = ? AND text_id = ?", historyid, user_id)[0]["text"]
        return render_template("editpost.html", title = title, text = text, id = historyid)


@app.route ("/editpost", methods=["GET", "POST"])
@login_required
def editpost():
    user_id = session["user_id"]
    historyid = request.form.get("id")
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("ckeditor")

        errorNoTitle = "Please enter a title"
        errorNoText = "Please write something before submitting"

        if not title:
            title = "No Title"
        if not text:
            return render_template("editpost.html", errorNoText = errorNoText, title = title)

        db.execute("UPDATE users_text SET title = ?, text = ? WHERE text_id = ? AND history_id = ?", title, text, user_id, historyid)
        return redirect("/posts")
    return redirect("/posts")
    

@app.route ("/deletepost", methods=["POST"])
@login_required
def deletepost():
    # history id is an id that is different for every user and every post, so that we can delete a post easily
    historyid = request.form.get("id")
    if id:
        db.execute("DELETE FROM users_text WHERE history_id = ?", historyid)
    return redirect("/posts")

@app.route ("/createtodo", methods=["GET","POST"])
@login_required
def createtodo():
    # Creating todo
    user_id = session["user_id"]
    title = request.form.get("title")
    todo = request.form.get("ckeditor")
    day = request.form.get("day")
    month = request.form.get("month")
    year = request.form.get("year")
    # error checking
    if request.method == "POST":
        errorNoTitle = "Please enter a title"
        errorNoText = "Please write something before submitting"
        errorNoDay = "Please enter a valid date"
        errorNoMonth = "Please enter a valid date"
        errorNoYear = "Please enter a valid date"

        if not title:
            return render_template("createtodo.html", errorNoTitle = errorNoTitle, todo = todo, day = day, month = month, year = year)
        if not todo:
            return render_template("createtodo.html", errorNoText = errorNoText, title = title, day = day, month = month, year = year )
        if not day:
            return render_template("createtodo.html", errorNoDay = errorNoDay, title = title, todo = todo, month = month, year = year ) 
        if not month:
            return render_template("createtodo.html", errorNoMonth = errorNoMonth, title = title, todo = todo, day = day, year = year)
        if not year:
            return render_template("createtodo.html", errorNoYear = errorNoYear, title = title, todo = todo, day = day, month = month)
        # checking if date is numeric
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return render_template("createtodo.html", errorNoDay = errorNoDay, title = title, todo = todo)

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


@app.route ("/edittodobutton", methods=["GET","POST"])
@login_required
def edittodobutton():
    user_id = session["user_id"]
    historyid = request.form.get("id")
    if id:
        title = db.execute("SELECT title FROM users_todo WHERE history_id_todo = ? AND todo_id = ?", historyid, user_id)[0]["title"]
        todo = db.execute("SELECT todo FROM users_todo WHERE history_id_todo = ? AND todo_id = ?", historyid, user_id)[0]["todo"]
        day = db.execute("SELECT day FROM users_todo WHERE history_id_todo = ? AND todo_id = ?", historyid, user_id)[0]["day"]
        month = db.execute("SELECT month FROM users_todo WHERE history_id_todo = ? AND todo_id = ?", historyid, user_id)[0]["month"]
        year = db.execute("SELECT year FROM users_todo WHERE history_id_todo = ? AND todo_id = ?", historyid, user_id)[0]["year"]
        return render_template("edittodo.html", title = title, todo = todo, id = historyid, day = day, month = month, year = year)


@app.route ("/edittodo", methods=["GET", "POST"])
@login_required
def edittodo():
    user_id = session["user_id"]
    historyid = request.form.get("id")
    if request.method == "POST":
        title = request.form.get("title")
        todo = request.form.get("ckeditor")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        errorNoTitle = "Please enter a title"
        errorNoText = "Please write something before saving"
        errorNoDay = "Please enter a valid date"
        errorNoMonth = "Please enter a valid date"
        errorNoYear = "Please enter a valid date"

        if not title:
            return render_template("edittodo.html", errorNoTitle = errorNoTitle, todo = todo, day = day, month = month, year = year)
        if not todo:
            return render_template("edittodo.html", errorNoText = errorNoText, title = title, day = day, month = month, year = year)
        if not day:
            return render_template("edittodo.html", errorNoDay = errorNoDay, title = title, todo = todo, month = month, year = year) 
        if not month:
            return render_template("edittodo.html", errorNoMonth = errorNoMonth, title = title, todo = todo, day = day, year = year)
        if not year:
            return render_template("edittodo.html", errorNoYear = errorNoYear, title = title, todo = todo, day = day, month = month)
        # checking if date is numeric
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return render_template("edittodo.html", errorNoDay = errorNoDay, todo = todo, title = title)

        db.execute("UPDATE users_todo SET title = ?, todo = ?, day = ?, month = ?, year = ? WHERE todo_id = ? AND history_id_todo = ?",
            title, todo, day, month, year, user_id, historyid)
        return redirect("/todos")
    return redirect("/todos")


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
    user_id = session["user_id"]
    if request.method == "POST":
        seconds = int(request.form["seconds"])
        session["seconds"] = seconds
        minutes = int(request.form["minutes"])
        session["minutes"] = minutes

        title = request.form.get("title")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        errorNoSeconds = "Enter a valid time"
        errorNoMinutes = "Enter a valid time"
        errorNoTitle = "Please enter a title"
        errorNoDay = "Please enter a valid date"
        errorNoMonth = "Please enter a valid date"
        errorNoYear = "Please enter a valid date"

        if not title:
            return render_template("timer.html", errorNoTitle = errorNoTitle)
        if isinstance(seconds, int) is not True or isinstance(minutes, int) is not True:
            return render_template("timer.html", errorNoSeconds = errorNoSeconds, errorNoMinutes = errorNoMinutes)
        if not day:
            return render_template("timer.html", errorNoDay = errorNoDay) 
        if not month:
            return render_template("timer.html", errorNoMonth = errorNoMonth)
        if not year:
            return render_template("timer.html", errorNoYear = errorNoYear)
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return render_template("timer.html", errorNoDay = errorNoDay)

        db.execute("INSERT INTO activity (activity_id, title, minutes, seconds, month, day, year) VALUES (?,?,?,?,?,?,?)",
            user_id, title, minutes, seconds, month, day, year)

        history_id = db.execute("SELECT history_id_activity FROM activity WHERE activity_id = ? ORDER BY history_id_activity DESC LIMIT 1 ", user_id)
        
        return redirect("/timecounter")
    if request.method == "GET":
        return render_template("timer.html")

@app.route("/timecounter", methods=["GET","POST"])
@login_required
def timecounter():
    user_id = session["user_id"]

    history_id = db.execute("SELECT history_id_activity FROM activity WHERE activity_id = ? ORDER BY history_id_activity DESC LIMIT 1 ", user_id)
    history = int(history_id[0]["history_id_activity"])

    if request.method == "POST":
        seconds = request.form.get("seconds")
        minutes = request.form.get("minutes")

        db.execute("UPDATE activity SET minutes = ?, seconds = ? WHERE history_id_activity = ? AND activity_id = ?",
            minutes, seconds, history, user_id)

        return redirect("/timer")
    return render_template("timecounter.html", seconds = session["seconds"], minutes = session["minutes"], history_id = history)

@app.route("/activity", methods=["GET","POST"])
@login_required
def activity():
    user_id = session["user_id"]
    activity = db.execute("SELECT * FROM activity WHERE activity_id = ?", user_id)
    return render_template("activity.html", activity = activity)

@app.route ("/deleteactivity", methods=["POST"])
@login_required
def deleteactivity():
    # history id is an id that is different for every post so that we can delete a post easily
    historyid = request.form.get("id")
    if id:
        db.execute("DELETE FROM activity WHERE history_id_activity = ?", historyid)
    return redirect("/activity")