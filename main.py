from flask import Flask, render_template, request, url_for, redirect, abort, flash
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_sqlalchemy import SQLAlchemy
from datetime import date as dt
from datetime import datetime
from smpt import PostSomeself
from forms import FormatStories, FormatNovel, FormatNews
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from functools import wraps
import os

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
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment_author = relationship("User", back_populates="comments")


db.create_all()

print(current_user)
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(404)
        return f(*args, **kwargs)

    return decorated_function()


@app.route('/admin')
def admin_panel():
    if current_user.is_authenticated:
        if current_user.id == 1:
            global name_button
            global story_page
            global show_story
            news = db.session.query(News).order_by(db.desc(News.date)).all()
            posts = db.session.query(Stories).order_by(db.desc(Stories.date)).all()

            return render_template("index_admin.html", all_posts=posts, dt=dt,
                                   story_page=story_page, datetime=datetime, news=news)
        flash("You have no enough access rights")
        return render_template("login_admin.html")
    return redirect(url_for("login"))


# page edit Story
@app.route('/add_stories', methods=['GET', 'POST'])
@admin_only
def add_stories():
    form = FormatStories()
    button = "Add Story"
    print('')
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
    print(form.validate_on_submit())
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
    print('update_novel'[-5:-1])
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


# home page
@app.route('/')
@app.route('/home')
def get_new_posts():
    global name_button
    global story_page
    global show_story

    news = db.session.query(News).order_by(db.desc(News.date)).all()
    posts = Stories.query.filter_by(new_story=True).order_by(db.desc(Stories.date)).all()
    show_story = 1
    story_page = 1
    name_button = "Older Story →"

    return render_template("index.html", all_posts=posts, dt=dt, name_button=name_button,
                           story_page=story_page, datetime=datetime, news=news[:3])


@app.route('/<int:index>')
def get_old_posts(index):
    global show_story
    global name_button
    global story_page

    story_page = index + 1
    number_open_stories = 2
    posts = db.session.query(Stories).filter_by(new_story=False).order_by(db.desc(Stories.date)).all()

    if show_story + number_open_stories < len(posts):
        show_story += number_open_stories
    else:
        show_story = len(posts)
        story_page -= 1
        name_button = "The End of Stories"
    return render_template("previous_story.html", all_posts=posts[0:show_story], dt=dt,
                           name_button=name_button, story_page=story_page, datetime=datetime)


@app.route('/about')
def get_about():
    return render_template('about.html', datetime=datetime)


@app.route('/novel')
def get_novel():
    novels = db.session.query(Novel).order_by(db.desc(Novel.date)).all()
    return render_template('novel_1.html', novels=novels, datetime=datetime, dt=dt)


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = Stories.query.get(index)
    return render_template('post.html', post=requested_post, datetime=datetime, dt=dt)


@app.route('/contact', methods=['POST', 'GET'])
def get_contact():
    method = request.method
    if method == "POST":
        data = request.form
        msg = PostSomeself(data['name'], data['email'], data['phone'], data['message'])
        try:
            msg.connection_mail_ru("billibon80@mail.ru", MAIL_CODE)
        except:
            method = "ERROR"

    return render_template('contact.html', datetime=datetime, method=method)


if __name__ == "__main__":
    app.run(debug=True)
