from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

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
            raise ValidationError('Эта электронная почта уже используется')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Пользователь с таким ником уже существует')


class LoginForm(FlaskForm):
    """
    Форма для входа пользователей
    """
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    submit = SubmitField('Login')

