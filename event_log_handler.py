import logging
import time

from pynput.keyboard import Key, Listener


class EventLogHandler:
    def __init__(self):
        self.event_log = []
        self.listener_running = True
        self.listener = None

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
                self.listener_running = False
                return False  # Returning False stops the listener

    def start_listener(self):
        """Start the keystroke listener."""
        # Assign the Listener object to self.listener
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        with self.listener:
            self.listener.join()  # This will block until the listener stops (ESC is pressed)

    def clear_event_log(self):
        """Clear the event log."""
        self.event_log.clear()

    def filter_event_log(self):
        """Filter out 'enter' and 'esc' events from the start and end of the event log."""
        start_index = 0
        end_index = len(self.event_log) - 1

        # Skip 'enter' and 'esc' events at the start of the event log
        while start_index <= end_index and self.event_log[start_index][0] in [Key.enter, Key.esc]:
            start_index += 1

        # Skip 'enter' and 'esc' events at the end of the event log
        while end_index >= start_index and self.event_log[end_index][0] in [Key.enter, Key.esc]:
            end_index -= 1

        # Extract the filtered event log
        filtered_event_log = self.event_log[start_index:end_index + 1]

        # Detailed logging of the filtered event log
        logging.info("Filtered Event Log:")
        for event in filtered_event_log:
            key, action, timestamp = event
            if isinstance(key, Key):
                key = key.name  # Use the name of special keys, like 'shift'
            logging.info(f"Event: Key: {key}, Action: {action}, Timestamp: {timestamp}")

        return filtered_event_log

    def get_keystrokes(self):
        """Pair up press and release times for each key to create keystrokes from filtered events."""
        filtered_event_log = self.filter_event_log()  # Obtain filtered events
        press_times = {}
        keystrokes = []

        for event in filtered_event_log:
            key, action, timestamp = event
            # Check if the key is a special key
            is_special_key = isinstance(key, Key)

            # Use the original key object for special keys, lowercase string for regular keys
            key_identifier = key if is_special_key else key.lower()

            if action == 'press':
                if key_identifier not in press_times:
                    press_times[key_identifier] = timestamp
            elif action == 'release' and key_identifier in press_times:
                down_time = press_times[key_identifier]
                up_time = timestamp
                # Use the original key for special keys in the output, lowercase for regular keys
                keystrokes_output = key if is_special_key else key_identifier
                keystrokes.append((keystrokes_output, down_time, up_time))
                del press_times[key_identifier]  # Remove the entry after using it

        # Sort the keystrokes by the down_time to ensure they are in the order they were pressed
        keystrokes.sort(key=lambda k: k[1])
        return keystrokes
