from core.frame_sampler import FrameSampler
from core.cnn_region_fast import CNNRegionExtractorFast

class FastVideoProcessor:
    def __init__(self):
        self.sampler = FrameSampler(fps=1)
        self.extractor = CNNRegionExtractorFast()

    def process(self, video_path):
        frames = self.sampler.sample(video_path)
        embeddings = []
        for frame in frames:
            feats = self.extractor.extract(frame)
            embeddings.append(feats)
        return embeddings
