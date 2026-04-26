import streamlit as st
import json
import time
from gemini_summary import generate_gemini_summary
from pipeline.report_generator import compute_risk_score, risk_label
from pipeline.timeline import plot_timeline

st.set_page_config(layout="wide")

st.markdown("""
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
}

/* Cards */
.block-container {
    padding-top: 2rem;
}

/* Titles */
h1, h2, h3 {
    color: #f8fafc;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}

/* Buttons */
button {
    background: linear-gradient(90deg, #6366f1, #3b82f6);
    color: white;
    border-radius: 8px;
}

/* Divider glow */
hr {
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center; font-size: 42px;'>
🛡️ Kavach — Content Intelligence Dashboard
</h1>
<p style='text-align: center; color: #9ca3af;'>
AI-powered tracking of sports media across platforms
</p>
""", unsafe_allow_html=True)

st.markdown("### 🎬 Demo")

with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password", 
                                placeholder="Paste your key here")
    st.caption("Get yours free at aistudio.google.com")
    
    st.markdown("---")
    confidence_threshold = st.slider(
        "🎚️ Detection Sensitivity",
        min_value=0.50,
        max_value=0.99,
        value=0.70,
        step=0.01,
        help="Minimum confidence score to flag a match. Lower = catch more (may include false positives). Higher = only flag near-certain matches."
    )
    st.caption(f"Currently flagging matches above **{int(confidence_threshold * 100)}%** confidence")

run = st.button("🚀 Run Intelligence Scan", use_container_width=True)

