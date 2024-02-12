import random

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, g, session
from sqlalchemy.exc import IntegrityError

from extensions import db
from feature_calculator import FeatureCalculator
from forms import RegistrationForm, LoginForm
from keystroke_processor import KeystrokeProcessor
from models.models import User

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session management
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

# Initialize database with app
db.init_app(app)

# Predefined phrases for typing test
phrases = ["Quick brown", "Lazy dog", "Jumped over"]


# Create database tables before first request if not already created
@app.before_request
def create_tables():
    if not hasattr(g, 'db_created'):
        db.create_all()
        app.before_request_funcs[None].remove(create_tables)  # Remove handler to run only once


# Main page route
@app.route('/')
def index():
    return redirect(url_for('capture'))


# Capture page route
@app.route('/capture')
def capture():
    if 'user_id' in session:
        return render_template('capture.html')  # Show capture page if logged in
    else:
        return redirect(url_for('login'))  # Redirect to login if not logged in


# Route to get a new random phrase as JSON
@app.route('/get_new_phrase')
def get_new_phrase():
    random_phrase = random.choice(phrases)  # Select a random phrase
    return jsonify({'newPhrase': random_phrase})


# User registration route
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check for existing user
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Create and add new user to database
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('There was an issue creating the account. Please try again.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)


# User login route
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


# User logout route
@app.route("/logout")
def logout():
    session.clear()  # Clear session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# Route to analyze keystrokes
@app.route('/analyze_keystrokes', methods=['POST'])
def analyze_keystrokes():
    data = request.json
    key_events = data.get('key_events')
    if key_events is not None:
        processed_data = KeystrokeProcessor().process_key_events(key_events)
        features = FeatureCalculator().calculate_features(processed_data)
        return jsonify({'message': 'Keystrokes analyzed successfully', 'data': features})
    else:
        return jsonify({'error': 'No key_events data found'}), 400


# Log incoming requests
@app.before_request
def before_request():
    app.logger.debug(f'Incoming request: {request.method} {request.url}')


# Log and modify response headers
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    app.logger.debug(f'Response status: {response.status}')
    return response


if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
