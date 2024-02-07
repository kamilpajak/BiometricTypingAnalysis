import time

from pynput.keyboard import Key, Listener


class KeyboardEventHandler:
    def __init__(self):
        self.keyboard_events = []
        self.listener_running = True
        self.listener = None

    def on_press(self, key):
        if key not in [Key.ctrl_l, Key.ctrl_r]:  # Skip Ctrl keys
            key_code = key if isinstance(key, Key) else key.char
            self.keyboard_events.append((key_code, 'press', time.time()))

    def on_release(self, key):
        if key not in [Key.ctrl_l, Key.ctrl_r]:  # Skip Ctrl keys
            key_code = key if isinstance(key, Key) else key.char
            self.keyboard_events.append((key_code, 'release', time.time()))
            if key == Key.esc:
                self.listener_running = False
                return False  # Stop listener

    def start_listener(self):
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        with self.listener:
            self.listener.join()

    def clear_keyboard_events(self):
        self.keyboard_events.clear()

    def filter_keyboard_events(self):
        start_index, end_index = 0, len(self.keyboard_events) - 1
        while start_index <= end_index and self.keyboard_events[start_index][0] in [Key.enter, Key.esc]:
            start_index += 1
        while end_index >= start_index and self.keyboard_events[end_index][0] in [Key.enter, Key.esc]:
            end_index -= 1
        filtered_keyboard_events = self.keyboard_events[start_index:end_index + 1]

        return filtered_keyboard_events

    def get_keystrokes(self):
        filtered_keyboard_events = self.filter_keyboard_events()
        press_times, keystrokes = {}, []
        for key, action, timestamp in filtered_keyboard_events:
            key = key if isinstance(key, Key) else key.lower()
            if action == 'press' and key not in press_times:
                press_times[key] = timestamp
            elif action == 'release' and key in press_times:
                keystrokes.append((key, press_times[key], timestamp))
                del press_times[key]
        keystrokes.sort(key=lambda k: k[1])
        return keystrokes
