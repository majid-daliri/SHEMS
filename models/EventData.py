from app import db
from datetime import datetime

class EventData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('enrolled_device.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('event_label.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
