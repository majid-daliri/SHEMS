from app import db


class EnrolledDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_location_id = db.Column(db.Integer, db.ForeignKey('service_location.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('device_model.id'), nullable=False)
    events = db.relationship('EventData', backref='enrolled_device', lazy=True)
    service_location = db.relationship('ServiceLocation', backref='enrolled_devices')
