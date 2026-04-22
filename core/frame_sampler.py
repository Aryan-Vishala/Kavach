import cv2


def sample_frames(video_path, target_fps=1):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / target_fps) if fps > 0 else 30

    frames = []
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if idx % interval == 0:
            frames.append(frame)

        idx += 1

    cap.release()
    return frames