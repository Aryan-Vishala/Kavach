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
