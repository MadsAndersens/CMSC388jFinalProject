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
from flask_talisman import Talisman
from flask_mail import Mail

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
    app.config['SECRET_KEY'] = b'\xe4\x9eap\x9b\xd1\xa4\xbe\x9f\x1b\xad\xfaq;6A'

    from .profile.routes import profile
    from .forum.routes import forum
    from .loginregistration.routes import loginreg

    db.init_app(app)
    mail = Mail(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    #This allows us to still use the js scripts
    #csp = {
       # 'script-src': ["https://code.jquery.com/jquery-3.4.1.slim.min.js",
      #                 "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
     #                  "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
    #                   "h#ttps://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"]
   # }

    #Talisman(app, content_security_policy=csp)

    app.register_blueprint(loginreg)
    app.register_blueprint(profile)
    app.register_blueprint(forum)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
