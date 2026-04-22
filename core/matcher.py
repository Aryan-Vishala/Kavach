import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class RegionMatcher:
    def __init__(self, global_thresh=0.75, region_thresh=0.88):
        self.global_thresh = global_thresh
        self.region_thresh = region_thresh

    def match(self, query_feats, db_feats):
        best_score = 0.0

        # Global comparison
        global_score = cosine_similarity(query_feats[0], db_feats[0])
        best_score = max(best_score, global_score)

        if global_score >= self.global_thresh:
            return True, best_score

        # Region-wise comparison
        for q in query_feats[1:]:
            for d in db_feats[1:]:
                sim = cosine_similarity(q, d)
                best_score = max(best_score, sim)

                if sim >= self.region_thresh:
                    return True, best_score

        return False, best_score