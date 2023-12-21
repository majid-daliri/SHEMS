from app import db


class DeviceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    model_number = db.Column(db.String(50), nullable=False)
    enrolled_devices = db.relationship('EnrolledDevice', backref='device_model', lazy=True)
