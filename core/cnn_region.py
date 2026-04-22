import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import numpy as np


class CNNRegionExtractor:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load pretrained model (clean API)
        self.model = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
        self.model.classifier = torch.nn.Identity()
        self.model = self.model.to(self.device)
        self.model.eval()

        # Transform
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def _embed(self, frame):
        # BGR → RGB
        frame = frame[:, :, ::-1]

        img = Image.fromarray(frame)
        img = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            feat = self.model(img)

        feat = feat.squeeze().cpu().numpy()

        # normalize
        norm = np.linalg.norm(feat)
        if norm > 0:
            feat /= norm

        return feat

    def extract(self, frame):
        h, w = frame.shape[:2]

        regions = [
            frame,  # global
            frame[:h//2, :w//2],      # top-left
            frame[:h//2, w//2:],      # top-right
            frame[h//2:, :w//2],      # bottom-left
            frame[h//2:, w//2:]       # bottom-right
        ]

        features = [self._embed(r) for r in regions]
        return features