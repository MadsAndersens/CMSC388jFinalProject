from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user
from flask_mongoengine import MongoEngine
from .. import bcrypt
from flask_app.forms import SearchForm, QuestionForm
from ..models import User, Question, Answer
from flask_app import db
from datetime import datetime
from flask_app.utils import current_time


forum = Blueprint("forum", __name__)

@forum.route("/")
@forum.route("/forum")
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for("forum.search_results", query=search_form.search_query.data))
    return render_template("index.html", search_form=search_form)
@forum.route("/search_results/<query>", methods=["GET", "POST"])
def search_results(query):
    try:
        results = db.posts.search(query)
    except ValueError as e:
        return render_template("search_results.html", error_msg="No results found")
    return render_template("search_results.html", results=results)

# TODO make sure the route is correct
@forum.route("/posts/<post_title>", methods = ["GET","POST"])
@login_required
def make_post():

    # TODO make sure the below works
    form = QuestionForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        post= Question(
            commenter=current_user._get_current_object(),
            title=form.title.data,
            description = form.description.data,
            date = current_time()
        )
        post.save()

        return redirect(request.path)

    # TODO Figure out what questions should be...
    questions = Question.objects(commenter = current_user._get_current_object())
    
    # TODO render appropriate template with corresponding data for it
    return render_template(
        "404.html", form=form)