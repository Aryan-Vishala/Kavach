from PIL import Image
import cv2
import imagehash


def compute_hashes(frame):
    """
    Compute perceptual hashes for a frame
    """

    # 🔹 Convert BGR (OpenCV) → RGB (PIL)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 🔹 Resize to fixed size (VERY IMPORTANT for consistency)
    frame = cv2.resize(frame, (256, 256))

    img = Image.fromarray(frame)

    # 🔹 Compute hashes
    phash = imagehash.phash(img)
    dhash = imagehash.dhash(img)

    return phash, dhash


def hash_similarity(hash1, hash2):
    """
    Convert Hamming distance → similarity (0 to 1)
    """
    max_bits = 64
    return 1 - (hash1 - hash2) / max_bits