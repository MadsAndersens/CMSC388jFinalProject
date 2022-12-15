from flask import Blueprint, redirect, url_for, render_template, flash, request,send_file
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import UpdateProfileForm
from ..models import User, Question, Answer

import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns

profile = Blueprint("profile", __name__)

@profile.route("/account", methods=["GET", "POST"])
@login_required
def account():
    print("Test account")
    profile_form = UpdateProfileForm()
    user = User.objects(username=current_user.username).first()
    questions = Question.objects(commenter=user)
    answers = Answer.objects(commenter=user)
    likes_present = False if user.total_likes == 0 else True

    if profile_form.validate_on_submit():
        current_user.modify(username=profile_form.username.data)
        current_user.save()
        return redirect(url_for("profile.account"))


    return render_template("account.html",
                           title="Account",
                           profile_form=profile_form,
                           questions=questions,
                           answers=answers,
                           likes_present=likes_present)

@profile.route("/vizualise_likes", methods=["GET", "POST"])
@login_required
def vizualise_likes():
    user = User.objects(username=current_user.username).first()
    list_of_likes = user.likes_over_time
    x = list_of_likes[:][0]
    y = list_of_likes[:][1]
    fig = sns.lineplot(x=x, y=y)
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

