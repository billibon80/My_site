import smtplib

from flask import Flask, render_template, request, url_for, redirect, abort, flash, Response
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_sqlalchemy import SQLAlchemy
from datetime import date as dt
from datetime import datetime
from smpt import PostSomeself
from forms import FormatStories, FormatNovel, FormatNews, LoginForm, RegisterForm, Comments, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from functools import wraps
import os
import urllib

# import sqlite3
#
#
# def add_column(database_name, table_name, column_name, data_type):
#
#     connection = sqlite3.connect(database_name)
#     cursor = connection.cursor()
#
#     if data_type == "Integer":
#         data_type_formatted = "INTEGER"
#     elif data_type == "String":
#         data_type_formatted = "VARCHAR()"
#
#     base_command = ("ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'")
#     sql_command = base_command.format(table_name=table_name, column_name=column_name, data_type=data_type_formatted)
#
#     cursor.execute(sql_command)
#     connection.commit()
#     connection.close()
#
# add_column('data-site.db', 'novel', 'gif', 'String')
show_story = 0
name_button = "Older Story →"
story_page = 1

# date = datetime.date.fromisoformat('2021-05-16')
# print(date.strftime('%b ru_RU.UTF-8'))
MAIL_CODE = os.environ.get("MAIL_CODE")
app = Flask(__name__, static_folder='static')

##CONNECT TO DB
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
ckeditor = CKEditor(app)
Bootstrap(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


## CONFIGURE TABLES
class Stories(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    chapter = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String, nullable=False)
    img = db.Column(db.String)
    main_img = db.Column(db.String)
    new_story = db.Column(db.Boolean)

    comments = relationship("Comment", back_populates="parent_stories")


class Novel(db.Model):
    __tablename__ = "novel"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String, nullable=False)
    img = db.Column(db.String)
    gif = db.Column(db.String)


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    subtitle = db.Column(db.String(110), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    img = db.Column(db.String)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    comments = relationship("Comment", back_populates="comment_author")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment_author = relationship("User", back_populates="comments")

    stories_id = db.Column(db.Integer, db.ForeignKey("stories.id"))
    parent_stories = relationship("Stories", back_populates="comments")


class Letter(db.Model):
    __tablename__ = "letters"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    text = db.Column(db.String, nullable=False)


db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.id == 1:
                return f(*args, **kwargs)
        return abort(404)

    return decorated_function


@app.route('/admin')
def admin_panel():
    if current_user.is_authenticated:
        if current_user.id == 1:
            global name_button
            global story_page
            global show_story
            news = db.session.query(News).order_by(db.desc(News.date)).all()
            posts = db.session.query(Stories).order_by(db.desc(Stories.date)).all()
            letter = db.session.query(Letter).order_by(db.desc(Letter.date)).first()

            return render_template("index_admin.html", all_posts=posts, dt=dt,
                                   story_page=story_page, datetime=datetime, news=news, letter=letter)
        flash("You have no enough access rights")
        return redirect(url_for("login"))
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.id == 1:
                    return redirect(url_for("admin_panel"))
                page = request.args.get('page')
                if page:
                    return redirect(url_for('show_post', index=page[page.find('/') + 1:], _anchor='text'))
                return redirect(url_for('get_new_posts'))
            flash("Invalid password")
        else:
            flash("That Email doesn't exist")

    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        )
        db.session.add(user)
        db.session.commit()
        load_user(user)
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_new_posts'))


# page edit Story
@app.route('/add_stories', methods=['GET', 'POST'])
@admin_only
def add_stories():
    form = FormatStories()
    button = "Add Story"
    if request.method == "GET":
        if form.date.data is None:
            form.date.data = datetime.now().strftime('%Y-%m-%d')
        if db.session.query(Stories).all():
            last_story = db.session.query(Stories).all()[-1]
            form.chapter.data = last_story.chapter
            form.main_img.data = last_story.main_img
        form.new_story.data = True
    if form.validate_on_submit():
        new_story = Stories(
            date=form.date.data,
            title=form.title.data,
            chapter=form.chapter.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img=form.img.data,
            main_img=form.main_img.data,
            new_story=form.new_story.data,
        )
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    return render_template('add_stories_admin.html', form=form, button=button, function='add_stories', id='')


@app.route('/update_story', methods=['GET', 'POST'])
@admin_only
def update_story():
    form = FormatStories()
    id = request.args.get('id')
    story = Stories.query.get(id)
    button = "Update Story"
    if request.method == "GET":
        form.date.data = story.date
        form.title.data = story.title
        form.chapter.data = story.chapter
        form.subtitle.data = story.subtitle
        form.body.data = story.body
        form.img.data = story.img
        form.main_img.data = story.main_img
        form.new_story.data = story.new_story

    if form.validate_on_submit():
        story.date = form.date.data
        story.title = form.title.data
        story.chapter = form.chapter.data
        story.subtitle = form.subtitle.data
        story.body = form.body.data
        story.img = form.img.data
        story.main_img = form.main_img.data
        story.new_story = form.new_story.data
        db.session.commit()
        return redirect(url_for('admin_panel'))
    return render_template('add_stories_admin.html', form=form, button=button, function='update_story', id=id)


