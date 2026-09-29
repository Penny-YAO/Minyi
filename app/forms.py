from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import DateField, IntegerField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, URL, ValidationError

from app.models import AdminUser


class ContactForm(FlaskForm):
    name = StringField("姓名", validators=[DataRequired(), Length(max=80)])
    email = StringField("電子郵件", validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField("主旨", validators=[Length(max=150)])
    message = TextAreaField("訊息內容", validators=[DataRequired(), Length(max=2000)])


class LoginForm(FlaskForm):
    username = StringField("帳號", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("密碼", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("登入")


class AdminUserForm(FlaskForm):
    username = StringField("帳號", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("密碼", validators=[DataRequired(), Length(min=8, max=120, message="密碼長度需為 8 到 120 個字元")])
    email = StringField("信箱", validators=[DataRequired(), Email(message="請輸入有效的電子郵件"), Length(max=120)])
    created_at = DateField("建立日期", validators=[DataRequired()], default=date.today)
    submit = SubmitField("新增帳號")

    def validate_username(self, field):
        if AdminUser.query.filter_by(username=field.data).first():
            raise ValidationError("此帳號已存在")


class WorkForm(FlaskForm):
    title = StringField("作品名稱", validators=[DataRequired(), Length(max=150)])
    category = StringField("分類", validators=[Optional(), Length(max=80)])
    description = TextAreaField("作品說明", validators=[Optional(), Length(max=4000)])
    image = FileField(
        "封面圖片",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "僅限圖片檔案（jpg, png, gif, webp）"),
            FileSize(max_size=5 * 1024 * 1024, message="圖片檔案大小不可超過 5MB"),
        ],
    )
    video = FileField(
        "作品影片",
        validators=[
            Optional(),
            FileAllowed(["mp4", "webm", "ogg", "mov"], "僅限影片檔案（mp4, webm, ogg, mov）"),
            FileSize(max_size=50 * 1024 * 1024, message="影片檔案大小不可超過 50MB（Supabase 免費版單檔上限）"),
        ],
    )
    link = StringField("外部連結", validators=[Optional(), Length(max=255), URL(require_tld=True, message="請輸入有效的網址")])
    order = IntegerField(
        "排序（數字越小越前面）",
        validators=[Optional(), NumberRange(min=0, max=9999)],
        default=0,
    )
    submit = SubmitField("儲存")


class PartnerForm(FlaskForm):
    name = StringField("合作廠商", validators=[DataRequired(), Length(max=120)])
    software = StringField("建置的軟體名稱", validators=[DataRequired(), Length(max=150)])
    started_on = DateField("合作日期", validators=[DataRequired()], default=date.today)
    submit = SubmitField("儲存")
