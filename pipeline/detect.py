from core.utils import extract_frames
from core.hashing import compute_hashes, hash_similarity
from core.orb import compute_orb, match_orb
from storage.storage import load_db


def compute_temporal_score(matched_indices):
    if len(matched_indices) < 2:
        return 0

    increasing = 0
    decreasing = 0

    for i in range(1, len(matched_indices)):
        if matched_indices[i] > matched_indices[i - 1]:
            increasing += 1
        elif matched_indices[i] < matched_indices[i - 1]:
            decreasing += 1

    total = len(matched_indices) - 1
    return max(increasing / total, decreasing / total)


def detect_video(input_video, mode="fast"):

    print("🔍 Detecting video...")
    print("MODE:", mode)

    input_frames = extract_frames(input_video)

    if len(input_frames) == 0:
        return {"match": False, "reason": "No frames extracted"}

    db = load_db()

    best_match = None
    best_score = 0

    import imagehash

    for video in db["videos"]:

        print("\n➡️ Checking video:", video["video_id"])

        stored_hashes = video["hashes"]
        stored_orb = video.get("orb", [])

        similarities = []
        matched_indices = []

        # 🔹 HASH MATCHING
        for f in input_frames:

            p1, d1 = compute_hashes(f)

            best_sim = 0
            best_index = -1

            for j, stored in enumerate(stored_hashes[:100]):

                p2 = imagehash.hex_to_hash(stored["phash"])
                d2 = imagehash.hex_to_hash(stored["dhash"])

                sim_p = hash_similarity(p1, p2)
                sim_d = hash_similarity(d1, d2)

                sim = (0.6 * sim_p) + (0.4 * sim_d)

                if sim > best_sim:
                    best_sim = sim
                    best_index = j

            similarities.append(best_sim)
            matched_indices.append(best_index)

        if not similarities:
            continue

        # 🔢 SCORES
        hash_score = sum(similarities) / len(similarities)
        match_ratio = sum(1 for s in similarities if s > 0.75) / len(similarities)
        temporal_score = compute_temporal_score(matched_indices)

        print(f"Hash: {round(hash_score,3)} | Temp: {round(temporal_score,3)}")

        pre_score = (
            0.75 * hash_score +
            0.2 * match_ratio +
            0.05 * temporal_score
        )

        print(f"Pre Score: {round(pre_score,3)}")

        # 🟢 FAST MODE
        if pre_score >= 0.85 and mode != "strict":
            return {
                "match": True,
                "video_id": video["video_id"],
                "confidence": float(pre_score),
                "stage": "hash"
            }

        if pre_score <= 0.55 and mode != "strict":
            continue

        # 🔥 ORB
        run_orb = False

        if mode == "strict":
            run_orb = True
        elif 0.55 < pre_score < 0.85:
            run_orb = True

        orb_score = 0

        if run_orb:
            print("⚠️ Running ORB...")

            orb_scores = []
            import numpy as np

            for f in input_frames[:20]:

                _, des1 = compute_orb(f)

                if des1 is None:
                    continue

                best_orb = 0

                for des2_list in stored_orb[:100]:

                    if des2_list is None:
                        continue

                    des2 = np.array(des2_list, dtype=np.uint8)

                    score = match_orb(des1, des2)

                    if score > best_orb:
                        best_orb = score

                orb_scores.append(best_orb)

            orb_score = sum(orb_scores) / len(orb_scores) if orb_scores else 0

        print("ORB Score:", round(orb_score, 3))

        # 🎯 FINAL SCORE
        if mode == "strict":
            final_score = (0.5 * pre_score + 0.5 * orb_score)
        else:
            final_score = pre_score if not run_orb else (0.7 * pre_score + 0.3 * orb_score)

        print(f"Final Score: {round(final_score,3)}")

        if final_score > best_score:
            best_score = final_score
            best_match = video["video_id"]

    if best_score >= 0.65:
        return {
            "match": True,
            "video_id": best_match,
            "confidence": float(best_score),
            "stage": "hash+orb"
        }

    return {
        "match": False,
        "confidence": float(best_score)
    }