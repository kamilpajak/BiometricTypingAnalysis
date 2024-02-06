import pytest

from feature_calculator import FeatureCalculator


# Define the test cases for the feature calculations
@pytest.mark.parametrize("keystrokes, expected_features", [
    # Test case 1: Simple key presses and releases
    ([
         ('a', 0, 1),
         ('b', 2, 3)
     ], {
         'keys': ['a', 'b'],
         'DD': [None, 2],
         'UD': [None, 1],
         'DU': [1, 1]
     }),

    # Test case 2: Overlapping key presses
    ([
         ('a', 0, 3),
         ('b', 1, 4),
         ('c', 5, 6)
     ], {
         'keys': ['a', 'b', 'c'],
         'DD': [None, 1, 4],
         'UD': [None, -2, 1],
         'DU': [3, 3, 1]
     }),

    # Add more test cases as needed...
])
def test_feature_calculator(keystrokes, expected_features):
    # Call the calculate_features method from the FeatureCalculator class
    features = FeatureCalculator.calculate_features(keystrokes)
    # Assert that the calculated features match the expected features
    assert features == expected_features
