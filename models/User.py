from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    billing_address_id = db.Column(db.Integer, nullable=True)
    service_locations = db.relationship('ServiceLocation', backref='user', lazy=True)
