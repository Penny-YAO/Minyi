from flask import Blueprint, render_template, redirect, url_for, flash, current_app

from app import db
from app.models import TeamMember, Work, ContactMessage
from app.forms import ContactForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """首頁：工作室核心理念"""
    philosophy_points = [
        {
            "title": "以人為本",
            "description": "每一次設計都從理解使用者與客戶的真實需求出發。",
            "icon": "heart",
        },
        {
            "title": "精益求精",
            "description": "在細節中堅持品質，讓每件作品都經得起檢驗。",
            "icon": "target",
        },
        {
            "title": "誠信合作",
            "description": "透明溝通、如期交付，與客戶建立長久的信任關係。",
            "icon": "shield",
        },
        {
            "title": "持續創新",
            "description": "不斷學習新技術與新思維，為專案注入創意能量。",
            "icon": "bulb",
        },
    ]
    featured_works = (
        Work.query.filter(Work.image_url.isnot(None), Work.image_url != "")
        .order_by(Work.order.asc(), Work.created_at.desc())
        .limit(6)
        .all()
    )
    specialties = [
        {
            "title": "個人網站架設",
            "description": "為個人品牌、工作室或作品集打造專屬網站，快速上線、輕鬆維護。",
            "icon": "user",
        },
        {
            "title": "一頁式網頁製作",
            "description": "聚焦單一目標的一頁式網站，適合活動宣傳、產品發表，訊息更集中。",
            "icon": "layout",
        },
        {
            "title": "企業管理系統架設",
            "description": "依需求客製化企業內部管理系統，整合作業流程，提升團隊效率。",
            "icon": "building",
        },
        {
            "title": "AI 技術整合",
            "description": "介接最新 AI 技術，協助內容產生、客服互動與後台管理，讓網站經營更省力。",
            "icon": "spark",
        },
    ]
    return render_template(
        "index.html",
        philosophy_points=philosophy_points,
        featured_works=featured_works,
        specialties=specialties,
    )


@main_bp.route("/team")
def team():
    """團隊成員介紹"""
    members = TeamMember.query.order_by(TeamMember.order.asc(), TeamMember.id.asc()).all()
    placeholder_count = max(0, 4 - len(members))
    return render_template(
        "team.html", members=members, placeholder_count=placeholder_count
    )


@main_bp.route("/portfolio")
def portfolio():
    """案例實績"""
    works = Work.query.order_by(Work.order.asc(), Work.created_at.desc()).all()
    return render_template("portfolio.html", works=works)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """聯絡方式與聯絡表單"""
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
        )
        db.session.add(message)
        db.session.commit()
        flash("訊息已送出，我們會盡快與您聯繫！", "success")
        return redirect(url_for("main.contact"))

    return render_template(
        "contact.html", form=form, contact_email=current_app.config["CONTACT_EMAIL"]
    )
