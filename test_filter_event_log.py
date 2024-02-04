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
