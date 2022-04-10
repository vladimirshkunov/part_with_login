from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, HiddenField, FileField
from wtforms.validators import DataRequired


class GalleryForm(FlaskForm):
    hid = HiddenField('Категория')
    file = FileField('Файл')
    submit = SubmitField('Отправить')
