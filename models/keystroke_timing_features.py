# keystroke_timing_features.py
from datetime import datetime, timezone

from database import db


def calculate_features(keystrokes):
    """
    Calculates keystroke features based on the press and release times of Keystroke instances.
    """
    # Convert Keystroke instances to a list of dictionaries for the 'keystrokes' feature
    keystrokes_data = [
        {
            "key": ks.key,
            "press_time": ks.press_time,
            "release_time": ks.release_time,
        }
        for ks in keystrokes
    ]

    features = {
        "keystrokes": keystrokes_data,
        "press_to_press": [],
        "release_to_press": [],
        "press_to_release": [],
    }

    # Iterate through the keystrokes to calculate timing features
    for i, ks in enumerate(keystrokes):
        if i == 0:
            features["press_to_release"].append(ks.release_time - ks.press_time)
            continue

        prev_ks = keystrokes[i - 1]
        features["press_to_press"].append(ks.press_time - prev_ks.press_time)
        features["release_to_press"].append(ks.press_time - prev_ks.release_time)
        features["press_to_release"].append(ks.release_time - ks.press_time)

    return features


class KeystrokeTimingFeatures(db.Model):
    __tablename__ = "keystroke_timing_features"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    features = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, keystrokes, user_id):
        """
        Initializes a new instance of the KeystrokeTimingFeatures class,
        calculating features based on the provided keystrokes.

        :param keystrokes: List of Keystroke instances, where each instance contains attributes for key, press_time, and release_time.
        :param user_id: The ID of the user associated with this set of keystroke timing features.
        """
        self.created_at = datetime.now(timezone.utc)
        self.features = calculate_features(keystrokes)
        self.user_id = user_id

    def __repr__(self):
        return f"<KeystrokeTimingFeatures(id='{self.id}', created_at='{self.created_at}', user_id='{self.user_id}')>"
