from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, BooleanField


class ObjectForm(FlaskForm):
    name = StringField("Название")
    place = StringField("Регион")
    category = StringField("Категория значения")
    type = StringField("Вид объекта")
    in_UNESCO = BooleanField('Состоит в Юнеско?')

    picture = FileField('Фото', validators=[FileAllowed([
        'jpg', 'png'])])

    submit = SubmitField("Подтвердить")
