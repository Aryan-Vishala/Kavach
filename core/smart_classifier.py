import numpy as np
from sklearn.tree import DecisionTreeClassifier


class SmartClassifier:
    def __init__(self):
        self.model = DecisionTreeClassifier(max_depth=4)
        self._train()

    def _train(self):
        """
        Tiny synthetic training (based on your expected patterns)
        You can improve later with real collected data
        """

        # Features:
        # [avg_similarity, max_similarity, match_ratio, variance]

        X = [
            # FULL
            [0.95, 1.0, 0.9, 0.01],
            [0.93, 0.98, 0.85, 0.02],

            # CROPPED
            [0.80, 0.90, 0.65, 0.04],
            [0.78, 0.88, 0.6, 0.05],

            # EDITED
            [0.65, 0.82, 0.45, 0.08],
            [0.60, 0.78, 0.4, 0.1],
        ]

        y = [
            "full", "full",
            "cropped", "cropped",
            "edited", "edited"
        ]

        self.model.fit(X, y)

    def predict(self, features):
        return self.model.predict([features])[0]
