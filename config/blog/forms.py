from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, EmailField, PasswordField, TextAreaField, validators, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(),
                                                   validators.Length(min=4, max=25)])
    email = EmailField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password',
                             validators=[validators.DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Email already exists')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(),
                                                   validators.Length(min=4, max=25)])

    password = PasswordField('Password',
                             validators=[validators.DataRequired()])


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(),
                                                   validators.Length(min=4, max=25)])
    email = EmailField('Email', validators=[validators.DataRequired()])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username already exists')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email already exists')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[validators.DataRequired()])
    text = TextAreaField('Text', validators=[validators.DataRequired()])
