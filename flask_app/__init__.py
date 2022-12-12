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
app = Flask(__name__)
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/FinalProject"
app.config["SECRET_KEY"] = b'\xde\xb0"\x9d!\x13nElU\xb9\x84/\xf2z\xe2'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)
