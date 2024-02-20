from werkzeug.security import generate_password_hash, check_password_hash

from database import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    keystroke_timing_features = db.relationship(
        "KeystrokeTimingFeatures", backref="users", lazy=True
    )

    def set_password(self, password):
        """
        Hashes the provided password and stores it in the password_hash attribute.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifies the provided password against the stored hashed password.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Provides a string representation of the User object, useful for debugging.
        """
        return f"<User {self.username}>"
