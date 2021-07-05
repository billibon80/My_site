from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, URL
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField


class FormatStories(FlaskForm):
    date = StringField("Date Story", validators=[DataRequired(message=""), Length(min=10, max=10, message="")])
    chapter = TextAreaField("Name Chapter", validators=[DataRequired(message=""), Length(max=250, message="")])
    title = TextAreaField("Name Title", validators=[DataRequired(message=""), Length(max=250, message="")])
    subtitle = TextAreaField("Your Subtitle", validators=[DataRequired(message=""), Length(max=250, message="")])
    body = TextAreaField("Text Story", validators=[DataRequired(message="")])
    img = StringField("Img for Story")
    main_img = StringField("Img for Chapter")
    new_story = BooleanField("It's New Story")
    submit = SubmitField("Add Story")


class FormatNovel(FlaskForm):
    date = StringField("Date Format yyyy-mm-dd", validators=[DataRequired(message=''), Length(max=10, min=10, message="")])
    title = TextAreaField("Name Your Novel", validators=[DataRequired(message=''), Length(max=250, message="")])
    subtitle = TextAreaField("Subtitle of Novel", validators=[DataRequired(message=''), Length(max=250, message="")])
    body = TextAreaField("Text of Novel", validators=[DataRequired(message='')])
    img = StringField("Img for Novel")
    gif = StringField("Add Path of GIF")
    submit = SubmitField("Add Novel")


class FormatNews(FlaskForm):
    date = StringField("Date Format yyyy-mm-dd", validators=[DataRequired(), Length(max=10, min=10, message='')])
    title = StringField("Your Name Title News", validators=[DataRequired(), Length(max=20, message='')])
    subtitle = TextAreaField("Your Subtitle News", validators=[DataRequired(), Length(max=110, message='')])
    body = TextAreaField("Text of News", validators=[DataRequired(), Length(max=250, message='')])
    img = StringField("Img for News")
    submit = SubmitField("Add News")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Logged In")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(message="Required fields")])
    password = PasswordField("Password", validators=[DataRequired(message="Required fields")])
    name = StringField("Name", validators=[DataRequired(message="Required fields")])
    submit = SubmitField("Sign Me Up")