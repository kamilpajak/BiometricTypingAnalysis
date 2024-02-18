# keystroke.py
class Keystroke:
    def __init__(self, key, press_time, release_time):
        """
        Initializes a new instance of the Keystroke class.

        :param key: The key that was pressed.
        :param press_time: The timestamp when the key was pressed.
        :param release_time: The timestamp when the key was released.
        """
        self.key = key.lower()
        self.press_time = press_time
        self.release_time = release_time

    def __repr__(self):
        """
        Provides a string representation of the Keystroke instance,
        which is helpful for debugging and logging.
        """
        return f"Keystroke(key='{self.key}', press_time={self.press_time}, release_time={self.release_time})"
