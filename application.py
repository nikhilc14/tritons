import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required


# Configure application
app = Flask(__name__)

#Might need later stuff<input type = 'text' id = 'search' name ='search' placeholder='Page you want to visit'>#<button class ='btn-sm'>Search</button>
#might need later export FLASK_APP=application.py
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///user.db")

#Ensure reponses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    #If users try register themselves
    if request.method == "POST" :
        #Getting required info
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = request.form.get("username")

        #if users skips entering something
        if not username :
            return ("Enter username")
        if not password :
            return ("Enter password")
        if not confirmation:
            return ("Enter confirmation")
        if password != confirmation :
            return ("Passwords do not match")

        #Checking is users already there
        dup_user = db.execute("SELECT * FROM users WHERE username = ? ",request.form.get("username"))

        #Adding users info to table if users isn't already there
        if len(dup_user) == 0:
            hash = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users(username,hash) VALUES (?,?)",username,hash)
            return redirect("login")

        else :
            return ("Username already exists")

    else :
        return render_template("register.html")

    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return ("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("invalid username and/or password..........please go to register page and register if not registered")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        db.execute("INSERT INTO cart(user_id,username) VALUES(?,?)",session["user_id"],request.form.get("username"))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("login")

@app.route("/products")
@login_required
def products():
    return render_template("products.html")


@app.route("/innovation")
@login_required
def innovation():
    return render_template("innovation.html")


@app.route("/aboutus")
@login_required
def aboutus():
    return render_template("aboutus.html")

@app.route("/addtocart1")
@login_required
def addtocart1():
    temp1 = db.execute("SELECT bottle,ath,vermi FROM cart WHERE user_id=:user_id",user_id = session["user_id"])
    bottle =temp1[0]["bottle"]
    bottle=bottle+1
    db.execute("UPDATE cart SET bottle = ? WHERE user_id = ?",bottle,session["user_id"])
    return render_template("products.html",bottle=bottle,bottle2=temp1[0]["ath"],bottle3=temp1[0]["vermi"])

@app.route("/addtocart2")
@login_required
def addtocart2():
    temp1 = db.execute("SELECT ath,vermi,bottle FROM cart WHERE user_id=:user_id",user_id = session["user_id"])
    bottle2 =temp1[0]["ath"]
    bottle2=bottle2+1
    db.execute("UPDATE cart SET ath = ? WHERE user_id = ?",bottle2,session["user_id"])
    return render_template("products.html",bottle2=bottle2,bottle=temp1[0]["bottle"],bottle3=temp1[0]["vermi"])

@app.route("/addtocart3")
@login_required
def addtocart3():
    temp1 = db.execute("SELECT vermi,ath,bottle FROM cart WHERE user_id=:user_id",user_id = session["user_id"])
    bottle3 =temp1[0]["vermi"]
    bottle3=bottle3+1
    db.execute("UPDATE cart SET vermi = ? WHERE user_id = ?",bottle3,session["user_id"])
    return render_template("products.html",bottle3=bottle3, bottle=temp1[0]["bottle"], bottle2=temp1[0]["ath"])

@app.route("/addtocart4")
@login_required
def addtocart4():
    return "Please contact us by email ...if you want to buy plastic from the tritons"


@app.route("/contactus",methods=["GET","POST"])
@login_required
def contactus():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        concern = request.form.get("concern")
        
        if not name:
            return "Enter your name "
        if not email:
            return "Enter your email"
        if not concern:
            return "Enter your concern"

        db.execute("INSERT INTO contact(name,email,concern) VALUES(?,?,?)",name,email,concern)
        return redirect("/")

    else:
        return render_template("contactus.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return (e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

