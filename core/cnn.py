import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2
from PIL import Image
import numpy as np


class CNNExtractor:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load pretrained model
        self.model = mobilenet_v2(pretrained=True)
        self.model.classifier = torch.nn.Identity()  # remove classifier
        self.model = self.model.to(self.device)
        self.model.eval()

        # Preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def extract(self, frame):
        # Convert OpenCV BGR → RGB
        frame = frame[:, :, ::-1]

        img = Image.fromarray(frame)
        img = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            features = self.model(img)

        features = features.squeeze().cpu().numpy()

        # Normalize
        norm = np.linalg.norm(features)
        if norm > 0:
            features /= norm

        return features