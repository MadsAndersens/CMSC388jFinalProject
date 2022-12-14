from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user

from .. import bcrypt
from .forms import SearchForm
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
    # TODO: Add search_results and html page