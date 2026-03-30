import uuid
from core.utils import extract_frames
from core.hashing import compute_hashes
from core.orb import compute_orb
from storage.storage import add_video
from core.audio import extract_audio_features

def register_video(video_path):

    print("📥 Registering video...")

    frames = extract_frames(video_path)
    audio_features = extract_audio_features(video_path)

    hashes = []
    orb_data = []

    for i, frame in enumerate(frames):

        phash, dhash = compute_hashes(frame)
        _, des = compute_orb(frame)

        hashes.append({
            "frame": i,
            "phash": str(phash),
            "dhash": str(dhash)
        })

        # Store ORB descriptors (convert to list for JSON)
        if des is not None:
            orb_data.append(des.tolist())
        else:
            orb_data.append(None)

    video_data = {
        "video_id": str(uuid.uuid4()),
        "total_frames": len(frames),
        "hashes": hashes,
        "orb": orb_data,
        "audio": audio_features.tolist() if audio_features is not None else None,
    }

    add_video(video_data)

    print("✅ Video registered successfully!")
    print("Video ID:", video_data["video_id"])

    return video_data["video_id"]