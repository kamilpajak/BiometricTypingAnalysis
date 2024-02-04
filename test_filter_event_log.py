import pytest
from pynput.keyboard import Key

from biometric_typing_analysis import KeystrokeLogger


@pytest.mark.parametrize("event_log,expected_filtered_event_log", [
    ([
         (Key.enter, 'release', 0),
         ('t', 'press', 1),
         ('t', 'release', 2),
         ('e', 'press', 3),
         ('e', 'release', 4),
         ('s', 'press', 5),
         ('s', 'release', 6),
         ('t', 'press', 7),
         ('t', 'release', 8),
         (Key.esc, 'press', 9),
         (Key.esc, 'release', 10)
     ], [
         ('t', 'press', 1),
         ('t', 'release', 2),
         ('e', 'press', 3),
         ('e', 'release', 4),
         ('s', 'press', 5),
         ('s', 'release', 6),
         ('t', 'press', 7),
         ('t', 'release', 8),
     ])
])
def test_filter_event_log(event_log, expected_filtered_event_log):
    keystroke_logger = KeystrokeLogger()
    keystroke_logger.event_log = event_log

    filtered_event_log = keystroke_logger.filter_event_log()
    assert filtered_event_log == expected_filtered_event_log
