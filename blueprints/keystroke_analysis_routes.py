# keystroke_analysis_routes.py

from collections import defaultdict

from flask import Blueprint, session, jsonify

from models import KeystrokeTimingFeatures

keystroke_analysis_bp = Blueprint(
    "keystroke_analysis", __name__, template_folder="templates"
)


def group_records_by_key_sequence(records):
    """
    Groups records by their sequences of keys. Records with identical sequences of keys
    are grouped together, regardless of the timing values.

    :param records: A list of KeystrokeTimingFeatures instances.
    :return: A dictionary where each key is a tuple representing a unique sequence of keys,
             and the value is a list of record IDs that share this sequence.
    """
    sequence_groups = defaultdict(list)
    for record in records:
        # Extract the sequence of keys from the record
        key_sequence = tuple(ks["key"] for ks in record.features["keystrokes"])
        sequence_groups[key_sequence].append(record.id)
    return sequence_groups


@keystroke_analysis_bp.route("/grouped_keystrokes", methods=["GET"])
def get_grouped_keystrokes():
    """
    Retrieves keystroke records from the database, groups them by the sequence of keys,
    and returns the grouped sequences for the logged-in user.
    """
    if "user_id" not in session:
        return jsonify({"error": "User is not logged in"}), 400

    user_id = session["user_id"]
    try:
        records = KeystrokeTimingFeatures.query.filter_by(user_id=user_id).all()
        grouped_by_sequence = group_records_by_key_sequence(records)

        # Prepare the response data
        grouped_sequences = [
            {"sequence": list(sequence), "record_ids": ids}
            for sequence, ids in grouped_by_sequence.items()
        ]

        return jsonify(
            {
                "message": "Successfully retrieved and grouped keystroke sequences",
                "grouped_sequences": grouped_sequences,
            }
        )
    except Exception as e:
        # Assuming your Flask app is configured for logging
        print(
            f"Error retrieving grouped keystrokes: {str(e)}"
        )  # Consider using logging instead of print in production
        return (
            jsonify({"error": "An error occurred while processing your request"}),
            500,
        )
