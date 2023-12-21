from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class EnrollDeviceForm(FlaskForm):
    device_type = SelectField('Device Type', coerce=int, validators=[DataRequired()])
    service_location = SelectField('Service Location', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enroll Device')