if run:

    progress = st.progress(0)

    steps = [
        "Scanning YouTube...",
        "Scanning Instagram...",
        "Scanning Twitter...",
        "Analyzing propagation...",
        "Generating intelligence report..."
    ]

    for i, step in enumerate(steps):
        st.write(f"🔍 {step}")
        time.sleep(0.4)
        progress.progress((i + 1) * 20)

    st.success("✅ Analysis Complete")

    # --- GEMINI INTELLIGENCE SUMMARY ---
    st.markdown("## 🤖 AI Intelligence Summary")

    # Mock channels for the demo summary
    channels = [
        {"platform": "youtube", "channel": "sports_fan_123", "type": "full", "confidence": 0.98, "upload_time": "08:12 PM"},
        {"platform": "instagram", "channel": "viral.vids", "type": "cropped", "confidence": 0.85, "upload_time": "08:45 PM"},
        {"platform": "twitter", "channel": "@trend_tracker", "type": "edited", "confidence": 0.72, "upload_time": "09:10 PM"},
    ]

    if gemini_key:
        with st.spinner("Gemini is analyzing the propagation data..."):
            summary = generate_gemini_summary(channels, gemini_key)
        
        st.info(summary)
    else:
        st.warning("⚠️ Add your Gemini API key in the sidebar to enable AI summaries.")

    st.subheader("⏳ Propagation Timeline")

    from datetime import datetime, timedelta

    # Demo timeline data — replace with real results when engine connected
    demo_timeline_results = [
        {"platform": "youtube",   "channel": "sports_fan_123", "upload_time": "08:12 PM",
        "type": "full",    "confidence": 0.95, "video_id": "v1",
        "timestamp": int((datetime.now() - timedelta(minutes=90)).timestamp())},
        {"platform": "instagram", "channel": "viral.vids",     "upload_time": "08:45 PM",
        "type": "cropped", "confidence": 0.78, "video_id": "v1",
        "timestamp": int((datetime.now() - timedelta(minutes=57)).timestamp())},
        {"platform": "twitter",   "channel": "@fast_news",     "upload_time": "09:10 PM",
        "type": "edited",  "confidence": 0.65, "video_id": "v1",
        "timestamp": int((datetime.now() - timedelta(minutes=32)).timestamp())},
        {"platform": "twitter",   "channel": "@trend_tracker", "upload_time": "09:20 PM",
        "type": "reversed","confidence": 0.62, "video_id": "v1",
        "timestamp": int((datetime.now() - timedelta(minutes=22)).timestamp())},
    ]

    timeline_fig = plot_timeline(demo_timeline_results)
    if timeline_fig:
        st.pyplot(timeline_fig)

    st.divider()

    # INTELLIGENCE SUMMARY
    st.markdown("## 📊 Intelligence Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Platforms", "3")
    col2.metric("Videos Found", "7")
    col3.metric("Channels", "5")
    col4.metric("Risk Level", "HIGH")
    
    st.divider()

    # CONFIDENCE BREAKDOWN
    import pandas as pd
    st.subheader("📉 Confidence Analysis")

    conf = pd.DataFrame({
        "Metric": ["Visual", "Temporal", "Coverage"],
        "Score": [0.91, 0.88, 0.85]
    })

    st.bar_chart(conf.set_index("Metric"))

    st.divider()

    # PLATFORM BREAKDOWN & MODIFICATION DISTRIBUTION
    st.subheader("📊 Platform Distribution")

    data = pd.DataFrame({
        "Platform": ["YouTube", "Instagram", "Twitter"],
        "Videos": [2, 2, 3]
    })

    st.bar_chart(data.set_index("Platform"))

    st.divider()

    st.subheader("🎯 Platform Risk Scores")

    # Shared results for risk scores and table
    all_results = [
        {"platform": "youtube",   "confidence": 0.95, "type": "full",    "channel": "sports_fan_123", "time": "08:12 PM"},
        {"platform": "youtube",   "confidence": 0.92, "type": "cropped", "channel": "highlights_now", "time": "08:30 PM"},
        {"platform": "instagram", "confidence": 0.78, "type": "cropped", "channel": "viral.vids",     "time": "08:45 PM"},
        {"platform": "instagram", "confidence": 0.81, "type": "edited",  "channel": "insta_reels",    "time": "08:55 PM"},
        {"platform": "twitter",   "confidence": 0.65, "type": "edited",  "channel": "@fast_news",     "time": "09:10 PM"},
        {"platform": "twitter",   "confidence": 0.62, "type": "reversed","channel": "@anon_user",     "time": "09:15 PM"},
        {"platform": "twitter",   "confidence": 0.68, "type": "speed",   "channel": "@trend_tracker", "time": "09:20 PM"},
    ]

    scores = compute_risk_score(all_results)

    risk_cols = st.columns(len(scores))
    for col, (platform, score) in zip(risk_cols, scores.items()):
        label = risk_label(score)
        col.metric(
            label=f"{platform.capitalize()}",
            value=f"{score}/100",
            delta=label
        )

    st.divider()

    # LEAK SOURCES TABLE
    st.subheader("🕵️ Leak Sources")
    
    # Filter results by threshold
    filtered_results = []
    for r in all_results:
        if r["confidence"] >= confidence_threshold:
            # Add a formatted match string for the table
            r_display = r.copy()
            r_display["Match %"] = f"{int(r['confidence'] * 100)}%"
            filtered_results.append(r_display)
    
    if filtered_results:
        # Displaying with specific columns for a cleaner look
        st.table(filtered_results)
    else:
        st.info(f"No matches found above the current confidence threshold ({int(confidence_threshold * 100)}%). Try lowering the sensitivity in the sidebar.")

    st.divider()

    def video_card(title, path, desc):
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05);
                    padding:12px;
                    border-radius:12px;
                    margin-bottom:10px'>
            <h4 style='margin:0;'>{title}</h4>
        </div>
        """, unsafe_allow_html=True)
        st.video(path)
        st.caption(desc)

    # VIDEOS
    st.subheader("📺 YouTube Variants")
    yt_cols = st.columns(2)

    with yt_cols[0]:
        video_card("Full Upload", "data/platforms/youtube/full.mp4", "Match: 1.0 | sports_fan_123 | 2 hrs ago")

    with yt_cols[1]:
        video_card("Clip", "data/platforms/youtube/clip.mp4", "Match: 0.92 | highlights_now | 1.5 hrs ago")

    st.subheader("📸 Instagram Variants")
    ig_cols = st.columns(2)

    with ig_cols[0]:
        video_card("Cropped", "data/platforms/instagram/cropped.mp4", "Match: 0.78 | viral.vids | 1 hr ago")

    with ig_cols[1]:
        video_card("Short Clip", "data/platforms/instagram/10sec_clip.mp4", "Match: 0.81 | insta_reels | 45 mins ago")

    st.subheader("🐦 Twitter Variants")
    tw_cols = st.columns(3)

    with tw_cols[0]:
        video_card("Edited", "data/platforms/twitter/filtered.mp4", "Match: 0.65 | @fast_news | 10 mins ago")

    with tw_cols[1]:
        video_card("Reversed", "data/platforms/twitter/reversed.mp4", "Match: 0.62 | @anon_user | 5 mins ago")

    with tw_cols[2]:
        video_card("2x Speed", "data/platforms/twitter/speed_2x.mp4", "Match: 0.68 | @trend_tracker | Just now")

    st.divider()

    # GRAPH
    st.subheader("🌐 Propagation Network")

    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()

    # Root
    G.add_node("Original")

    # YouTube
    G.add_edge("Original", "YT Full")
    G.add_edge("Original", "YT Clip")

    # Instagram
    G.add_edge("YT Full", "IG Cropped")
    G.add_edge("YT Full", "IG Clip")

    # Twitter
    G.add_edge("IG Cropped", "TW Filtered")
    G.add_edge("TW Filtered", "TW Reversed")
    G.add_edge("TW Filtered", "TW Speed")

    pos = nx.spring_layout(G, seed=42)

    color_map = []
    for node in G:
        if "Full" in node:
            color_map.append("green")
        elif "Cropped" in node:
            color_map.append("orange")
        elif "Filtered" in node or "Edited" in node:
            color_map.append("red")
        else:
            color_map.append("lightblue")

    edge_labels = {
        ("Original", "YT Full"): "upload",
        ("Original", "YT Clip"): "clip",
        ("YT Full", "IG Cropped"): "crop",
        ("YT Full", "IG Clip"): "clip",
        ("IG Cropped", "TW Filtered"): "edit",
        ("TW Filtered", "TW Reversed"): "reverse",
        ("TW Filtered", "TW Speed"): "speedup",
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3500,
        node_color=color_map,
        edge_color="#38bdf8",
        font_color="white",
        width=2,
        font_size=9,
        ax=ax
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    ax.set_facecolor("#020617")
    fig.patch.set_facecolor("#020617")

    st.pyplot(fig)

    # FINAL TOUCH — CLEAN FOOTER
    st.markdown("""
    <hr>
    <p style='text-align:center; color:#6b7280'>
    Built with AI for Sports Media Protection • Kavach
    </p>
    """, unsafe_allow_html=True)
