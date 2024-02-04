from csv_handler import CSVHandler
from event_log_handler import EventLogHandler


class BiometricTypingAnalysis:
    def __init__(self):
        self.event_log_handler = EventLogHandler()
        self.csv_handler = CSVHandler("keystroke_data.csv", "keystroke_features.csv")

    def process_and_log_keystrokes(self):
        """Process the event log and save it to the CSV file."""
        keystrokes = self.event_log_handler.get_keystrokes()
        self.csv_handler.log_keystrokes(keystrokes)

    def enrollment_phase(self):
        """Handle the enrollment phase."""
        print("Welcome to the Biometric Typing Analysis Enrollment")
        target_string = "Uniwersytet Slaski"
        print(f"Please type the following string and press ESC to complete enrollment: {target_string}")
        self.event_log_handler.clear_event_log()  # Clear any previous events within the handler
        self.event_log_handler.start_listener()  # Start and run the listener within the handler
        self.process_and_log_keystrokes()

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
    analysis = BiometricTypingAnalysis()
    analysis.main_menu()
