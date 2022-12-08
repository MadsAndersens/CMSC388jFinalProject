# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from . import app, bcrypt

'''View functions for the Flask app'''

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")
