import cv2
import numpy as np


class GISTExtractor:
    def __init__(self, orientations=(0, 45, 90, 135), scales=(3, 5), grid_size=4):
        self.orientations = orientations
        self.scales = scales
        self.grid_size = grid_size
        self.kernels = self._build_gabor_kernels()

    def _build_gabor_kernels(self):
        kernels = []
        for theta in self.orientations:
            theta_rad = theta / 180.0 * np.pi
            for sigma in self.scales:
                kernel = cv2.getGaborKernel(
                    ksize=(21, 21),
                    sigma=sigma,
                    theta=theta_rad,
                    lambd=10.0,
                    gamma=0.5,
                    psi=0
                )
                kernels.append(kernel)
        return kernels

    def _apply_gabor_filters(self, image):
        responses = []
        for kernel in self.kernels:
            filtered = cv2.filter2D(image, cv2.CV_32F, kernel)
            responses.append(filtered)
        return responses

    def _spatial_pooling(self, responses):
        h, w = responses[0].shape
        gh, gw = self.grid_size, self.grid_size

        cell_h = h // gh
        cell_w = w // gw

        features = []

        for response in responses:
            for i in range(gh):
                for j in range(gw):
                    cell = response[
                        i * cell_h:(i + 1) * cell_h,
                        j * cell_w:(j + 1) * cell_w
                    ]
                    features.append(cell.mean())

        return np.array(features, dtype=np.float32)

    def extract(self, frame):
        # Step 1: grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Step 2: resize (important for consistency)
        gray = cv2.resize(gray, (128, 128))

        # Step 3: normalize
        gray = gray.astype(np.float32) / 255.0

        # Step 4: apply filters
        responses = self._apply_gabor_filters(gray)

        # Step 5: pooling
        feature_vector = self._spatial_pooling(responses)

        # Step 6: normalize vector
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector /= norm

        return feature_vector