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

        # Return the filtered event log that excludes 'enter' and 'esc' from the start and end
        return self.event_log[start_index:end_index + 1]

    def get_keystrokes(self):
        """Pair up press and release times for each key to create keystrokes from filtered events."""
        filtered_event_log = self.filter_event_log()  # Obtain filtered events
        press_times = {}
        keystrokes = []

        for key, action, timestamp in filtered_event_log:
            if action == 'press':
                press_times[key] = timestamp
            elif action == 'release' and key in press_times:
                down_time = press_times[key]
                up_time = timestamp
                keystrokes.append((key, down_time, up_time))
                del press_times[key]  # Remove the entry after using it

        return keystrokes
