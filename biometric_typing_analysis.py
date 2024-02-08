import logging

from tabulate import tabulate

from feature_calculator import FeatureCalculator
from keystroke_processor import KeyboardEventHandler


class BiometricTypingAnalysis:
    def __init__(self):
        self.keystrokes = None
        self.keyboard_event_handler = KeyboardEventHandler()

    def retrieve_keystrokes(self):
        self.keystrokes = self.keyboard_event_handler.get_keystrokes()
        table_data = [[key_code, press_time, release_time] for key_code, press_time, release_time in self.keystrokes]
        table = tabulate(table_data, headers=["Key Code", "Press Time", "Release Time"], tablefmt="grid",
                         floatfmt=".3f")
        logging.info(f"\n{table}")

    def calculate_features(self):
        if not self.keystrokes:
            logging.info("No keystrokes to process for features.")
            return
        features = FeatureCalculator.calculate_features(self.keystrokes)
        logging.info("Features:")
        logging.info(features)

    def enrollment_phase(self):
        print("Welcome to the Biometric Typing Analysis Enrollment")
        target_string = "Uniwersytet Slaski"
        print(f"Please type the following string and press ESC to complete enrollment: {target_string}")
        self.keyboard_event_handler.clear_keyboard_events()
        self.keyboard_event_handler.start_listener()

        self.retrieve_keystrokes()
        self.calculate_features()

    def main_menu(self):
        print("\nBiometric Typing Analysis System")
        print("1. Enrollment")
        print("2. Authentication")
        print("3. Exit")
        while True:
            choice = input("Choose an option (1/2/3): ")
            if choice == '1':
                self.enrollment_phase()
            elif choice == '2':
                pass  # Authentication phase can be implemented here
            elif choice == '3':
                print("Exiting the system.")
                break
            else:
                print("Invalid option, please choose 1, 2, or 3.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    analysis = BiometricTypingAnalysis()
    analysis.main_menu()
