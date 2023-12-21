from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
