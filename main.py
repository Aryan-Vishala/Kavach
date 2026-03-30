import sys
from pipeline.register import register_video
from pipeline.detect import detect_video


def main():

    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  Register: python main.py register <video_path>")
        print("  Detect:   python main.py detect <video_path> [mode]")
        return

    command = sys.argv[1]
    video_path = sys.argv[2]

    if command == "register":
        video_id = register_video(video_path)
        print(f"\n✅ Registered Video ID: {video_id}")

    elif command == "detect":

        # 🔥 FIXED MODE HANDLING
        mode = "fast"
        if len(sys.argv) >= 4:
            mode = sys.argv[3]

        print("Selected mode:", mode)

        result = detect_video(video_path, mode=mode)

        print("\n🎯 Detection Result:")
        print(result)

    else:
        print("❌ Invalid command")


if __name__ == "__main__":
    main()