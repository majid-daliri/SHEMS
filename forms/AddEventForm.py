from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateTimeLocalField, IntegerField
from wtforms.validators import InputRequired, DataRequired


class AddEventForm(FlaskForm):
    timestamp = DateTimeLocalField('Timestamp', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    label_id = SelectField('Label', coerce=int, validators=[InputRequired()])
    value = IntegerField('Value', validators=[InputRequired()])
    submit = SubmitField('Add Event')