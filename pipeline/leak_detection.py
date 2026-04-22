import math
from datetime import datetime

# -----------------------------
# CONFIG (tune if needed)
# -----------------------------
W_SIM = 0.4
W_TIME = 0.3
W_MOD = 0.2
W_PLATFORM = 0.1

TAU = 300  # seconds decay (~5 min)

# -----------------------------
# PLATFORM PRIORS
# -----------------------------
PLATFORM_PRIOR = {
    ("youtube", "instagram"): 0.9,
    ("youtube", "twitter"): 0.85,
    ("instagram", "twitter"): 0.8,
    ("twitter", "youtube"): 0.3,
}

# -----------------------------
# SCORING FUNCTION
# -----------------------------
def compute_score(parent, child):
    # 1. Visual similarity (use child's similarity as proxy)
    sim = child["similarity"]

    # 2. Temporal proximity
    time_diff = (child["timestamp"] - parent["timestamp"]).total_seconds()
    if time_diff < 0:
        return 0  # invalid direction

    temporal_score = math.exp(-time_diff / TAU)

    # 3. Modification factor
    if child["type"].lower() == "edited":
        mod_score = 0.8
    else:
        mod_score = 1.0

    # 4. Platform prior
    platform_score = PLATFORM_PRIOR.get(
        (parent["platform"].lower(), child["platform"].lower()),
        0.5
    )

    # Final score
    score = (
        W_SIM * sim +
        W_TIME * temporal_score +
        W_MOD * mod_score +
        W_PLATFORM * platform_score
    )

    return score

# -----------------------------
# BUILD CAUSAL GRAPH
# -----------------------------
def build_graph(events):
    events = sorted(events, key=lambda x: x["timestamp"])

    for i in range(len(events)):
        best_parent = None
        best_score = 0

        for j in range(i):
            parent = events[j]
            child = events[i]

            score = compute_score(parent, child)

            if score > best_score:
                best_score = score
                best_parent = parent

        events[i]["parent"] = best_parent
        events[i]["parent_score"] = best_score

    return events

# -----------------------------
# FIND ORIGINAL
# -----------------------------
def find_original(events):
    # earliest high-confidence full match
    candidates = [
        e for e in events
        if e["similarity"] > 0.95 and e["type"].lower() == "full"
    ]

    if not candidates:
        return min(events, key=lambda x: x["timestamp"])

    return min(candidates, key=lambda x: x["timestamp"])

# -----------------------------
# FIND LEAK SOURCE
# -----------------------------
def find_leak(events, original):
    candidates = [e for e in events if e != original]
    
    if not candidates:
        return original, 100.0

    leak = max(candidates, key=lambda x: x.get("parent_score", 0))
    confidence = leak.get("parent_score", 0) * 100

    return leak, confidence

# -----------------------------
# BUILD PROPAGATION TREE
# -----------------------------
def build_tree(events):
    tree = {}

    for e in events:
        parent = e.get("parent")
        if parent is None:
            continue

        parent_id = parent["id"]
        tree.setdefault(parent_id, []).append(e)

    return tree

# -----------------------------
# PRINT TREE (nice format)
# -----------------------------
def print_tree(node, tree, level=0):
    indent = "  " * level
    print(f"{indent}- {node['platform']} ({node['channel']})")

    for child in tree.get(node["id"], []):
        print_tree(child, tree, level + 1)

# -----------------------------
# EXPLANATION
# -----------------------------
def explain(parent, child):
    reasons = []

    if child["similarity"] > 0.8:
        reasons.append(f"High visual similarity ({child['similarity']:.2f})")

    time_gap = (child["timestamp"] - parent["timestamp"]).total_seconds() / 60
    if time_gap < 10:
        reasons.append(f"Close upload time ({time_gap:.1f} min)")

    if child["type"].lower() == "edited":
        reasons.append("Edited version detected")

    if (parent["platform"], child["platform"]) in PLATFORM_PRIOR:
        reasons.append("Common platform transition")

    return reasons

# -----------------------------
# MAIN ANALYSIS FUNCTION
# -----------------------------
def run_leak_analysis(events):
    if not events:
        print("\n🚨 No events found for leak analysis.")
        return None
        
    # Build graph
    events = build_graph(events)

    # Find original
    original = find_original(events)

    # Find leak
    leak, confidence = find_leak(events, original)

    # Build tree
    tree = build_tree(events)

    # Output
    print("\n🚨 LEAK ANALYSIS\n")
    print(f"Original Upload: {original['platform']} ({original['channel']})")
    print(f"Most Probable Leak Source: {leak['platform']} ({leak['channel']})")
    print(f"Confidence: {confidence:.1f}%\n")

    print("Reasoning:")
    if leak != original:
        reasons = explain(leak["parent"], leak) if leak.get("parent") else []
        for r in reasons:
            print(f"✔ {r}")
    else:
        print("✔ No leaks detected. Only original found.")

    print("\n🌐 PROPAGATION TREE:")
    print_tree(original, tree)

    return {
        "original": original,
        "leak": leak,
        "confidence": confidence,
        "tree": tree
    }
