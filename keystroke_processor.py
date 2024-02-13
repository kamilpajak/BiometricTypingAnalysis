# keystroke_processor.py
class KeystrokeProcessor:
    def __init__(self):
        self.keystrokes = []

    def process_key_events(self, key_events):
        self.keystrokes.clear()
        press_times = {}
        for raw_keystroke in key_events:
            key = raw_keystroke["key"].lower()
            action = raw_keystroke["type"]
            timestamp = raw_keystroke["time"]

            if action == "press" and key not in press_times:
                press_times[key] = timestamp
            elif action == "release" and key in press_times:
                self.keystrokes.append((key, press_times[key], timestamp))
                del press_times[key]

        self.keystrokes.sort(key=lambda x: x[1])
        return self.keystrokes
