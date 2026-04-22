import uuid
import os
import numpy as np
from pipeline.fast_pipeline import FastVideoProcessor
from storage.storage import add_video


def register_video(video_path):

    print("📥 Registering video (CNN pipeline)...")

    processor = FastVideoProcessor()

    # Extract embeddings (list of frames → each has (5,1280))
    embeddings = processor.process(video_path)

    video_id = str(uuid.uuid4())
    os.makedirs("storage/embeddings", exist_ok=True)
    embedding_path = f"storage/embeddings/{video_id}.npy"
    np.save(embedding_path, embeddings)

    video_data = {
        "video_id": video_id,
        "num_frames": len(embeddings),
        "embedding_path": embedding_path
    }

    add_video(video_data)

    print("✅ Video registered successfully!")
    print("Video ID:", video_data["video_id"])

    return video_data["video_id"]