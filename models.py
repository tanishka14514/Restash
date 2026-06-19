"""
Restash - Database Models
----------------------------
Defines User accounts, their token wallets, and rest history.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date, datetime
import secrets

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(64), unique=True, default=lambda: secrets.token_hex(32))
    last_sleep_report = db.Column(db.Float, default=0)
    security_answer_hash = db.Column(db.String(255), nullable=True)
    referred_by = db.Column(db.String(150), nullable=True)  # email of referrer

    # Wallet fields
    balance = db.Column(db.Integer, default=500)  # welcome bonus
    daily_sleep_earned = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.String(20), default=lambda: str(date.today()))
    daily_ads_watched = db.Column(db.Integer, default=0)
    last_ad_time = db.Column(db.Float, default=0)

    # Rest identity features
    streak_days = db.Column(db.Integer, default=0)
    last_rest_date = db.Column(db.String(20), default="")
    total_rest_minutes = db.Column(db.Float, default=0)
    last_sleep_report = db.Column(db.DateTime, nullable=True)
    def reset_daily_cap_if_needed(self):
        today = str(date.today())
        if self.last_reset != today:
            self.daily_sleep_earned = 0
            self.daily_ads_watched = 0
            self.last_reset = today


class RestLog(db.Model):
    """One row per reported rest (sleep or shutdown). Powers the stats dashboard."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    minutes = db.Column(db.Float, default=0)
    awarded = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now)

from datetime import datetime

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), default="New chat")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pinned = db.Column(db.Boolean, default=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    role = db.Column(db.String(10))  # "user" or "ai"
    content = db.Column(db.Text)
    deep_mode = db.Column(db.Boolean, default=False)
    tokens_cost = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)