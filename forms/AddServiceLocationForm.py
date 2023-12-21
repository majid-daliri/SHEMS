from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddServiceLocationForm(FlaskForm):
    customer = StringField('Customer')
    address = StringField('Address')
    unit_number = StringField('Unit Number')
    date_taken_over = DateField('Date Taken Over', validators=[DataRequired()])
    square_footage = IntegerField('Square Footage')
    bedrooms = IntegerField('Bedrooms')
    occupants = IntegerField('Occupants')
    submit = SubmitField('Add Service Location')