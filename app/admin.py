import os
import uuid
from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from app import db
from app.forms import LoginForm, WorkForm
from app.models import Work

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

UPLOAD_URL_PREFIX = "/static/uploads/works/"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("請先登入後台管理。", "error")
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def _save_upload(file_storage, subfolder):
    """儲存上傳檔案至 static/uploads/works/<subfolder>，回傳可直接用於 <img>/<video> 的網址路徑。"""
    if not file_storage or not file_storage.filename:
        return None

    ext = file_storage.filename.rsplit(".", 1)[-1].lower() if "." in file_storage.filename else ""
    unique_name = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex

    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(folder, exist_ok=True)
    file_storage.save(os.path.join(folder, unique_name))

    return f"{UPLOAD_URL_PREFIX}{subfolder}/{unique_name}"


def _delete_upload(url_path):
    """刪除先前上傳的檔案（僅限本站上傳的檔案，外部連結不處理）。"""
    if not url_path or not url_path.startswith(UPLOAD_URL_PREFIX):
        return
    relative_path = url_path[len(UPLOAD_URL_PREFIX):]
    full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], relative_path)
    if os.path.isfile(full_path):
        os.remove(full_path)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        password_hash = current_app.config["ADMIN_PASSWORD_HASH"]
        username_ok = form.username.data == current_app.config["ADMIN_USERNAME"]
        password_ok = bool(password_hash) and check_password_hash(password_hash, form.password.data)

        if username_ok and password_ok:
            session.clear()
            session["admin_logged_in"] = True
            session.permanent = True
            flash("登入成功！", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.dashboard"))

        flash("帳號或密碼錯誤。", "error")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    flash("已登出。", "success")
    return redirect(url_for("admin.login"))


@admin_bp.route("/works")
@login_required
def dashboard():
    works = Work.query.order_by(Work.order.asc(), Work.created_at.desc()).all()
    return render_template("admin/dashboard.html", works=works)


@admin_bp.route("/works/new", methods=["GET", "POST"])
@login_required
def new_work():
    form = WorkForm()
    if form.validate_on_submit():
        work = Work(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data,
            link=form.link.data,
            order=form.order.data or 0,
        )
        work.image_url = _save_upload(form.image.data, "images")
        work.video_url = _save_upload(form.video.data, "videos")

        db.session.add(work)
        db.session.commit()
        flash("作品已新增！", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/work_form.html", form=form, work=None)


@admin_bp.route("/works/<int:work_id>/edit", methods=["GET", "POST"])
@login_required
def edit_work(work_id):
    work = Work.query.get_or_404(work_id)
    form = WorkForm(obj=work)

    if form.validate_on_submit():
        work.title = form.title.data
        work.category = form.category.data
        work.description = form.description.data
        work.link = form.link.data
        work.order = form.order.data or 0

        new_image_url = _save_upload(form.image.data, "images")
        if new_image_url:
            _delete_upload(work.image_url)
            work.image_url = new_image_url

        new_video_url = _save_upload(form.video.data, "videos")
        if new_video_url:
            _delete_upload(work.video_url)
            work.video_url = new_video_url

        db.session.commit()
        flash("作品已更新！", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/work_form.html", form=form, work=work)


@admin_bp.route("/works/<int:work_id>/delete", methods=["POST"])
@login_required
def delete_work(work_id):
    work = Work.query.get_or_404(work_id)
    _delete_upload(work.image_url)
    _delete_upload(work.video_url)
    db.session.delete(work)
    db.session.commit()
    flash("作品已刪除。", "success")
    return redirect(url_for("admin.dashboard"))
