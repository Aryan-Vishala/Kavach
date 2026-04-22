import cv2
import numpy as np


def is_different(frame1, frame2, threshold=15):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    score = np.mean(diff)

    return score > threshold


def filter_frames(frames):
    if not frames:
        return []

    filtered = [frames[0]]

    for i in range(1, len(frames)):
        if is_different(filtered[-1], frames[i]):
            filtered.append(frames[i])

    return filtered