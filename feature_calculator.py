# feature_calculator.py
class FeatureCalculator:
    @staticmethod
    def calculate_features(keystrokes):
        """
        Calculate keystroke features: keys, DD, UD, and DU times.

        keystrokes: list of Keystroke instances, where each instance contains attributes for key, press_time, and release_time

        Returns a dictionary with the following structure:
        {
            'keys': [keys...],
            'DD': [down-down times...],
            'UD': [up-down times...],
            'DU': [down-up times...],
        }
        """
        # Initialize features with keys and placeholders for the first DD and UD times
        features = {
            "keys": [ks.key for ks in keystrokes],
            "DD": [],
            "UD": [],
            "DU": [],
        }

        # Calculate the DU time for each keystroke
        for ks in keystrokes:
            features["DU"].append(ks.release_time - ks.press_time)

        # Calculate DD and UD times for the rest of the keystrokes
        for i in range(1, len(keystrokes)):
            prev_ks = keystrokes[i - 1]
            ks = keystrokes[i]

            # Down-Down Time (DD)
            dd_time = ks.press_time - prev_ks.press_time
            features["DD"].append(dd_time)

            # Up-Down Time (UD)
            ud_time = ks.press_time - prev_ks.release_time
            features["UD"].append(ud_time)

        return features
