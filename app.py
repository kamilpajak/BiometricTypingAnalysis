# app.py
from flask import Flask, redirect, url_for

from blueprints.auth_routes import auth_bp
from blueprints.capture_routes import capture_bp
from blueprints.keystroke_analysis_routes import keystroke_analysis_bp
from config import configure_app
from database import db

app = Flask(__name__)
configure_app(app)
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(capture_bp, url_prefix="/capture")
app.register_blueprint(keystroke_analysis_bp, url_prefix="/analysis")


@app.route("/")
def root():
    return redirect(url_for("capture.index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables here, at start-up
    app.run(debug=True)
