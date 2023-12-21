import sqlite3

from flask import Flask, flash, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import DateTimeLocalField, FloatField
from datetime import datetime
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, InputRequired

from forms.AddEventForm import AddEventForm
from forms.AddEventLabelForm import AddEventLabelForm
from forms.AddServiceLocationForm import AddServiceLocationForm
from forms.DeviceModelForm import DeviceModelForm
from forms.EditProfileForm import EditProfileForm
from forms.EditServiceLocationForm import EditServiceLocationForm
from forms.EnergyPriceForm import EnergyPriceForm
from forms.EnrollDeviceForm import EnrollDeviceForm
from forms.LoginForm import LoginForm
from forms.RegistrationForm import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
DB_PATH = "/Users/machouse/WorkSpace/Smart-Home-Energy-Management-System/instance/site.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.User import User
from models.Device import DeviceModel
from models.ServiceLocation import ServiceLocation
from models.Address import Address
from models.EventData import EventData
from models.EnergyPrice import EnergyPrice
from models.EnrolledDevice import EnrolledDevice
from models.EventLabel import EventLabel


@app.route('/')
def index():
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])
        return render_template('index.html', message=f"Welcome, {current_user.username}!", current_user=current_user)
    else:
        return render_template('index.html', message="Welcome to the Energy Monitoring System!", current_user=None)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    error_message = None

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            error_message = "Username already exists. Please choose a different one."
        else:
            new_user = User(username=form.username.data, password=form.password.data, name=form.name.data,
                            billing_address_id=form.billing_address_id.data)
            db.session.add(new_user)
            db.session.commit()

            # Set the user's session after successful registration
            session['user_id'] = new_user.id

            return redirect(url_for('index'))

    return render_template('register.html', form=form, error_message=error_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = None

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            if not user:
                error_message = "Invalid username. Please check your username and try again."
            else:
                error_message = "Invalid password. Please check your password and try again."

    return render_template('login.html', form=form, current_user=None, error_message=error_message)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()

    if 'user_id' in session:
        user = User.query.get(session['user_id'])

        if form.validate_on_submit():
            user.name = form.name.data
            user.billing_address_id = form.billing_address_id.data
            db.session.commit()

            return redirect(url_for('profile'))

        form.name.data = user.name
        form.billing_address_id.data = user.billing_address_id

        return render_template('edit_profile.html', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/add_service_location', methods=['GET', 'POST'])
def add_service_location():
    form = AddServiceLocationForm()

    if form.validate_on_submit():
        new_location = ServiceLocation(
            user_id=session['user_id'],
            address=form.address.data,
            unit_number=form.unit_number.data,
            square_footage=form.square_footage.data,
            bedrooms=form.bedrooms.data,
            occupants=form.occupants.data
        )
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('add_service_location.html', form=form)


@app.route('/edit_service_location/<int:location_id>', methods=['GET', 'POST'])
def edit_service_location(location_id):
    form = EditServiceLocationForm()
    location = ServiceLocation.query.get(location_id)

    if form.validate_on_submit():
        location.address = form.address.data
        location.unit_number = form.unit_number.data
        location.square_footage = form.square_footage.data
        location.bedrooms = form.bedrooms.data
        location.occupants = form.occupants.data
        db.session.commit()
        return redirect(url_for('profile'))

    form.address.data = location.address
    form.unit_number.data = location.unit_number
    form.square_footage.data = location.square_footage
    form.bedrooms.data = location.bedrooms
    form.occupants.data = location.occupants

    return render_template('edit_service_location.html', form=form, location=location)


@app.route('/remove_service_location/<int:location_id>')
def remove_service_location(location_id):
    location = ServiceLocation.query.get(location_id)
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/add_device_model', methods=['GET', 'POST'])
def add_device_model():
    form = DeviceModelForm()

    if form.validate_on_submit():
        new_device_model = DeviceModel(
            type=form.type.data,
            model_number=form.model_number.data
        )
        db.session.add(new_device_model)
        db.session.commit()
        return redirect(url_for('add_device_model'))

    return render_template('add_device_model.html', form=form)


@app.route('/enroll_device', methods=['GET', 'POST'])
def enroll_device():
    form = EnrollDeviceForm()

    form.device_type.choices = [(model.id, f"{model.type} - {model.model_number}") for model in DeviceModel.query.all()]

    user_service_locations = ServiceLocation.query.filter_by(user_id=session['user_id']).all()
    form.service_location.choices = [(location.id, location.address) for location in user_service_locations]

    if form.validate_on_submit():
        selected_device_model = DeviceModel.query.get(form.device_type.data)
        selected_service_location = ServiceLocation.query.get(form.service_location.data)

        enrolled_device = EnrolledDevice(
            device_model=selected_device_model,
            service_location=selected_service_location
        )
        db.session.add(enrolled_device)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('enroll_device.html', form=form)


@app.route('/enrolled_devices')
def enrolled_devices():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.service_locations:
            service_location = user.service_locations[0]
            enrolled_devices = EnrolledDevice.query.filter_by(service_location_id=service_location.id).all()
            return render_template('enrolled_devices.html', user=user, enrolled_devices=enrolled_devices)
        else:
            flash("Please add a service location before viewing enrolled devices.", 'warning')
            return redirect(url_for('add_service_location'))
    else:
        return redirect(url_for('login'))


@app.route('/remove_enrolled_device/<int:device_id>')
def remove_enrolled_device(device_id):
    enrolled_device = EnrolledDevice.query.get(device_id)
    if enrolled_device:
        db.session.delete(enrolled_device)
        db.session.commit()

    return redirect(url_for('profile'))


@app.route('/add_event_label', methods=['GET', 'POST'])
def add_event_label():
    form = AddEventLabelForm()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    if form.validate_on_submit():
        cur.execute("INSERT INTO Event_Label (label_name) VALUES (?)", (form.label_name.data,))
        con.commit()
        con.close()

        return redirect(url_for('index'))

    return render_template('add_event_label.html', form=form)


@app.route('/add_event/<int:device_id>', methods=['GET', 'POST'])
def add_event(device_id):
    form = AddEventForm()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT id, label_name FROM Event_Label")
    event_labels = cur.fetchall()

    form.label_id.choices = [(label[0], label[1]) for label in event_labels]

    if form.validate_on_submit():
        if not isinstance(form.timestamp.data, datetime):
            form.timestamp.data = datetime.strptime(form.timestamp.data, '%Y-%m-%dT%H:%M')
        cur.execute(
            "INSERT INTO Event_Data (device_id, timestamp, label_id, value) VALUES (?, ?, ?, ?)",
            (device_id, form.timestamp.data, form.label_id.data, form.value.data)
        )
        con.commit()
        con.close()

        return redirect(url_for('add_event', device_id=device_id))

    return render_template('add_event.html', form=form, device_id=device_id)


@app.route('/add_energy_price', methods=['GET', 'POST'])
def add_energy_price():
    form = EnergyPriceForm()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    if form.validate_on_submit():
        if not isinstance(form.hour.data, datetime):
            form.hour.data = datetime.strptime(form.hour.data, '%Y-%m-%dT%H:%M')

        cur.execute(
            "INSERT INTO Energy_Price (zip_code, hour, rate) VALUES (?, ?, ?)",
            (form.zip_code.data, form.hour.data, form.rate.data)
        )
        con.commit()
        con.close()

        return redirect(url_for('index'))

    return render_template('add_energy_price.html', form=form)


@app.route('/energy_consumption/<int:service_location_id>/<string:time_resolution>')
def energy_consumption(service_location_id, time_resolution):
    if time_resolution == 'day':
        query = """
            SELECT DATE(e.Timestamp) AS date, SUM(e.Value) AS total_energy
            FROM event_data e
            JOIN enrolled_device ed ON e.Device_ID = ed.id
            WHERE ed.Service_Location_ID = :service_location_id
            GROUP BY date
        """
        con2 = sqlite3.connect(DB_PATH)
        cur2 = con2.cursor()
        data = cur2.execute(query, (service_location_id,)).fetchall()
    elif time_resolution == 'month':
        query = """
            SELECT strftime('%m', e.Timestamp) AS month, SUM(e.Value) AS total_energy
            FROM event_data e
            JOIN enrolled_device ed ON e.Device_ID = ed.id
            WHERE ed.Service_Location_ID = :service_location_id
            GROUP BY month
        """
        con2 = sqlite3.connect(DB_PATH)
        cur2 = con2.cursor()
        data = cur2.execute(query, (service_location_id,)).fetchall()
        pass
    else:
        return "Invalid time resolution"

    # Extract data for the chart
    labels = [str(row[0]) for row in data]
    values = [row[1] for row in data]
    con2.close()
    return render_template('energy_consumption.html', labels=labels, values=values, time_resolution=time_resolution)


if __name__ == '__main__':
    app.run(debug=True)
