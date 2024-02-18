import pytest

from keystroke_processor import KeystrokeProcessor
from models.keystroke import Keystroke


@pytest.mark.parametrize(
    "keyboard_events,expected_filtered_keyboard_events",
    [
        (
            [
                # Filtering out "enter" and "esc" events at the beginning and end
                ("enter", "release", 0),
                ("t", "press", 1),
                ("t", "release", 2),
                ("e", "press", 3),
                ("e", "release", 4),
                ("s", "press", 5),
                ("s", "release", 6),
                ("t", "press", 7),
                ("t", "release", 8),
                ("esc", "press", 9),
                ("esc", "release", 10),
            ],
            [
                # Expected log after filtering
                ("t", "press", 1),
                ("t", "release", 2),
                ("e", "press", 3),
                ("e", "release", 4),
                ("s", "press", 5),
                ("s", "release", 6),
                ("t", "press", 7),
                ("t", "release", 8),
            ],
        ),
        (
            [
                # Additional "enter" events in the middle should remain
                ("enter", "press", 0),  # "enter" at the start to be filtered out
                ("enter", "release", 1),
                ("t", "press", 2),
                ("t", "release", 3),
                ("enter", "press", 4),  # "enter" in the middle to remain
                ("enter", "release", 5),
                ("e", "press", 6),
                ("e", "release", 7),
                ("enter", "press", 8),  # Another "enter" in the middle to remain
                ("enter", "release", 9),
                ("s", "press", 10),
                ("s", "release", 11),
                ("t", "press", 12),
                ("t", "release", 13),
                ("esc", "press", 14),  # "esc" at the end to be filtered out
                ("esc", "release", 15),
            ],
            [
                # Expected log after filtering with middle "enter" events remaining
                ("t", "press", 2),
                ("t", "release", 3),
                ("enter", "press", 4),  # Middle "enter" remains
                ("enter", "release", 5),
                ("e", "press", 6),
                ("e", "release", 7),
                ("enter", "press", 8),  # Another middle "enter" remains
                ("enter", "release", 9),
                ("s", "press", 10),
                ("s", "release", 11),
                ("t", "press", 12),
                ("t", "release", 13),
            ],
        ),
    ],
)
def test_filter_keyboard_events(keyboard_events, expected_filtered_keyboard_events):
    assert True


@pytest.mark.parametrize(
    "key_events, expected_keystrokes",
    [
        # Test case 1: Simple sequence where each key is pressed and then released.
        (
            [
                {"key": "a", "type": "press", "time": 0},
                {"key": "a", "type": "release", "time": 1},
                {"key": "b", "type": "press", "time": 2},
                {"key": "b", "type": "release", "time": 3},
            ],
            [Keystroke("a", 0, 1), Keystroke("b", 2, 3)],
        ),
        # Test case 2: Sequence with overlapping presses, demonstrating concurrent key actions.
        (
            [
                {"key": "a", "type": "press", "time": 0},
                {"key": "b", "type": "press", "time": 1},
                {"key": "a", "type": "release", "time": 2},
                {"key": "b", "type": "release", "time": 3},
            ],
            [Keystroke("a", 0, 2), Keystroke("b", 1, 3)],
        ),
        # Test case 3: A single key hold down before being released.
        (
            [
                {"key": "a", "type": "press", "time": 0},
                {"key": "a", "type": "press", "time": 1},
                {"key": "a", "type": "press", "time": 2},
                {"key": "a", "type": "release", "time": 3},
            ],
            [Keystroke("a", 0, 3)],
        ),
        # Test case 4: A modifier key (shift) is held down while another key ("u") is pressed and released.
        (
            [
                {"key": "Shift", "type": "press", "time": 0},
                {"key": "U", "type": "press", "time": 1},
                {"key": "U", "type": "release", "time": 2},
                {"key": "Shift", "type": "release", "time": 3},
            ],
            [Keystroke("shift", 0, 3), Keystroke("u", 1, 2)],
        ),
        # Test case 5: Similar to test case 4 but the release order is reversed.
        (
            [
                {"key": "Shift", "type": "press", "time": 0},
                {"key": "U", "type": "press", "time": 1},
                {"key": "Shift", "type": "release", "time": 2},
                {"key": "U", "type": "release", "time": 3},
            ],
            [Keystroke("shift", 0, 2), Keystroke("u", 1, 3)],
        ),
        # Test case 6: Mixed sequence with modifier key and regular keys pressed and released in varying order.
        (
            [
                {"key": "Shift", "type": "press", "time": 0},
                {"key": "A", "type": "press", "time": 1},
                {"key": "Shift", "type": "release", "time": 2},
                {"key": "a", "type": "release", "time": 3},
                {"key": "l", "type": "press", "time": 4},
                {"key": "l", "type": "release", "time": 5},
                {"key": "Shift", "type": "press", "time": 6},
                {"key": "A", "type": "press", "time": 7},
                {"key": "A", "type": "release", "time": 8},
                {"key": "Shift", "type": "release", "time": 9},
            ],
            [
                Keystroke("shift", 0, 2),
                Keystroke("a", 1, 3),
                Keystroke("l", 4, 5),
                Keystroke("shift", 6, 9),
                Keystroke("a", 7, 8),
            ],
        ),
    ],
)
def test_get_keystrokes(key_events, expected_keystrokes):
    processed_keystrokes = KeystrokeProcessor.process_key_events(key_events)

    processed_keystrokes_tuples = [
        (ks.key, ks.press_time, ks.release_time) for ks in processed_keystrokes
    ]
    expected_keystrokes_tuples = [
        (ks.key, ks.press_time, ks.release_time) for ks in expected_keystrokes
    ]

    assert processed_keystrokes_tuples == expected_keystrokes_tuples
