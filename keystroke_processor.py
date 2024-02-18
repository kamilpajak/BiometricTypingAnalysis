# keystroke_processor.py
from models.keystroke import Keystroke


class KeystrokeProcessor:
    @staticmethod
    def process_key_events(key_events):
        """
        Processes a list of key events, converting them into a sorted list of Keystroke instances.

        :param key_events: A list of key event dictionaries, each containing 'key', 'type', and 'time'.
        :return: A sorted list of Keystroke instances.
        """
        keystrokes = []
        press_times = {}
        for raw_keystroke in key_events:
            key = raw_keystroke["key"].lower()
            action = raw_keystroke["type"]
            timestamp = raw_keystroke["time"]

            if action == "press" and key not in press_times:
                press_times[key] = timestamp
            elif action == "release" and key in press_times:
                keystrokes.append(Keystroke(key, press_times[key], timestamp))
                del press_times[key]

        keystrokes.sort(key=lambda x: x.press_time)
        return keystrokes
