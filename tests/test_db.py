import pytest
from flask import Flask
from extensions import db
from models import User, Scan, FlaggedEvent, LLMResponse


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_create_user(app):
    with app.app_context():
        user = User(name="Test User", email="test@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        found = User.query.filter_by(email="test@test.com").first()
        assert found is not None
        assert found.name == "Test User"


def test_create_scan_linked_to_user(app):
    with app.app_context():
        user = User(name="Test User", email="test2@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()

        scan = Scan(user_id=user.id, filename="test.csv", total_events=100, flagged_count=5)
        db.session.add(scan)
        db.session.commit()

        found = Scan.query.filter_by(filename="test.csv").first()
        assert found is not None
        assert found.user_id == user.id
        assert found.user.name == "Test User"


def test_create_flagged_event_linked_to_scan(app):
    with app.app_context():
        user = User(name="Test User", email="test3@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()

        scan = Scan(user_id=user.id, filename="test.csv", total_events=100, flagged_count=1)
        db.session.add(scan)
        db.session.commit()

        event = FlaggedEvent(
            scan_id=scan.id,
            anomaly_score=-0.25,
            risk_category="HIGH",
            plain_english="Suspicious activity detected",
            top_factors="unusual data volume, odd timing"
        )
        db.session.add(event)
        db.session.commit()

        found = FlaggedEvent.query.filter_by(scan_id=scan.id).first()
        assert found is not None
        assert found.risk_category == "HIGH"
        assert found.scan.filename == "test.csv"


def test_create_llm_response_linked_to_event(app):
    with app.app_context():
        user = User(name="Test User", email="test4@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()

        scan = Scan(user_id=user.id, filename="test.csv", total_events=100, flagged_count=1)
        db.session.add(scan)
        db.session.commit()

        event = FlaggedEvent(
            scan_id=scan.id,
            anomaly_score=-0.3,
            risk_category="HIGH",
            plain_english="Suspicious",
            top_factors="factor1, factor2"
        )
        db.session.add(event)
        db.session.commit()

        response = LLMResponse(
            event_id=event.id,
            question="Should I be worried?",
            response="Yes, this looks suspicious."
        )
        db.session.add(response)
        db.session.commit()

        found = LLMResponse.query.filter_by(event_id=event.id).first()
        assert found is not None
        assert found.question == "Should I be worried?"
        assert found.event.risk_category == "HIGH"


def test_email_must_be_unique(app):
    with app.app_context():
        user1 = User(name="User One", email="dup@test.com", password_hash="hashed")
        db.session.add(user1)
        db.session.commit()

        user2 = User(name="User Two", email="dup@test.com", password_hash="hashed")
        db.session.add(user2)
        with pytest.raises(Exception):
            db.session.commit()