@app.route('/delete_story')
@admin_only
def delete_story():
    id = request.args.get('id')
    story = Stories.query.get(id)
    db.session.delete(story)
    db.session.commit()
    return redirect(url_for('admin_panel'))


# page edit News
@app.route('/add_news', methods=['GET', 'POST'])
@admin_only
def add_news():
    form = FormatNews()
    button = "Add News"
    if request.method == "GET":
        if form.date.data is None:
            form.date.data = datetime.now().strftime('%Y-%m-%d')
    if form.validate_on_submit():
        new_news = News(
            date=form.date.data,
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img=form.img.data,
        )
        db.session.add(new_news)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    return render_template('add_news_admin.html', form=form, button=button, function='add_news', id='')


@app.route('/update_news', methods=['GET', 'POST'])
@admin_only
def update_news():
    form = FormatNews()
    id = request.args.get('id')
    story = News.query.get(id)
    copy = bool(request.args.get('copy') == "True")
    button = "Update News"

    if copy:
        button = "Copy & Add News"

    if request.method == "GET":
        form.date.data = story.date
        if copy:
            form.date.data = datetime.now().strftime('%Y-%m-%d')
        form.title.data = story.title
        form.subtitle.data = story.subtitle
        form.body.data = story.body
        form.img.data = story.img

    if form.validate_on_submit():
        if copy:
            new_news = News(
                date=form.date.data,
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                img=form.img.data,
            )
            db.session.add(new_news)
        else:
            story.date = form.date.data
            story.title = form.title.data
            story.subtitle = form.subtitle.data
            story.body = form.body.data
            story.img = form.img.data
        db.session.commit()
        return redirect(url_for('admin_panel'))
    return render_template('add_news_admin.html', form=form, button=button,
                           function='update_news', id=id, copy=copy)


@app.route('/delete_news')
@admin_only
def delete_news():
    id = request.args.get('id')
    story = News.query.get(id)
    db.session.delete(story)
    db.session.commit()
    return redirect(url_for('admin_panel'))


# novel edit
@app.route('/novel_admin')
@admin_only
def novel_admin():
    novels = db.session.query(Novel).order_by(db.desc(Novel.date)).all()
    return render_template('novel_admin.html', novels=novels, datetime=datetime, dt=dt)


@app.route('/add_novel', methods=['GET', 'POST'])
@admin_only
def add_novel():
    form = FormatNovel()
    button = "Add Novel"
    if request.method == "GET":
        if form.date.data is None:
            form.date.data = datetime.now().strftime('%Y-%m-%d')
    if form.validate_on_submit():
        new_novel = Novel(
            date=form.date.data,
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img=form.img.data,
            gif=form.gif.data,
        )
        db.session.add(new_novel)
        db.session.commit()
        return redirect(url_for('novel_admin'))
    return render_template('add_news_admin.html', form=form, button=button, function='add_novel', id='')


@app.route('/update_novel', methods=['GET', 'POST'])
@admin_only
def update_novel():
    form = FormatNovel()
    id = request.args.get('id')
    story = Novel.query.get(id)
    button = "Update Novel"
    if request.method == "GET":
        form.date.data = story.date
        form.title.data = story.title
        form.subtitle.data = story.subtitle
        form.body.data = story.body
        form.img.data = story.img
        form.gif.data = story.gif

    if form.validate_on_submit():
        story.date = form.date.data
        story.title = form.title.data
        story.subtitle = form.subtitle.data
        story.body = form.body.data
        story.img = form.img.data
        story.gif = form.gif.data
        db.session.commit()
        return redirect(url_for('novel_admin'))
    return render_template('add_news_admin.html', form=form, button=button,
                           function='update_novel', id=id, copy="")


@app.route('/delete_novel')
@admin_only
def delete_novel():
    id = request.args.get('id')
    story = Novel.query.get(id)
    db.session.delete(story)
    db.session.commit()
    return redirect(url_for('novel_admin'))


@app.route('/post/<int:index>/delete_comment')
@login_required
def delete_comment(index):
    id = request.args.get('comment_id')
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('show_post', index=index, _anchor='submit'))


@app.route('/letter_add', methods=['GET', 'POST'])
@admin_only
def add_letter():
    form = FormatStories()
    type_edit = request.args.get('type_edit')
    _id = request.args.get('_id')

    if form.validate_on_submit():
        if type_edit == 'add':
            new_letter = Letter(
                date=form.date.data,
                text=form.body.data
            )
            db.session.add(new_letter)
            db.session.commit()
        elif type_edit == 'update':
            letter = Letter.query.get(_id)
            letter.date = form.date.data
            letter.text = form.body.data
            db.session.commit()
        return redirect(url_for('admin_panel'))

    if type_edit == "delete":
        letter = Letter.query.get(_id)
        db.session.delete(letter)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    elif type_edit == "add":
        form.date.data = datetime.now().strftime('%Y-%m-%d')
        button = "Add Letter"
    elif type_edit == "update":
        letter = Letter.query.get(_id)
        form.date.data = letter.date
        form.body.data = letter.text
        button = "Update Letter"

    return render_template('add_letter_admin.html', form=form, type_edit=type_edit, copy="copy",
                           _id=_id, button=button, function='story')


