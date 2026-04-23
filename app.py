import streamlit as st
import json
import time

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

    st.subheader("⏳ Propagation Timeline")

    timeline_data = [
        ("08:12 PM", "YouTube", "Full Upload"),
        ("08:45 PM", "Instagram", "Cropped"),
        ("09:10 PM", "Twitter", "Edited"),
    ]

    timeline_box = st.empty()

    for t, platform, action in timeline_data:
        timeline_box.markdown(f"""
        **{t}** — 🔵 {platform} → {action}
        """)
        time.sleep(0.7)

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

    # LEAK SOURCES TABLE
    st.subheader("🕵️ Leak Sources")
    channels = [
        {"Platform": "YouTube", "Channel": "sports_fan_123", "Type": "Full"},
        {"Platform": "Instagram", "Channel": "viral.vids", "Type": "Cropped"},
        {"Platform": "Twitter", "Channel": "@trend_tracker", "Type": "Edited"},
    ]
    st.table(channels)

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
