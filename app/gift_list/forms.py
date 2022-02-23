from flask import flash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, FileField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, URL


class CreateGift(FlaskForm):
    """
    форма для создания подарка
    """
    img = FileField('Загрузить изображение', validators=[Optional()])
    name = StringField(validators=[DataRequired(),
                                   Length(min=5, max=40, )], render_kw={"placeholder": "Название"})
    price = StringField(validators=[DataRequired(), NumberRange(1)], render_kw={"placeholder": "Цена"})
    url = StringField(validators=[DataRequired(message='Укажите сылку чтоб другие смогли найти этот товар'),
                                  URL()], render_kw={"placeholder": "Ссылка на товар"})
    submit = SubmitField('Опубликовать')
