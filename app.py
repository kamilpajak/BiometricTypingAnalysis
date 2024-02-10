from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, g, session
from sqlalchemy.exc import IntegrityError

from extensions import db
from feature_calculator import FeatureCalculator
from forms import RegistrationForm, LoginForm
from keystroke_processor import KeystrokeProcessor
from models.models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Or another database URI
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_request
def create_tables():
    if not hasattr(g, 'db_created'):
        db.create_all()
        # Remove the handler so it only runs once
        app.before_request_funcs[None].remove(create_tables)


@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check whether user already exists
        user_by_email = User.query.filter_by(email=form.email.data).first()
        if user_by_email:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        user_by_username = User.query.filter_by(username=form.username.data).first()
        if user_by_username:
            flash('Username already taken. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Create a new user with the form data
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)

        # Add the new user to the database
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:  # Catching a specific SQLAlchemy IntegrityError
            db.session.rollback()
            flash('There was an issue creating the account. Please try again.', 'danger')
            return redirect(url_for('register'))
        except Exception as e:  # Catching any other exceptions that might occur
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.clear()  # This clears all data stored in the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/analyze_keystrokes', methods=['POST'])
def analyze_keystrokes():
    key_events = request.json
    processor = KeystrokeProcessor()
    keystrokes = processor.process_key_events(key_events)
    feature_calculator = FeatureCalculator()
    features = feature_calculator.calculate_features(keystrokes)
    return jsonify({'message': 'Keystrokes analyzed successfully', 'data': features})


@app.before_request
def before_request():
    app.logger.debug('Incoming request: %s %s', request.method, request.url)
    if request.method == 'POST':
        app.logger.debug('Request data: %s', request.get_data(as_text=True))


@app.after_request
def after_request(response):
    # Add headers to both force the latest IE rendering engine or Chrome Frame,
    # and also to cache the rendered page for 10 minutes.
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    app.logger.debug('Response status: %s', response.status)
    if not response.direct_passthrough:
        app.logger.debug('Response data:\n%s', response.get_data(as_text=True))
    else:
        app.logger.debug('Response data: not available (passthrough mode)')
    return response


if __name__ == '__main__':
    app.run(debug=True)
