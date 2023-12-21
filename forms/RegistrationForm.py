from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegistrationForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    name = StringField('Name')
    billing_address_id = StringField('Billing Address ID')
    submit = SubmitField('Register')