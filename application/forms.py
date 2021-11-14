from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

class form_post(FlaskForm):
    title = StringField(u'title', [Length(max=100)])
    body = TextAreaField(u'body', [InputRequired(), Length(max=1000)])
    upload = FileField('image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'gif'])
    ])
    submit = SubmitField(u'Post')