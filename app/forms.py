from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("姓名", validators=[DataRequired(), Length(max=80)])
    email = StringField("電子郵件", validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField("主旨", validators=[Length(max=150)])
    message = TextAreaField("訊息內容", validators=[DataRequired(), Length(max=2000)])
