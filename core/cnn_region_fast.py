import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import numpy as np


class CNNRegionExtractorFast:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.model = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
        self.model.classifier = torch.nn.Identity()
        self.model = self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def extract(self, frame):
        h, w = frame.shape[:2]

        regions = [
            frame,
            frame[:h//2, :w//2],
            frame[:h//2, w//2:],
            frame[h//2:, :w//2],
            frame[h//2:, w//2:]
        ]

        imgs = []
        for r in regions:
            r = r[:, :, ::-1]  # BGR → RGB
            img = Image.fromarray(r)
            img = self.transform(img)
            imgs.append(img)

        batch = torch.stack(imgs).to(self.device)

        with torch.no_grad():
            feats = self.model(batch)

        feats = feats.cpu().numpy()

        # normalize each vector
        norms = np.linalg.norm(feats, axis=1, keepdims=True)
        feats = feats / (norms + 1e-8)

        return feats  # shape: (5, 1280)