# home page
@app.route('/')
@app.route('/home')
def get_new_posts():
    global name_button
    global story_page
    global show_story

    posts_id = 0
    news = db.session.query(News).order_by(db.desc(News.date)).all()
    posts = Stories.query.filter_by(new_story=True).order_by(db.desc(Stories.date)).all()
    if posts:
        posts_id = posts[-1].id - 1
    letter = Letter.query.order_by(db.desc(Letter.date)).first()
    name_button = "Older Story →"
    return render_template("index.html", all_posts=posts, dt=dt, name_button=name_button,
                           story_page=posts_id, datetime=datetime, news=news[:3], letter=letter)


@app.route('/story/<int:index>')
def get_old_posts(index):
    posts = db.session.query(Stories).filter_by(new_story=False).order_by(db.desc(Stories.date)).all()

    return render_template("previous_story.html", posts=posts, dt=dt, datetime=datetime, index=index - 1)


@app.route('/about')
def get_about():
    return render_template('about.html', datetime=datetime)


@app.route('/novel')
def get_novel():
    novels = db.session.query(Novel).order_by(db.desc(Novel.date)).all()
    return render_template('novel_1.html', novels=novels, datetime=datetime, dt=dt)


@app.route('/post/<int:index>', methods=['POST', 'GET'])
def show_post(index):
    form = Comments()
    stories = Stories.query.get(index)
    requested_post = Stories.query.get(index)
    msg_id = request.args.get('msg_id')
    answer = request.args.get('answer')
    further = request.args.get('further')
    show_message = request.args.get('show_message')
    _anchor = request.args.get('anchor')
    all_row = requested_post.body.split("\n")
    msg_index = [i for i in range(len(all_row)) if '{message}' in all_row[i]]
    show = request.args.get('show')

    if show_message:

        if msg_id in msg_index:
            msg_id = msg_index[msg_index.index(int(msg_id))]
        else:
            msg_id = int(msg_id) - 1

        return redirect(url_for('show_post', index=index, _anchor='newstring', show=show_message,
                                msg_index=msg_id, answer=int(answer), anchor=show_message))
    if further:
        if further == '0':
            return render_template('post.html', post=requested_post, datetime=datetime, dt=dt, form=form,
                                   msg_index=msg_index[0] + 1, answer=answer, show=show, anchor_msg=0)
    if msg_id:
        msg_id = int(msg_id.replace('msg_', ''))

        if msg_index.index(msg_id) + 1 == len(msg_index):
            if all_row.index(all_row[msg_index[msg_index.index(msg_id)]]) != len(all_row):
                _anchor = all_row.index(all_row[msg_index[msg_index.index(msg_id)] + 1])
            else:
                _anchor = all_row.index(all_row[msg_index[msg_index.index(msg_id)] - 1])
        else:
            _anchor = msg_index[msg_index.index(msg_id) + 1] - (msg_index[msg_index.index(msg_id) + 1] - msg_id) + 1

        if msg_index[-1] != msg_id:
            msg_index = msg_index[msg_index.index(msg_id) + 1]
        else:
            msg_index = len(all_row) - 1

        if answer:
            return redirect(url_for('show_post', index=index, _anchor='newstring', anchor=_anchor,
                                    msg_index=msg_index, answer=int(answer)))

        return redirect(url_for('show_post', index=index, _anchor='newstring', anchor=_anchor,
                                msg_index=msg_index))
    elif request.args.get('msg_index'):
        msg_index = int(request.args.get('msg_index')) + 1
    else:

        if msg_index:
            msg_index = msg_index[0] + 1
        else:
            msg_index = len(all_row)
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            author_id=current_user.id,
            stories_id=stories.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('show_post', index=index, _anchor="submit"))

    return render_template('post.html', post=requested_post, datetime=datetime, dt=dt, form=form,
                           msg_index=msg_index, answer=answer, show=show, anchor_msg=_anchor)


@app.route('/contact', methods=['POST', 'GET'])
def get_contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = PostSomeself(form.name.data, form.email.data,
                           form.phone.data, form.text.data)
        try:
            msg.connection_mail_ru("billibon80@mail.ru", MAIL_CODE)
        except:
            flash("What wrong! 😞😞😞 Your message don't send, sorry for this attempt!")
        return redirect(url_for("get_contact"))

    return render_template('contact.html', datetime=datetime, form=form)


if __name__ == "__main__":
    app.run(debug=True)
