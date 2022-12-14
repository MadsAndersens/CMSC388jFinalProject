from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField,EmailField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

class SearchForm(FlaskForm):
    search_query = StringField("Search", validators=[InputRequired()])
    submit = SubmitField("Submit")
