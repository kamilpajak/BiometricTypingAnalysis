# capture_routes.py
import random

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    jsonify,
    request,
)

from feature_calculator import FeatureCalculator
from keystroke_processor import KeystrokeProcessor

capture_bp = Blueprint("capture", __name__, template_folder="templates")

phrases = ["Quick brown", "Lazy dog", "Jumped over"]


# Define the index route for capture which will serve as the new home page
@capture_bp.route("/", endpoint="index")
def index():
    if "user_id" in session:
        phrase_to_type = random.choice(phrases)
        return render_template("capture.html", phrase_to_type=phrase_to_type)
    return redirect(url_for("auth.login"))


@capture_bp.route("/get_new_phrase")
def get_new_phrase():
    random_phrase = random.choice(phrases)
    return jsonify({"newPhrase": random_phrase})


@capture_bp.route("/analyze_keystrokes", methods=["POST"])
def analyze_keystrokes():
    data = request.json
    key_events = data.get("key_events")
    if key_events is not None:
        processed_data = KeystrokeProcessor().process_key_events(key_events)
        features = FeatureCalculator().calculate_features(processed_data)
        return jsonify(
            {"message": "Keystrokes analyzed successfully", "data": features}
        )
    else:
        return jsonify({"error": "No key_events data found"}), 400
