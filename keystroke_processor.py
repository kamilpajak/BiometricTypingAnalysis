class KeystrokeProcessor:
    def __init__(self):
        self.keystrokes = []

    def process_key_events(self, raw_keystrokes):
        """Process raw keystrokes which are a list of dicts with key, type, and time."""
        self.keystrokes.clear()
        press_times = {}
        for raw_keystroke in raw_keystrokes:
            key = raw_keystroke['key'].lower()
            action = raw_keystroke['type']
            timestamp = raw_keystroke['time']

            if action == 'press' and key not in press_times:
                press_times[key] = timestamp

            elif action == 'release' and key in press_times:
                self.keystrokes.append((key, press_times[key], timestamp))
                del press_times[key]

        # Sort keystrokes by the down_time to ensure they are in the order they were pressed
        self.keystrokes.sort(key=lambda x: x[1])

    def get_keystrokes(self):
        """Return the processed keystrokes."""
        return self.keystrokes
