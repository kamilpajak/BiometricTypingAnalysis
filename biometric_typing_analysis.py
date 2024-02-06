import logging

from csv_handler import CSVHandler
from event_log_handler import EventLogHandler
from feature_calculator import FeatureCalculator


class BiometricTypingAnalysis:
    def __init__(self):
        # Initialize the event log handler for capturing keyboard events.
        self.event_log_handler = EventLogHandler()
        # Initialize the CSV handler for logging data to CSV files.
        self.csv_handler = CSVHandler("keystroke_data.csv", "keystroke_features.csv")
        # Initialize a place to store keystrokes after they are first retrieved.
        self.keystrokes = []

    def process_and_log_keystrokes(self):
        """
        Retrieve keystrokes from the event log, process them,
        and log the detailed keystroke information to a CSV file.
        """
        # Extract keystrokes (key press and release events) from the event log.
        self.keystrokes = self.event_log_handler.get_keystrokes()
        # Log the processed keystrokes to the designated CSV file.
        self.csv_handler.log_keystrokes(self.keystrokes)

    def process_and_log_features(self):
        """
        Calculate features from existing keystrokes and
        log the calculated features to a CSV file.
        """
        if not self.keystrokes:
            logging.info("No keystrokes to process for features.")
            return

        # Calculate features based on the already extracted keystrokes.
        features = FeatureCalculator.calculate_features(self.keystrokes)
        # Log the calculated features to the designated CSV file.
        self.csv_handler.log_features(features)

    def run_analysis(self):
        """
        A method to encapsulate the full analysis process.
        """
        print("Starting keystroke analysis...")
        self.process_and_log_keystrokes()
        self.process_and_log_features()
        print("Analysis complete.")

    def enrollment_phase(self):
        """Handle the enrollment phase."""
        print("Welcome to the Biometric Typing Analysis Enrollment")
        target_string = "Uniwersytet Slaski"
        print(f"Please type the following string and press ESC to complete enrollment: {target_string}")
        self.event_log_handler.clear_event_log()  # Clear any previous events within the handler
        self.event_log_handler.start_listener()  # Start and run the listener within the handler
        self.process_and_log_keystrokes()
        self.process_and_log_features()

    def main_menu(self):
        """Display the main menu and handle user choices."""
        while True:
            print("\nBiometric Typing Analysis System")
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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    analysis = BiometricTypingAnalysis()
    analysis.main_menu()
