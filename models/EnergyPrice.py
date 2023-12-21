from app import db


class EnergyPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(10), db.ForeignKey('address.zip_code'), nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Float, nullable=False)
