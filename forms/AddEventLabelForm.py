from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddEventLabelForm(FlaskForm):
    label_name = StringField('Event Label', validators=[DataRequired()])
    submit = SubmitField('Add Label')