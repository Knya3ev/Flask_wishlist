from tkinter.tix import Form

from flask import flash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from flask_login import current_user
from ..models import User


class RegistrationForm(FlaskForm):
    """
    Форма для созданния акаунта пользователя
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash('Эта электронная почта уже используется','danger')
            raise ValidationError()

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            flash('Пользователь с таким ником уже существует', 'danger')
            raise ValidationError()


class LoginForm(FlaskForm):
    """
    Форма для входа пользователей
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Update(RegistrationForm, ):
    img = FileField(validators=[Optional()])
    old_password = PasswordField('Password', validators=[Optional()])
    password = PasswordField('New Password', validators=[Optional(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Update')

    def validate_email(self, field):
        if current_user.email != field.data:
            super().validate_email(field)

    def validate_username(self, field):
        if current_user.username != field.data:
            super().validate_username(field)
