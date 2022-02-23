from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, FileField, IntegerField
from wtforms.validators import DataRequired, Optional, Length, URL, InputRequired


class CreateGift(FlaskForm):
    """
    форма для создания подарка
    """
    img = FileField('Загрузить изображение', validators=[Optional()])
    name = StringField(validators=[DataRequired(),
                                   Length(min=5, max=100, )], render_kw={"placeholder": "Название"})
    price = IntegerField(validators=[DataRequired(),InputRequired()], render_kw={"placeholder": "Цена"})
    url = StringField(validators=[DataRequired(message='Укажите сылку чтоб другие смогли найти этот товар'),
                                  URL()], render_kw={"placeholder": "Ссылка на товар"})
    submit = SubmitField('Опубликовать')


