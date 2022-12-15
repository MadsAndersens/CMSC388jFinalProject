from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, EmailField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Retype Password", validators=[InputRequired(), EqualTo("password")]
    )
    about_me = StringField("About Me", validators = [])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")
    
    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class UpdateProfileForm(FlaskForm):
    username = StringField("New Username", validators=[InputRequired(), Length(min=4, max=15)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data == current_user.username:
            raise ValidationError("Same username!")

        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

class QuestionForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    submit = SubmitField("Submit")


class AnswerForm(FlaskForm):
    answer = TextAreaField("Answer", validators=[InputRequired()])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    search_query = StringField("Search", validators=[InputRequired()])
    submit = SubmitField("Submit")