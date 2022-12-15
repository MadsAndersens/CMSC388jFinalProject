from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import UpdateProfileForm
from ..models import User, Question, Answer
from .likes_over_time import likes_over_time

profile = Blueprint("profile", __name__)

@profile.route("/account", methods=["GET", "POST"])
@login_required
def account():
    print("Test account")
    profile_form = UpdateProfileForm()
    user = User.objects(username=current_user.username).first()
    questions = Question.objects(commenter=user)
    answers = Answer.objects(commenter=user)

    likes_plot = likes_over_time(user.likes_over_time) if len(user.likes_over_time) != 0 else None


    if profile_form.validate_on_submit():
        current_user.modify(username=profile_form.username.data)
        current_user.save()
        return redirect(url_for("profile.account"))


    return render_template("account.html",
                           title="Account",
                           profile_form=profile_form,
                           questions=questions,
                           answers=answers,
                           likes_plot=likes_plot)
