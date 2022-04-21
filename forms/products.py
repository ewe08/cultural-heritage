from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, BooleanField, TextAreaField


class ObjectForm(FlaskForm):
    name = StringField("Название")
    place = StringField("Регион")
    category = StringField("Категория значения")
    type = StringField("Вид объекта")
    info = TextAreaField("Информация об объекте")
    in_UNESCO = BooleanField('Состоит в Юнеско?')

    picture = StringField("Ссылка фото на объект")

    submit = SubmitField("Подтвердить")
