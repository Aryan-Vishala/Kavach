import librosa
import numpy as np
import subprocess
import os
import uuid


def extract_audio_features(video_path):

    try:
        # 🔥 Create temp wav file
        temp_wav = f"temp_{uuid.uuid4().hex}.wav"

        # 🎯 Extract audio using ffmpeg
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",               # no video
            "-acodec", "pcm_s16le",
            "-ar", "22050",
            "-ac", "1",
            temp_wav,
            "-y"
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 🎧 Load extracted audio
        y, sr = librosa.load(temp_wav, sr=22050)

        # 🧠 MFCC features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        features = np.mean(mfcc, axis=1)

        # 🧹 Cleanup
        os.remove(temp_wav)

        return features

    except Exception as e:
        print("Audio extraction error:", e)
        return None


def compare_audio(f1, f2):

    if f1 is None or f2 is None:
        return 0

    similarity = np.dot(f1, f2) / (np.linalg.norm(f1) * np.linalg.norm(f2))

    return float(similarity)