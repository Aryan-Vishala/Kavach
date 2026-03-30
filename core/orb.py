import cv2

# Initialize ORB detector
orb = cv2.ORB_create(nfeatures=500)


def compute_orb(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    return keypoints, descriptors


def match_orb(des1, des2):
    if des1 is None or des2 is None:
        return 0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    if len(matches) == 0:
        return 0

    # Sort matches by quality
    matches = sorted(matches, key=lambda x: x.distance)

    # Take best matches only (robustness)
    good_matches = matches[:int(len(matches) * 0.5)]

    score = len(good_matches) / max(len(des1), len(des2))

    return score