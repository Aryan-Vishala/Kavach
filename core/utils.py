import cv2

def extract_frames(video_path, fps=1):
    cap = cv2.VideoCapture(video_path)

    frames = []
    video_fps = cap.get(cv2.CAP_PROP_FPS)

    interval = int(video_fps / fps) if video_fps > 0 else 1
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            frame = cv2.resize(frame, (640, 360))  # speed optimization
            frames.append(frame)

        count += 1

    cap.release()
    return frames