from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import InputRequired


class EditServiceLocationForm(FlaskForm):
    customer = StringField('Customer', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    unit_number = StringField('Unit Number', validators=[InputRequired()])
    date_taken_over = DateField('Date Taken Over', validators=[InputRequired()])
    square_footage = IntegerField('Square Footage', validators=[InputRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[InputRequired()])
    occupants = IntegerField('Occupants', validators=[InputRequired()])
    submit = SubmitField('Save Changes')