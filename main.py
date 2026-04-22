import sys
from pipeline.register import register_video
from pipeline.detect import detect_video
from pipeline.propagation_engine import PropagationEngine
from pipeline.timeline import build_timeline
from pipeline.report_generator import generate_report


def main():

    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  Register: python main.py register <video_path>")
        print("  Detect:   python main.py detect <video_path> [mode] (Old Flow)")
        print("  Analyze:  python main.py analyze <platforms_folder_path> (Intelligence Demo)")
        return

    command = sys.argv[1]
    path = sys.argv[2]

    if command == "register":
        video_id = register_video(path)
        print(f"\n✅ Registered Video ID: {video_id}")

    elif command == "detect":
        print("Selected mode: Intelligent (Auto)")
        result = detect_video(path)
        print("\n🎯 Detection Result:")
        print(result)

    elif command == "analyze":
        print(f"\n🔎 Starting Intelligence Propagation Scan on: {path}...\n")
        engine = PropagationEngine()
        results = engine.run(path)

        if not results:
            print("No matching distribution found. System clear.")
            return

        # Convert raw results to the event format expected by the leak detector
        from datetime import datetime
        from pipeline.leak_detection import run_leak_analysis
        
        events = []
        for i, r in enumerate(results):
            events.append({
                "id": str(i),
                "platform": r["platform"],
                "channel": r["channel"],
                "timestamp": datetime.fromtimestamp(r["timestamp"]),
                "similarity": r["confidence"],
                "type": r["type"]
            })
            
        run_leak_analysis(events)

    else:
        print("❌ Invalid command")


if __name__ == "__main__":
    main()