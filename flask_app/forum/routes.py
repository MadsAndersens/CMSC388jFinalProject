from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user
from .. import bcrypt
from flask_app.forms import SearchForm
from ..models import User
from flask_app import db


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