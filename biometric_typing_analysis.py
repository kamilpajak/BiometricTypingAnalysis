import csv
import logging
import time

import numpy as np
from pynput.keyboard import Key, Listener

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class KeystrokeLogger:
    def __init__(self):
        self.csv_file_path = "keystroke_data.csv"
        self.features_file_path = "keystroke_features.csv"
        self.keystrokes = []
        self.event_log = []
        self.initialize_files()

    def initialize_files(self):
        """Initialize CSV files with headers."""
        with open(self.csv_file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Key Code", "Press Time", "Release Time"])
        with open(self.features_file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Feature", "Mean", "Standard Deviation"])

    def on_press(self, key):
        """Log key press events with timestamps."""
        if key not in [Key.ctrl_l, Key.ctrl_r]:  # Skip Ctrl keys
            key_code = key if isinstance(key, Key) else key.char
            self.event_log.append((key_code, 'press', time.time()))

    def on_release(self, key):
        """Log key release events with timestamps."""
        if key not in [Key.ctrl_l, Key.ctrl_r]:  # Skip Ctrl keys
            key_code = key if isinstance(key, Key) else key.char
            self.event_log.append((key_code, 'release', time.time()))
            if key == Key.esc:
                self.process_and_log_keystrokes()
                return False  # Stop the listener

    def filter_event_log(self):
        """Filter out 'enter' and 'esc' events from the event log."""
        return [event for event in self.event_log if event[0] not in [Key.enter, Key.esc]]

    def process_and_log_keystrokes(self):
        """Process the event log and save it to the CSV file, and log filtered events."""
        filtered_event_log = self.filter_event_log()
        with open(self.csv_file_path, "a", newline='') as file:
            writer = csv.writer(file)
            for event in filtered_event_log:
                key_code, action, timestamp = event
                readable_key = key_code if isinstance(key_code, str) else key_code.name
                if action == 'press':
                    self.keystrokes.append({'key_code': readable_key, 'down_time': timestamp})
                elif action == 'release':
                    for keystroke in reversed(self.keystrokes):
                        if keystroke['key_code'] == readable_key and 'up_time' not in keystroke:
                            keystroke['up_time'] = timestamp
                            break
            for keystroke in self.keystrokes:
                if 'up_time' in keystroke:
                    writer.writerow([keystroke['key_code'], keystroke['down_time'], keystroke['up_time']])

        # After logging, calculate and log features
        self.calculate_and_log_features()

    def calculate_and_log_features(self):
        """Calculate features from the keystrokes and log them."""
        if not self.keystrokes:
            return

        # Calculate features
        features = self.calculate_features()

        # Log features to CSV
        with open(self.features_file_path, "a", newline='') as file:
            writer = csv.writer(file)
            for feature, values in features.items():
                writer.writerow([feature, values['Mean'], values['Standard Deviation']])

        # Clear keystrokes for next session
        self.keystrokes.clear()

    def calculate_features(self):
        """Calculate statistical features from the keystrokes."""
        dd_times = [self.keystrokes[i]['down_time'] - self.keystrokes[i - 1]['down_time'] for i in
                    range(1, len(self.keystrokes))]
        ud_times = [self.keystrokes[i]['down_time'] - self.keystrokes[i - 1]['up_time'] for i in
                    range(1, len(self.keystrokes))]
        du_times = [keystroke['up_time'] - keystroke['down_time'] for keystroke in self.keystrokes if
                    'up_time' in keystroke]

        features = {
            'DD Time': {'Mean': np.mean(dd_times) if dd_times else 0,
                        'Standard Deviation': np.std(dd_times, ddof=1) if len(dd_times) > 1 else 0},
            'UD Time': {'Mean': np.mean(ud_times) if ud_times else 0,
                        'Standard Deviation': np.std(ud_times, ddof=1) if len(ud_times) > 1 else 0},
            'DU Time': {'Mean': np.mean(du_times) if du_times else 0,
                        'Standard Deviation': np.std(du_times, ddof=1) if len(du_times) > 1 else 0},
        }

        return features

    def start_listener(self):
        """Start the keystroke listener."""
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def enrollment_phase(self):
        """Handle the enrollment phase."""
        print("Welcome to the Keystroke Dynamics Enrollment")
        target_string = "Please type the following string and press ESC to complete enrollment: Uniwersytet Slaski"
        print(target_string)
        self.event_log.clear()  # Clear any previous events
        self.start_listener()

    def main_menu(self):
        """Display the main menu and handle user choices."""
        while True:
            print("\nKeystroke Dynamics System")
            print("1. Enrollment")
            print("2. Authentication")
            print("3. Exit")
            choice = input("Choose an option (1/2/3): ")
            if choice == '1':
                self.enrollment_phase()
            elif choice == '2':
                # Authentication phase can be implemented here
                pass
            elif choice == '3':
                print("Exiting the system.")
                break
            else:
                print("Invalid option, please choose 1, 2, or 3.")


if __name__ == "__main__":
    keystroke_logger = KeystrokeLogger()
    keystroke_logger.main_menu()
