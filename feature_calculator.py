import numpy as np


class FeatureCalculator:
    @staticmethod
    def calculate_features(keystrokes):
        """Calculate statistical features from the keystrokes."""
        dd_times = [keystrokes[i]['down_time'] - keystrokes[i - 1]['down_time'] for i in range(1, len(keystrokes))]
        ud_times = [keystrokes[i]['down_time'] - keystrokes[i - 1]['up_time'] for i in range(1, len(keystrokes))]
        du_times = [keystroke['up_time'] - keystroke['down_time'] for keystroke in keystrokes if 'up_time' in keystroke]

        features = {
            'DD Time': {'Mean': np.mean(dd_times) if dd_times else 0,
                        'Standard Deviation': np.std(dd_times, ddof=1) if len(dd_times) > 1 else 0},
            'UD Time': {'Mean': np.mean(ud_times) if ud_times else 0,
                        'Standard Deviation': np.std(ud_times, ddof=1) if len(ud_times) > 1 else 0},
            'DU Time': {'Mean': np.mean(du_times) if du_times else 0,
                        'Standard Deviation': np.std(du_times, ddof=1) if len(du_times) > 1 else 0},
        }

        return features
