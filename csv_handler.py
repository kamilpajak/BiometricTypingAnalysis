import csv


class CSVHandler:
    def __init__(self, keystroke_data_path, feature_data_path):
        self.keystroke_data_path = keystroke_data_path
        self.feature_data_path = feature_data_path
        self.initialize_files()

    def initialize_files(self):
        """Initialize CSV files with headers."""
        with open(self.keystroke_data_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Key Code", "Press Time", "Release Time"])
        with open(self.feature_data_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Feature", "Mean", "Standard Deviation"])

    def log_keystrokes(self, keystrokes):
        """Log the keystrokes to a CSV file."""
        with open(self.keystroke_data_path, "a", newline='') as file:
            writer = csv.writer(file)
            for keystroke in keystrokes:
                if 'up_time' in keystroke:
                    writer.writerow([keystroke['key_code'], keystroke['down_time'], keystroke['up_time']])

    def log_features(self, features):
        """Log the features to a CSV file."""
        with open(self.feature_data_path, "a", newline='') as file:
            writer = csv.writer(file)
            for feature, values in features.items():
                writer.writerow([feature, values['Mean'], values['Standard Deviation']])
