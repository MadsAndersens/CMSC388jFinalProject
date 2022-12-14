from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import UpdateProfileForm
from ..models import User, Question, Answer

profile = Blueprint("profile", __name__)

@profile.route("/account", methods=["GET", "POST"])
@login_required
def account():
    profile_form = UpdateProfileForm()
    user = User.objects(username=current_user.username).first()
    questions = Question.objects(commenter=user)
    answers = Answer.objects(commenter=user)

    if profile_form.validate_on_submit():
        current_user.modify(username=profile_form.username.data)
        current_user.save()
        return redirect(url_for("profile.account"))

    return render_template("account.html", title="Account", profile_form=profile_form, questions=questions, answers=answers)
