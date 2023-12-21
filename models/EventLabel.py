from app import db


class EventLabel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.String(50), nullable=False, unique=True)
    events = db.relationship('EventData', backref='event_label', lazy=True)
