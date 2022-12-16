from flask import Blueprint, render_template, url_for, redirect, request, flash, Flask
from flask_login import current_user, login_required, login_user, logout_user
from flask_mongoengine import MongoEngine
from flask_mail import Mail, Message
from .. import bcrypt
from flask_app.forms import SearchForm, QuestionForm, AnswerForm,LikesForm
from ..models import User, Question, Answer
from flask_app import db
from datetime import datetime
from flask_app.utils import current_time

forum = Blueprint("forum", __name__)

app = Flask(__name__)
mail = Mail(app)
# I only got it to work with outlook 
MAIL_USERNAME = "" #'yourId@gmail.com' use an outlook account
MAIL_PASSWORD = "" # password don't merge if using your own

app.config['MAIL_SERVER']='smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
# Enter your own email credentials here for testing and remove
# before pushing on github
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@forum.route("/", methods=["GET", "POST"])
@forum.route("/forum", methods=["GET", "POST"])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for("forum.search_results", query=search_form.search_query.data))
    return render_template("index.html", search_form=search_form)

@forum.route("/see_all_questions",methods=["GET", "POST"])
def see_all_questions():
    all_posts = Question.objects.all()
    return render_template("see_all_questions.html", questions=all_posts)

#View function for searching in questions
@forum.route("/search_results/<query>", methods=["GET", "POST"])
def search_results(query):
    search_results = Question.objects(title__icontains=query)
    return render_template("search_results.html", search_results=search_results, query=query)

@forum.route("/question/<question_id>", methods=["GET", "POST"])
def see_question(question_id):
    question = Question.objects(id=question_id).first()
    answer_form = AnswerForm()
    likes_form = LikesForm()
    if answer_form.validate_on_submit():
        answer = Answer(
            commenter=current_user,
            question=question,
            description=answer_form.answer.data,
            date=current_time(),
        )
        answer.save()
        question.answers.append(answer)
        question.save()

        # Send email to person who asked question that a user answered
        msg = Message('Hello', sender = MAIL_USERNAME, recipients = [question.commenter.email,MAIL_USERNAME])
        msg.body = answer.commenter.username + "responded to your question!"
        mail.send(msg)

        return redirect(url_for("forum.see_question", question_id=question_id))

    if likes_form.validate_on_submit():
        question.likes += 1
        question.save()
        # Find the user who made the post and increment their total likes
        user = User.objects(username=question.commenter.username).first()
        user.total_likes += 1
        user.likes_over_time.append([current_time(),user.total_likes])
        user.save()
        return redirect(url_for("forum.see_question", question_id=question_id))

    return render_template("see_question.html",
                           question=question,
                           answer_form=answer_form,
                           answers=question.answers,
                           likes_form=likes_form)

# TODO make sure the route is correct
@forum.route("/posts", methods=["GET", "POST"])
@login_required
def make_post():
    # TODO make sure the below works
    form = QuestionForm()
    dublicate_flag = False
    try:
        if form.validate_on_submit() and current_user.is_authenticated:
            post = Question(
                commenter=current_user._get_current_object(),
                title=form.title.data,
                description=form.description.data,
                date=current_time(),
                likes=0,
            )
            post.save()
            print("test")
            return redirect(url_for("forum.see_question", question_id=post.id))
    except:
        dublicate_flag = True
        title = form.title.data
        ref = Question.objects(title = title).first()
        return render_template("make_post.html", form=form, id_reference=ref.id, dublicate_flag=dublicate_flag)

    return render_template("make_post.html", form=form)

  #  # TODO Figure out what questions should be... I think maybe we don't need this line below
  #  questions = Question.objects(commenter=current_user._get_current_object())

   # # TODO render appropriate template with corresponding data for it
   # return render_template("404.html", form=form)


# TODO make sure the route is correct
@forum.route("/posts/<post_title>", methods=["GET", "POST"])
@login_required
def make_reply(post_title):
    try:
        result = Question.objects(title=post_title)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("forum.login"))
    # TODO make sure the below works
    form = AnswerForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        post = Answer(
            commenter=current_user._get_current_object(),
            question=Question.objects(title=post_title),
            description=form.description.data,
            date=current_time()
        )
        post.save()
        return redirect(request.path)

    # TODO Figure out what answers should be...
    answers = Answer.objects(question=Question.objects(title=post_title))

    # TODO render appropriate template with corresponding data for it
    return render_template("404.html", form=form)

if __name__ == '__main__':
   app.run(debug = True)