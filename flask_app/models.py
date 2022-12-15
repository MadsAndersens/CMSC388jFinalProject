from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Question(db.Document):

    commenter = db.ReferenceField(User, required=True)
    title = db.StringField(required=True, unique=True)
    description = db.StringField(description=True)
    date = db.StringField(required=True)

class Answer(db.Document):
    commenter = db.ReferenceField(User, required=True)
    question = db.ReferenceField(Question, required=True)
    description = db.StringField(description=True)
    date = db.StringField(required=True)
