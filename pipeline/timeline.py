def build_timeline(results):

    timeline = {}

    for r in results:
        vid = r["video_id"]

        if vid not in timeline:
            timeline[vid] = []

        timeline[vid].append(r)

    # sort by timestamp
    for vid in timeline:
        timeline[vid].sort(key=lambda x: x["timestamp"])

    return timeline
