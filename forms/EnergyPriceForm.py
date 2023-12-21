from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, FloatField, SubmitField
from wtforms.validators import DataRequired


class EnergyPriceForm(FlaskForm):
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    hour = DateTimeLocalField('Hour', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    rate = FloatField('Rate', validators=[DataRequired()])
    submit = SubmitField('Add Energy Price')