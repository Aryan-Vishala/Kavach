def explain_match(score, mod_type):
    if mod_type == "full":
        return "High confidence direct reuse of original content"
    elif mod_type == "cropped":
        return "Partial reuse detected; content likely trimmed or zoomed"
    elif mod_type == "edited":
        return "Content modified with overlays, filters, or edits"
    else:
        return "Low similarity; unlikely to be related"

def recommend_action(risk):
    if risk == "HIGH":
        return "Immediate takedown recommended and legal review required"
    elif risk == "MEDIUM":
        return "Monitor usage and consider issuing warning"
    else:
        return "No action required; low-risk redistribution"

def generate_report(timeline_data):
    print("\n" + "="*50)
    print("📊 CONTENT INTELLIGENCE REPORT")
    print("="*50)

    for vid, events in timeline_data.items():
        if not events:
            continue
            
        print(f"\nVideo ID: {vid}\n")
        
        # Propagation Summary
        platforms_seen = [e['platform'] for e in events]
        spread_score = len(events)
        
        if spread_score >= 3:
            spread_label = "VIRAL"
        elif spread_score == 2:
            spread_label = "GROWING"
        else:
            spread_label = "ISOLATED"
            
        print("Propagation Summary:")
        print(f"- Detected on {spread_score} platforms")
        print(f"- Spread pattern: {spread_label}")
        
        # ASCII Visual Graph map
        print("\nDissemination Graph:")
        print("  Original")
        for p in platforms_seen:
            print("      ↓")
            print(f"  {p.capitalize()}")
        
        print("\nModification Analysis:")
        mod_type_map = {
            "full": "Full copy",
            "styled": "Styled (Filter/Color change)",
            "cropped": "Cropped",
            "edited": "Edited",
            "different": "Different"
        }
        for e in events:
            mod_str = mod_type_map.get(e["type"], "Unknown")
            print(f"- {e['platform'].capitalize()}: {mod_str}")
            
        # Risk Assessment
        types = [e["type"] for e in events]
        if "edited" in types:
            risk = "HIGH"
            explanation = "Content has been significantly modified and redistributed"
        elif "cropped" in types:
            risk = "MEDIUM"
            explanation = "Content has been cropped and shared unauthorized"
        else:
            risk = "LOW"
            explanation = "Direct copy shared across platforms"
            
        print("\nRisk Assessment:")
        print(f"- {risk} RISK")
        
        # Explanation
        print("\nExplanation:")
        print(f"- {explanation}")
        
        # Recommended Action
        print("\nRecommended Action:")
        print(f"→ {recommend_action(risk)}")
        
        # Source Analysis
        first_event = events[0]
        first_platform = first_event["platform"].capitalize()
        source_confidence = "High" if first_event["type"] == "full" else "Medium"
        
        print("\nSource Analysis:")
        print(f"- Origin likely: {first_platform}")
        print(f"- Confidence: {source_confidence}")
        
    print("\n" + "="*50)


def compute_risk_score(results: list) -> dict:
    """
    Computes a 0-100 risk score for each platform based on:
    - Confidence of match (40%)
    - Modification type severity (30%)
    - Number of channels on platform (20%)
    - Spread speed (10%)
    """
    MOD_WEIGHT = {
        "full": 1.0,
        "edited": 0.9,
        "cropped": 0.7,
        "styled": 0.5,
        "reversed": 0.6,
        "speed": 0.4
    }

    platform_scores = {}

    # Group results by platform
    by_platform = {}
    for r in results:
        p = r["platform"]
        by_platform.setdefault(p, []).append(r)

    max_channels = max(len(v) for v in by_platform.values()) if by_platform else 1

    for platform, events in by_platform.items():
        # 1. Average confidence across all matches on this platform
        avg_conf = sum(e["confidence"] for e in events) / len(events)
        conf_score = avg_conf * 40  # max 40 points

        # 2. Worst modification type on this platform
        worst_mod = max(events, key=lambda e: MOD_WEIGHT.get(e["type"], 0.5))
        mod_score = MOD_WEIGHT.get(worst_mod["type"], 0.5) * 30  # max 30 points

        # 3. Number of channels (normalized)
        channel_score = (len(events) / max_channels) * 20  # max 20 points

        # 4. Spread speed — earlier timestamp = more spread = higher risk
        # For demo: YouTube gets 10, Instagram 7, Twitter 4
        speed_map = {"youtube": 10, "instagram": 7, "twitter": 4}
        speed_score = speed_map.get(platform, 5)

        total = conf_score + mod_score + channel_score + speed_score
        platform_scores[platform] = round(min(total, 100))

    return platform_scores


def risk_label(score: int) -> str:
    if score >= 80:
        return "🔴 CRITICAL"
    elif score >= 60:
        return "🟠 HIGH"
    elif score >= 40:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"
