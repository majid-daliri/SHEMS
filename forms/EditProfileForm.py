from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    billing_address_id = StringField('Billing Address ID', validators=[InputRequired()])
    submit = SubmitField('Save Changes')