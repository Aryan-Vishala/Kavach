import cv2
import numpy as np


class HOGExtractor:
    def __init__(self):
        # OpenCV HOG descriptor with default params
        self.hog = cv2.HOGDescriptor(
            _winSize=(128, 128),
            _blockSize=(16, 16),
            _blockStride=(8, 8),
            _cellSize=(8, 8),
            _nbins=9
        )

    def extract(self, frame):
        # Step 1: grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Step 2: resize (must match winSize)
        gray = cv2.resize(gray, (128, 128))

        # Step 3: normalize
        gray = gray.astype(np.uint8)

        # Step 4: compute HOG
        features = self.hog.compute(gray)

        # Step 5: flatten
        features = features.flatten()

        # Step 6: normalize vector
        norm = np.linalg.norm(features)
        if norm > 0:
            features /= norm

        return features