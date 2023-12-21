from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DeviceModelForm(FlaskForm):
    type = StringField('Device Type', validators=[DataRequired()])
    model_number = StringField('Model Number', validators=[DataRequired()])
    submit = SubmitField('Add Device Model')