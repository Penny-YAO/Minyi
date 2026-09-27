from datetime import datetime
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app import db
from app.forms import LoginForm, WorkForm
from app.models import AdminUser, Work
from app.storage import StorageError, delete_upload, save_upload

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get("admin_user_id")
        user = db.session.get(AdminUser, user_id) if user_id else None
        if not user or not user.is_active:
            # 帳號被刪除或停用時，已登入的 session 也一併失效
            session.pop("admin_logged_in", None)
            session.pop("admin_user_id", None)
            flash("請先登入後台管理。", "error")
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def _upload_media(form):
    """上傳表單中的圖片與影片，回傳 (image_url, video_url)；失敗時清掉這次已上傳的檔案再拋出錯誤。"""
    image_url = save_upload(form.image.data, "images")
    try:
        video_url = save_upload(form.video.data, "videos")
    except StorageError:
        delete_upload(image_url)
        raise
    return image_url, video_url


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()

        if user and user.is_active and user.check_password(form.password.data):
            user.last_login_at = datetime.utcnow()
            db.session.commit()

            session.clear()
            session["admin_logged_in"] = True
            session["admin_user_id"] = user.id
            session.permanent = True
            flash("登入成功！", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.dashboard"))

        flash("帳號或密碼錯誤。", "error")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_user_id", None)
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
        try:
            work.image_url, work.video_url = _upload_media(form)
        except StorageError as e:
            flash(f"檔案上傳失敗：{e}", "error")
            return render_template("admin/work_form.html", form=form, work=None)

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

        try:
            new_image_url, new_video_url = _upload_media(form)
        except StorageError as e:
            db.session.rollback()
            flash(f"檔案上傳失敗：{e}", "error")
            return render_template("admin/work_form.html", form=form, work=work)

        if new_image_url:
            delete_upload(work.image_url)
            work.image_url = new_image_url
        if new_video_url:
            delete_upload(work.video_url)
            work.video_url = new_video_url

        db.session.commit()
        flash("作品已更新！", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/work_form.html", form=form, work=work)


@admin_bp.route("/works/<int:work_id>/delete", methods=["POST"])
@login_required
def delete_work(work_id):
    work = Work.query.get_or_404(work_id)
    delete_upload(work.image_url)
    delete_upload(work.video_url)
    db.session.delete(work)
    db.session.commit()
    flash("作品已刪除。", "success")
    return redirect(url_for("admin.dashboard"))
