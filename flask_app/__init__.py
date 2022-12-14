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

from .loginregistration.routes import loginreg

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
    app.config['SECRET_KEY'] = b'\xe3\x9eap\x9b\xd1\xa4\xbe\x9f\x1b\xad\xfaq;6A'

    from .profile.routes import profile
    from .forum.routes import forum
    from .loginregistration.routes import loginreg

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(loginreg)
    app.register_blueprint(profile)
    app.register_blueprint(forum)




    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
