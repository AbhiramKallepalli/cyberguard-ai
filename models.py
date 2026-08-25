from flask_login import UserMixin
from datetime import datetime
from extensions import db

# Table 1 — Users
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scans = db.relationship('Scan', backref='user', lazy=True)

# Table 2 — Scans
class Scan(db.Model):
    __tablename__ = 'scans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    total_events = db.Column(db.Integer, default=0)
    flagged_count = db.Column(db.Integer, default=0)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)
    flagged_events = db.relationship('FlaggedEvent', backref='scan', lazy=True)

# Table 3 — Flagged Events
class FlaggedEvent(db.Model):
    __tablename__ = 'flagged_events'
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'), nullable=False)
    anomaly_score = db.Column(db.Float, nullable=False)
    risk_category = db.Column(db.String(20), nullable=False)
    plain_english = db.Column(db.Text, nullable=False)
    top_factors = db.Column(db.Text, nullable=False)
    flagged_at = db.Column(db.DateTime, default=datetime.utcnow)
    llm_responses = db.relationship('LLMResponse', backref='event', lazy=True)

# Table 4 — LLM Responses
class LLMResponse(db.Model):
    __tablename__ = 'llm_responses'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('flagged_events.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    asked_at = db.Column(db.DateTime, default=datetime.utcnow)