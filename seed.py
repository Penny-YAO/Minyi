"""建立範例資料：團隊成員與作品。使用方式： python seed.py"""
from app import create_app, db
from app.models import TeamMember, Work
from app.team_profiles import PENNY_PHOTO, PENNY_PROFILE

app = create_app()

with app.app_context():
    if not TeamMember.query.first():
        db.session.add_all([
            TeamMember(
                name="家臻 Emily",
                role="美編",
                order=1,
            ),
            TeamMember(
                name="佩純 Penny",
                role="系統分析規劃",
                photo_url=PENNY_PHOTO,
                profile=PENNY_PROFILE,
                order=2,
            ),
            TeamMember(
                name="偉鈞 Leo",
                role="全端工程師 / 資料庫分析",
                order=3,
            ),
            TeamMember(
                name="佩彤 Wendy",
                role="全端工程師 / 資料庫分析",
                order=4,
            ),
        ])

    if not Work.query.first():
        db.session.add_all([
            Work(
                title="品牌識別設計 - 甘豆咖啡",
                category="品牌設計",
                description="為在地咖啡品牌打造完整視覺識別系統，包含 Logo、包裝與店面設計。",
                image_url="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=1200&q=80",
                order=1,
            ),
            Work(
                title="形象網站開發 - 日光工作室",
                category="網站開發",
                description="以簡約風格呈現攝影工作室作品集，並整合線上預約功能。",
                image_url="https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?auto=format&fit=crop&w=1200&q=80",
                order=2,
            ),
            Work(
                title="活動視覺設計 - 城市音樂節",
                category="平面設計",
                description="設計年度音樂節主視覺與周邊宣傳物，提升活動識別度。",
                image_url="https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=1200&q=80",
                order=3,
            ),
        ])

    db.session.commit()
    print("範例資料已建立完成。")
