from datetime import datetime
from app import db


class TeamMember(db.Model):
    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<TeamMember {self.name}>"


class Work(db.Model):
    __tablename__ = "works"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Work {self.title}>"


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage {self.email}>"
