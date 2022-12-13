from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user

from .. import bcrypt
from ..forms import QuestionForm, AnswerForm, SearchForm
from ..models import User

forum = Blueprint("forum", __name__)

@forum.route("/", methods=["GET", "POST"])
def index():
    search_form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("forum.search_results", query=search_form.search.data))

    return render_template("index.html", form=search_form)

@forum.route("/results/<query>", methods=["GET"])
def search_results(query):
    try: 
        result = forum_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("main.index"))
    
    return render_template("query.html")
    # TODO: Add search_results and html page