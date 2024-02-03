import csv
import time

import numpy as np
from pynput.keyboard import Key, Listener

# File initialization for keystroke data and features
csv_file_path = "keystroke_data.csv"
features_file_path = "keystroke_features.csv"

# Initialize the CSV files with headers
with open(csv_file_path, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Key Code", "Press Time", "Release Time"])

with open(features_file_path, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Feature", "Mean", "Standard Deviation"])

# Global list to track keystroke events and times
keystrokes = []


def calculate_features(keystrokes):
    """Calculate features from the keystrokes."""
    # Extract intervals
    dd_times = [keystrokes[i]['down_time'] - keystrokes[i - 1]['down_time'] for i in range(1, len(keystrokes))]
    ud_times = [keystrokes[i]['down_time'] - keystrokes[i - 1]['up_time'] for i in range(1, len(keystrokes))]
    du_times = [keystroke['up_time'] - keystroke['down_time'] for keystroke in keystrokes if 'up_time' in keystroke]

    # Calculate mean and standard deviation for each interval type
    features = {
        'Key-down Key-down Time': {
            'Mean': np.mean(dd_times) if dd_times else 0,
            'Standard Deviation': np.std(dd_times, ddof=1) if len(dd_times) > 1 else 0
        },
        'Key-up Key-down Time': {
            'Mean': np.mean(ud_times) if ud_times else 0,
            'Standard Deviation': np.std(ud_times, ddof=1) if len(ud_times) > 1 else 0
        },
        'Key-down Key-up Time': {
            'Mean': np.mean(du_times) if du_times else 0,
            'Standard Deviation': np.std(du_times, ddof=1) if len(du_times) > 1 else 0
        }
    }
    return features


def log_features(features):
    """Log the features to a CSV file."""
    with open(features_file_path, "a", newline='') as file:
        writer = csv.writer(file)
        for feature, stats in features.items():
            writer.writerow([feature, stats['Mean'], stats['Standard Deviation']])


def log_keystrokes():
    """Log the keystrokes to a CSV file."""
    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file)
        for keystroke in keystrokes:
            # Ensure we log only if the key has been released to have both press and release times
            if 'up_time' in keystroke:
                writer.writerow([
                    keystroke['key_code'],
                    keystroke['down_time'],
                    keystroke['up_time']
                ])


def on_press(key):
    """Callback for key press events."""
    key_code = key if isinstance(key, Key) else key.char
    key_down_time = time.time() * 1000  # Get current time in milliseconds
    keystrokes.append({'key_code': key_code, 'down_time': key_down_time})


def on_release(key):
    """Callback for key release events."""
    key_code = key if isinstance(key, Key) else key.char
    key_up_time = time.time() * 1000  # Get current time in milliseconds
    # Update the corresponding key press event with the release time
    for keystroke in keystrokes:
        if keystroke['key_code'] == key_code:
            keystroke['up_time'] = key_up_time
            break
    if key == Key.esc:
        # Log the keystrokes when ESC is pressed and stop the listener
        log_keystrokes()
        return False


# Start the listener to monitor keyboard
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
