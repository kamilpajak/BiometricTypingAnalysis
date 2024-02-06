class FeatureCalculator:
    @staticmethod
    def calculate_features(keystrokes):
        """
        Calculate keystroke features: keys, DD, UD, and DU times.

        keystrokes: list of tuples, where each tuple contains (key, down_time, up_time)

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
            'keys': [k[0] for k in keystrokes],
            'DD': [None],  # First DD time is None because there's no preceding keystroke
            'UD': [None],  # First UD time is None because there's no preceding keystroke
            'DU': [],  # DU times will be calculated for each keystroke
        }

        # Calculate the DU time for each keystroke
        for _, down_time, up_time in keystrokes:
            features['DU'].append(up_time - down_time)

        # Calculate DD and UD times for the rest of the keystrokes
        for i in range(1, len(keystrokes)):
            _, prev_down_time, prev_up_time = keystrokes[i - 1]
            _, down_time, _ = keystrokes[i]

            # Down-Down Time (DD)
            dd_time = down_time - prev_down_time
            features['DD'].append(dd_time)

            # Up-Down Time (UD)
            ud_time = down_time - prev_up_time
            features['UD'].append(ud_time)

        return features
