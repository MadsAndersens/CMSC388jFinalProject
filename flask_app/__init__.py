from flask import Flask, render_template, request, redirect, url_for
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
import os
from datetime import datetime

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax"
    )
    #set secret key
    app.config['SECRET_KEY'] = b'\xe3\x9eap\x9b\xd1\xa4\xbe\x9f\x1b\xad\xfaq;6A'

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    #Import here to avoid circular imports
    from .users.routes import users
    from .forum.routes import forum

    app.register_blueprint(users)
    app.register_blueprint(forum)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"
    #print(app.url_map)
    return app
