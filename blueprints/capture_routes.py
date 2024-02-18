# capture_routes.py
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


@capture_bp.route("/", endpoint="index")
def index():
    if "user_id" in session:
        return render_template("capture.html")
    return redirect(url_for("auth.login"))


@capture_bp.route("/analyze_keystrokes", methods=["POST"])
def analyze_keystrokes():
    data = request.json
    key_events = data.get("keyEvents")
    if key_events is not None:
        processed_keystrokes = KeystrokeProcessor.process_key_events(key_events)
        features = FeatureCalculator().calculate_features(processed_keystrokes)
        return jsonify(
            {"message": "Keystrokes analyzed successfully", "data": features}
        )
    else:
        return jsonify({"error": "No key_events data found"}), 400
