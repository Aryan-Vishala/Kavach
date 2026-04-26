import google.generativeai as genai

def generate_gemini_summary(results: list, api_key: str) -> str:
    """
    Takes the list of detection results from propagation_engine.run()
    and returns a natural language intelligence summary from Gemini.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Build a structured summary of results to send to Gemini
    if not results:
        return "No matches detected across scanned platforms."

    platform_lines = []
    for r in results:
        platform_lines.append(
            f"- Platform: {r['platform'].capitalize()} | "
            f"Channel: {r['channel']} | "
            f"Modification: {r['type'].capitalize()} | "
            f"Confidence: {int(r['confidence'] * 100)}% | "
            f"Detected at: {r['upload_time']}"
        )

    detections_text = "\n".join(platform_lines)
    num_platforms = len(set(r["platform"] for r in results))
    num_channels = len(set(r["channel"] for r in results))

    prompt = f"""
You are a sports media content intelligence analyst for a system called Kavach.

A proprietary sports video has been scanned across social media platforms.
Here are the detection results:

{detections_text}

Total platforms affected: {num_platforms}
Total unique channels found: {num_channels}

Write a concise, professional intelligence summary (5-7 sentences) that:
1. States how widely the content has spread
2. Describes the types of modifications made
3. Identifies the most concerning instance
4. Gives a clear recommended action for the sports organization
5. Ends with an overall threat level: LOW / MEDIUM / HIGH / CRITICAL

Do not use bullet points. Write in paragraph form. Be direct and professional.
"""

    response = model.generate_content(prompt)
    return response.text
