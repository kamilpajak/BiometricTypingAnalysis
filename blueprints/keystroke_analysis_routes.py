# keystroke_analysis_routes.py

import numpy as np
from flask import Blueprint, session, jsonify, request
from sqlalchemy import desc

from database import db
from models import KeystrokeTimingFeatures, Template

keystroke_analysis_bp = Blueprint(
    "keystroke_analysis", __name__, template_folder="templates"
)


def calculate_statistics(values):
    """Calculate mean and standard deviation."""
    mean_val = np.mean(values)
    std_dev_val = np.std(values, ddof=1)  # ddof=1 for standard deviation
    return mean_val, std_dev_val


@keystroke_analysis_bp.route("/calculate_template", methods=["POST"])
def calculate_template():
    """Calculate the template based on a specific key sequence."""
    if "user_id" not in session:
        return jsonify({"error": "User is not logged in"}), 400

    # Expecting JSON data with 'sequence'
    data = request.get_json()
    sequence = data.get("sequence")

    if not sequence:
        return jsonify({"error": "Key sequence not provided"}), 400

    user_id = session["user_id"]

    try:
        # Retrieve all records for the given user
        records = (
            KeystrokeTimingFeatures.query.filter_by(user_id=user_id)
            .order_by(desc(KeystrokeTimingFeatures.created_at))
            .all()
        )

        # Filter records to match the provided sequence
        filtered_records = []
        for record in records:
            if "keystrokes" in record.features:
                keys = [ks["key"] for ks in record.features["keystrokes"]]
                # Check if the beginning of the keys list matches the provided sequence
                if keys[: len(sequence)] == sequence:
                    filtered_records.append(record)

        # Now, select the 10 most recent matching records
        matching_records = filtered_records[:10]

        # Initialize lists to store timing intervals for each feature
        press_to_press_intervals = []
        release_to_press_intervals = []
        press_to_release_intervals = []

        # Extract the timing intervals from the matching records
        for record in matching_records:
            press_to_press_intervals.extend(record.features["press_to_press"])
            release_to_press_intervals.extend(record.features["release_to_press"])
            press_to_release_intervals.extend(record.features["press_to_release"])

        # Calculate the statistics for each feature
        mean_press_to_press, std_dev_press_to_press = calculate_statistics(
            press_to_press_intervals
        )
        mean_release_to_press, std_dev_release_to_press = calculate_statistics(
            release_to_press_intervals
        )
        mean_press_to_release, std_dev_press_to_release = calculate_statistics(
            press_to_release_intervals
        )

        # Create and save the Template object with calculated statistics
        new_template = Template(
            key=sequence[0],  # Assuming the sequence starts with the key of interest
            mean_press_press=mean_press_to_press,
            std_dev_press_press=std_dev_press_to_press,
            mean_release_press=mean_release_to_press,
            std_dev_release_press=std_dev_release_to_press,
            mean_press_release=mean_press_to_release,
            std_dev_press_release=std_dev_press_to_release,
            user_id=user_id,
        )
        db.session.add(new_template)
        db.session.commit()

        return jsonify(
            {"message": "Template statistics calculated and saved successfully"}
        )
    except Exception as e:
        print(f"Error calculating template: {str(e)}")
        return (
            jsonify({"error": "An error occurred while processing your request"}),
            500,
        )
