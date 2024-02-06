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
            writer.writerow(['Key', 'DD Times', 'UD Times', 'DU Times'])

    def log_keystrokes(self, keystrokes):
        """Log the keystrokes to a CSV file."""
        with open(self.keystroke_data_path, "a", newline='') as file:
            writer = csv.writer(file)
            for key, down_time, up_time in keystrokes:
                writer.writerow([key, down_time, up_time])

    def log_features(self, features):
        """Log the features to a CSV file."""
        with open(self.feature_data_path, "a", newline='') as file:
            writer = csv.writer(file)

            # Assuming features is a dictionary like:
            # {
            #     'keys': ['key1', 'key2', ...],
            #     'DD': [dd1, dd2, ...],
            #     'UD': [ud1, ud2, ...],
            #     'DU': [du1, du2, ...],
            # }

            # Get the number of features (all lists should have the same length)
            num_features = len(features['keys'])

            # Write each feature set to the CSV file
            for i in range(num_features):
                key = features['keys'][i]
                dd = features['DD'][i] if i < len(features['DD']) else ''
                ud = features['UD'][i] if i < len(features['UD']) else ''
                du = features['DU'][i] if i < len(features['DU']) else ''
                writer.writerow([key, dd, ud, du])
