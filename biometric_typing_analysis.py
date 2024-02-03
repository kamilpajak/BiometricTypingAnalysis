import csv
import logging
import time

import numpy as np
from pynput.keyboard import Key, Listener

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    """Log the keystrokes to a CSV file, excluding the last entry for the ESC key."""
    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file)
        # Exclude the last keystroke if it's the ESC key
        keystrokes_to_log = keystrokes[:-1] if keystrokes[-1]['key_code'] == Key.esc else keystrokes
        for keystroke in keystrokes_to_log:
            # Ensure we log only if the key has been released to have both press and release times
            if 'up_time' in keystroke:
                writer.writerow([
                    keystroke['key_code'],
                    keystroke['down_time'],
                    keystroke['up_time']
                ])


event_log = []  # List to store key events and their timestamps


def on_press(key):
    """Log key press events with timestamps."""
    key_code = key if isinstance(key, Key) else key.char
    if key not in [Key.ctrl_l, Key.ctrl_r]:  # Skip Ctrl keys
        event_log.append((key_code, 'press', time.time() * 1000))


def on_release(key):
    """Log key release events with timestamps."""
    if key not in [Key.ctrl_l, Key.ctrl_r]:  # Skip Ctrl keys
        key_code = key if isinstance(key, Key) else key.char
        event_log.append((key_code, 'release', time.time() * 1000))
        if key == Key.esc:
            process_and_log_keystrokes()
            return False  # Stop the listener


def process_and_log_keystrokes():
    """Process the event log and save it to a CSV file, excluding the first and last events."""
    with open(csv_file_path, "w", newline='') as file:  # Use "w" to overwrite existing or create new file
        writer = csv.writer(file)
        writer.writerow(["Key Code", "Press Time", "Release Time"])  # Write headers

        # Remove 'enter' and 'esc' events from the start
        while event_log and (event_log[0][0] == 'enter' or event_log[0][0] == 'esc'):
            event_log.pop(0)

        # Remove 'enter' and 'esc' events from the end
        while event_log and (event_log[-1][0] == 'enter' or event_log[-1][0] == 'esc'):
            event_log.pop()

        # Now event_log is filtered
        logging.debug("Filtered Event Log:")
        for key, action, timestamp in event_log:
            readable_key = key if isinstance(key, str) else key.name  # Convert key object to string if necessary
            logging.debug(f"{readable_key}, {action}, {timestamp}")

        # Initialize a dictionary to hold the press and release times
        keystroke_times = {}
        for event in event_log:
            key_code, action, timestamp = event
            if key_code not in keystroke_times:
                keystroke_times[key_code] = {'down_time': None, 'up_time': None}
            if action == 'press' and keystroke_times[key_code]['down_time'] is None:  # Only log the first press time
                keystroke_times[key_code]['down_time'] = timestamp
            elif action == 'release':
                # Always update the release time to the last release action
                keystroke_times[key_code]['up_time'] = timestamp

        # Write the processed keystrokes to the CSV
        for key_code, times in keystroke_times.items():
            if times['down_time'] and times['up_time']:  # Ensure both press and release times are present
                writer.writerow([key_code, times['down_time'], times['up_time']])


def start_listener():
    """Start the keystroke listener."""
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()  # Start the listener in a non-blocking fashion
    listener.join()  # Wait for the listener to complete


def enrollment_phase():
    print("Welcome to the Keystroke Dynamics Enrollment")
    target_string = "Uniwersytet Slaski"
    print(f"Please type the following string and press ESC to complete enrollment: {target_string}")
    keystrokes.clear()  # Clear any previous keystrokes
    start_listener()  # Start capturing keystrokes

    # Calculate and log features after keystrokes have been captured
    features = calculate_features(keystrokes)
    log_features(features)

    print("Enrollment complete. Features have been calculated and saved.")


def main_menu():
    while True:
        print("\nKeystroke Dynamics System")
        print("1. Enrollment")
        print("2. Authentication")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            enrollment_phase()
        elif choice == '2':
            continue
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid option, please choose 1, 2, or 3.")


# Remove the existing listener logic and replace with a call to main_menu
if __name__ == "__main__":
    main_menu()
