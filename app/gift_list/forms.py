from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired, Optional, Length, URL, InputRequired


class CreateGift(FlaskForm):
    """
    Gift form
    """
    img = FileField('Upload Image ', validators=[Optional()])
    name = StringField(validators=[DataRequired(),
                                   Length(min=5, max=100, )], render_kw={"placeholder": "Name "})
    price = IntegerField(validators=[DataRequired(),InputRequired()], render_kw={"placeholder": "Price"})
    url = StringField(validators=[DataRequired(message='Share the link so others can find this product'),
                                  URL()], render_kw={"placeholder": "Product link "})
    submit = SubmitField('Publish')


