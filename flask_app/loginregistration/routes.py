from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import LoginForm, RegisterForm
from ..models import User

loginreg = Blueprint("loginreg", __name__)

@loginreg.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("forum.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.email.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("profile.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("loginreg.login"))

    return render_template("login.html", title="Login", form=form)

@loginreg.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("forum.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("loginreg.login"))

    return render_template("register.html", title="Register", form=form)

@loginreg.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("forum.index"))
