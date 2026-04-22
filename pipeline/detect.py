import time
import os
import numpy as np
from pipeline.propagation_engine import PropagationEngine

def detect_video(input_video):
    print(f"\n🔍 Detecting single video: {input_video}")
    
    stride = 5

    engine = PropagationEngine()
    query_embeddings = engine.processor.process(input_video)
    
    if not query_embeddings:
        return {"match": False, "reason": "No frames extracted"}
        
    best_score = 0
    best_match = None
    best_type = None
    best_features = None
    
    q_globals = np.array([q[0] for q in query_embeddings])
    q_norms = np.linalg.norm(q_globals, axis=1, keepdims=True)
    q_norms[q_norms == 0] = 1e-10
    q_globals = q_globals / q_norms

    for video in engine.db["videos"]:
        embedding_path = video.get("embedding_path")
        if embedding_path and os.path.exists(embedding_path):
            db_embeddings = np.load(embedding_path, allow_pickle=True)
        else:
            db_embeddings = video.get("cnn_embeddings", [])
            
        if len(db_embeddings) == 0:
            continue

        d_globals = np.array([d[0] for d in db_embeddings])
        d_norms = np.linalg.norm(d_globals, axis=1, keepdims=True)
        d_norms[d_norms == 0] = 1e-10
        d_globals = d_globals / d_norms

        sim_matrix = np.dot(q_globals, d_globals.T)
        max_frame_similarity = np.max(sim_matrix)

        if max_frame_similarity > best_score:
            best_score = float(max_frame_similarity)

        if max_frame_similarity < 0.6:
            continue  # quick pre-filter skip

        if len(query_embeddings) <= len(db_embeddings):
            scores = engine.fast_subclip_match(db_embeddings, query_embeddings, stride=stride)
        else:
            scores = engine.fast_subclip_match(query_embeddings, db_embeddings, stride=stride)

        if scores:
            features = engine.extract_features(scores)
            avg_sim = features[0]
            max_sim = features[1]
            match_ratio = features[2]

            # HARD RULES
            if max_sim > 0.97:
                mod_type = "full"
            elif max_sim > 0.92 and avg_sim > 0.88:
                mod_type = "styled"
            elif avg_sim > 0.75:
                mod_type = "cropped"
            elif avg_sim > 0.55:
                mod_type = "edited"
            else:
                mod_type = engine.classifier.predict(features)
                
            local_best = max(scores)
            
            if local_best > best_score:
                best_score = local_best
                best_match = video["video_id"]
                best_type = mod_type
                best_features = features

    if best_score > 0.55:
        match_ratio_pct = round(best_features[2] * 100, 1)
        print(f"\n✅ Match: True")
        print(f"Video ID: {best_match}")
        print(f"Confidence: {round(best_score, 3)}")
        print(f"Type: {best_type.capitalize()}")
        print(f"\n💡 Why matched:")
        print(f"- {match_ratio_pct}% frames matched securely")
        print(f"- High embedding similarity (Max: {round(best_features[1], 3)}, Avg: {round(best_features[0], 3)})")
        
        return {
            "match": True,
            "video_id": best_match,
            "confidence": round(best_score, 3),
            "type": best_type,
            "features": best_features
        }

    print("\n❌ Match: False")
    print(f"Confidence: {round(best_score, 3)}")
    return {
        "match": False,
        "confidence": round(best_score, 3)
    }