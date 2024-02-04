import pytest
from pynput.keyboard import Key

from event_log_handler import EventLogHandler


@pytest.mark.parametrize("event_log,expected_filtered_event_log", [
    ([
         # Filtering out 'enter' and 'esc' events at the beginning and end
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
         # Expected log after filtering
         ('t', 'press', 1),
         ('t', 'release', 2),
         ('e', 'press', 3),
         ('e', 'release', 4),
         ('s', 'press', 5),
         ('s', 'release', 6),
         ('t', 'press', 7),
         ('t', 'release', 8),
     ]),
    ([
         # Additional 'enter' events in the middle should remain
         (Key.enter, 'press', 0),  # 'enter' at the start to be filtered out
         (Key.enter, 'release', 1),
         ('t', 'press', 2),
         ('t', 'release', 3),
         (Key.enter, 'press', 4),  # 'enter' in the middle to remain
         (Key.enter, 'release', 5),
         ('e', 'press', 6),
         ('e', 'release', 7),
         (Key.enter, 'press', 8),  # Another 'enter' in the middle to remain
         (Key.enter, 'release', 9),
         ('s', 'press', 10),
         ('s', 'release', 11),
         ('t', 'press', 12),
         ('t', 'release', 13),
         (Key.esc, 'press', 14),  # 'esc' at the end to be filtered out
         (Key.esc, 'release', 15)
     ], [
         # Expected log after filtering with middle 'enter' events remaining
         ('t', 'press', 2),
         ('t', 'release', 3),
         (Key.enter, 'press', 4),  # Middle 'enter' remains
         (Key.enter, 'release', 5),
         ('e', 'press', 6),
         ('e', 'release', 7),
         (Key.enter, 'press', 8),  # Another middle 'enter' remains
         (Key.enter, 'release', 9),
         ('s', 'press', 10),
         ('s', 'release', 11),
         ('t', 'press', 12),
         ('t', 'release', 13),
     ])
])
def test_filter_event_log(event_log, expected_filtered_event_log):
    event_log_handler = EventLogHandler()
    event_log_handler.event_log = event_log

    filtered_event_log = event_log_handler.filter_event_log()
    assert filtered_event_log == expected_filtered_event_log


@pytest.mark.parametrize("filtered_event_log, expected_keystrokes", [
    # Test case 1: Simple sequence where each key is pressed and then released.
    ([
         ('a', 'press', 0),
         ('a', 'release', 1),
         ('b', 'press', 2),
         ('b', 'release', 3)
     ], [
         ('a', 0, 1),
         ('b', 2, 3)
     ]),
    # Test case 2: Sequence with overlapping presses, demonstrating concurrent key actions.
    ([
         ('a', 'press', 0),
         ('b', 'press', 1),
         ('a', 'release', 2),
         ('b', 'release', 3)
     ], [
         ('a', 0, 2),
         ('b', 1, 3)
     ]),
    # Test case 3: A single key pressed multiple times before being released, showcasing the handling of key holding.
    ([
         ('a', 'press', 0),
         ('a', 'press', 1),
         ('a', 'press', 2),
         ('a', 'release', 3)
     ], [
         ('a', 0, 3)
     ]),
    # Test case 4: A modifier key (shift) is held down while another key ('U') is pressed and released.
    ([
         (Key.shift, 'press', 0),
         ('U', 'press', 1),
         ('U', 'release', 2),
         (Key.shift, 'release', 3)
     ], [
         ('U', 1, 2),
         (Key.shift, 0, 3)
     ]),
    # Test case 5: Similar to test case 4 but the release order is reversed.
    ([
         (Key.shift, 'press', 0),
         ('U', 'press', 1),
         (Key.shift, 'release', 2),
         ('U', 'release', 3)
     ], [
         (Key.shift, 0, 2),
         ('U', 1, 3)
     ])
])
def test_get_keystrokes(filtered_event_log, expected_keystrokes):
    event_log_handler = EventLogHandler()
    event_log_handler.event_log = filtered_event_log  # Directly set the filtered event log
    keystrokes = event_log_handler.get_keystrokes()
    assert keystrokes == expected_keystrokes
