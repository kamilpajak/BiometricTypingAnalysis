import pytest

from models import Keystroke, KeystrokeTimingFeatures


@pytest.mark.parametrize(
    "keystrokes_data, expected_features",
    [
        # Test case 1: Simple key presses and releases
        (
            [
                Keystroke("a", 0, 1),
                Keystroke("b", 2, 3),
            ],
            {
                "keystrokes": [
                    {"key": "a", "press_time": 0, "release_time": 1},
                    {"key": "b", "press_time": 2, "release_time": 3},
                ],
                "press_to_press": [2],
                "release_to_press": [1],
                "press_to_release": [1, 1],
            },
        ),
        # Test case 2: Overlapping key presses
        (
            [
                Keystroke("a", 0, 3),
                Keystroke("b", 1, 4),
                Keystroke("c", 5, 6),
            ],
            {
                "keystrokes": [
                    {"key": "a", "press_time": 0, "release_time": 3},
                    {"key": "b", "press_time": 1, "release_time": 4},
                    {"key": "c", "press_time": 5, "release_time": 6},
                ],
                "press_to_press": [1, 4],
                "release_to_press": [-2, 1],
                "press_to_release": [3, 3, 1],
            },
        ),
    ],
)
def test_keystroke_timing_features(keystrokes_data, expected_features):

    keystroke_timing_features = KeystrokeTimingFeatures(
        keystrokes=keystrokes_data, user_id=1
    )

    assert (
        keystroke_timing_features.features.get("keystrokes")
        == expected_features["keystrokes"]
    )
    assert (
        keystroke_timing_features.features.get("press_to_press")
        == expected_features["press_to_press"]
    )
    assert (
        keystroke_timing_features.features.get("release_to_press")
        == expected_features["release_to_press"]
    )
    assert (
        keystroke_timing_features.features.get("press_to_release")
        == expected_features["press_to_release"]
    )
