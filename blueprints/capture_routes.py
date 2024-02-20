from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    jsonify,
    request,
)

from database import db
from keystroke_processor import KeystrokeProcessor
from models import KeystrokeTimingFeatures

capture_bp = Blueprint("capture", __name__, template_folder="templates")


@capture_bp.route("/", endpoint="index")
def index():
    if "user_id" in session:
        return render_template("capture.html")
    return redirect(url_for("auth.login"))


@capture_bp.route("/process_keystrokes", methods=["POST"])
def process_keystrokes_and_save_features():
    """
    Processes the incoming key events, calculates the keystroke dynamics features,
    and associates them with the logged-in user.
    """
    data = request.json
    key_events = data.get("keyEvents")

    if key_events and "user_id" in session:
        user_id = session["user_id"]

        # Convert raw key events into instances suitable for feature calculation
        processed_keystrokes = KeystrokeProcessor.process_key_events(key_events)

        # Calculate features and create a new record
        keystroke_features = KeystrokeTimingFeatures(
            keystrokes=processed_keystrokes, user_id=user_id
        )
        db.session.add(keystroke_features)
        db.session.commit()

        return jsonify(
            {
                "message": "Keystroke dynamics features processed and saved successfully",
                "features": keystroke_features.features,
            }
        )
    else:
        return (
            jsonify({"error": "No keystroke events provided or user is not logged in"}),
            400,
        )
