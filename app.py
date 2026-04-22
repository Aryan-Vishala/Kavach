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

st.title("🛡️ Kavach: AI Content Intelligence System")
st.markdown("Track • Detect • Protect digital media")

st.markdown("### 🎬 Demo Mode")

if st.button("🚀 Run Demo"):

    st.info("🔍 Analyzing content...")

    # fake delay
    import time
    for step in ["Scanning YouTube...", "Scanning Instagram...", "Scanning Twitter..."]:
        st.write(step)
        time.sleep(0.5)

    st.success("✅ Analysis Complete")

    st.subheader("⏳ Content Propagation Timeline")

    timeline = [
        ("YouTube", "Full Upload", "08:12 PM"),
        ("Instagram", "Cropped Version", "08:45 PM"),
        ("Twitter", "Edited Version", "09:10 PM"),
    ]

    for platform, event, time_stamp in timeline:
        st.markdown(f"**{time_stamp}** — 🔵 {platform} → {event}")

    st.divider()

    # INTELLIGENCE SUMMARY
    st.subheader("📊 Intelligence Summary")

    def animate_metric(label, value):
        placeholder = st.empty()
        for i in range(1, value + 1):
            placeholder.metric(label, str(i))
            time.sleep(0.05)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        animate_metric("Platforms", 3)
    with col2:
        animate_metric("Videos Found", 7)
    with col3:
        animate_metric("Channels", 5)
    with col4:
        st.metric("Spread Speed", "High")
    with col5:
        st.metric("Risk", "HIGH")
    
    st.divider()

    # CONFIDENCE BREAKDOWN
    import pandas as pd
    st.subheader("📉 Confidence Breakdown")
    conf_data = {
        "Metric": ["Visual Similarity", "Frame Coverage", "Temporal Consistency"],
        "Score": [0.91, 0.85, 0.88]
    }
    df_conf = pd.DataFrame(conf_data)
    st.bar_chart(df_conf.set_index("Metric"))

    st.divider()

    # PLATFORM BREAKDOWN & MODIFICATION DISTRIBUTION
    colA, colB = st.columns(2)
    with colA:
        st.subheader("📊 Platform Distribution")
        data = {
            "Platform": ["YouTube", "Instagram", "Twitter"],
            "Videos": [2, 2, 3]
        }
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index("Platform"))
        
    with colB:
        st.subheader("🧪 Modification Analysis")
        mod_data = {
            "Type": ["Full", "Cropped", "Edited", "Reversed", "Speed"],
            "Count": [2, 1, 2, 1, 1]
        }
        df_mod = pd.DataFrame(mod_data)
        st.bar_chart(df_mod.set_index("Type"))

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

    # VIDEOS
    st.subheader("📺 YouTube Variants")
    yt_cols = st.columns(2)

    with yt_cols[0]:
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:12px'>", unsafe_allow_html=True)
            st.video("data/platforms/youtube/full.mp4")
            st.markdown("""
            **Type:** Full Copy  
            **Match Score:** 1.0  
            **Channel:** sports_fan_123  
            **Upload Time:** 2 hrs ago  
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    with yt_cols[1]:
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:12px'>", unsafe_allow_html=True)
            st.video("data/platforms/youtube/clip.mp4")
            st.markdown("""
            **Type:** Short Clip  
            **Match Score:** 0.92  
            **Channel:** highlights_now  
            **Upload Time:** 1.5 hrs ago  
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("📸 Instagram Variants")
    ig_cols = st.columns(2)

    with ig_cols[0]:
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:12px'>", unsafe_allow_html=True)
            st.video("data/platforms/instagram/cropped.mp4")
            st.markdown("""
            **Type:** Cropped  
            **Match Score:** 0.78  
            **Channel:** viral.vids  
            **Upload Time:** 1 hr ago  
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    with ig_cols[1]:
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:12px'>", unsafe_allow_html=True)
            st.video("data/platforms/instagram/10sec_clip.mp4")
            st.markdown("""
            **Type:** Short Clip  
            **Match Score:** 0.81  
            **Channel:** insta_reels  
            **Upload Time:** 45 mins ago  
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🐦 Twitter Variants")
    tw_cols = st.columns(3)

    with tw_cols[0]:
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:12px'>", unsafe_allow_html=True)
            st.video("data/platforms/twitter/filtered.mp4")
            st.markdown("""
            **Type:** Edited  
            **Match Score:** 0.65  
            **Channel:** @fast_news  
            **Upload Time:** 10 mins ago  
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    with tw_cols[1]:
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:12px'>", unsafe_allow_html=True)
            st.video("data/platforms/twitter/reversed.mp4")
            st.markdown("""
            **Type:** Reversed  
            **Match Score:** 0.62  
            **Channel:** @anon_user  
            **Upload Time:** 5 mins ago  
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    with tw_cols[2]:
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:12px'>", unsafe_allow_html=True)
            st.video("data/platforms/twitter/speed_2x.mp4")
            st.markdown("""
            **Type:** 2x Speed  
            **Match Score:** 0.68  
            **Channel:** @trend_tracker  
            **Upload Time:** Just now  
            """)
            st.markdown("</div>", unsafe_allow_html=True)

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

    fig, ax = plt.subplots(figsize=(12, 7))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3500,
        node_color=color_map,
        font_color="white",
        edge_color="cyan",
        width=2,
        font_size=9,
        ax=ax
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    ax.set_facecolor("#020617")
    fig.patch.set_facecolor("#020617")

    st.pyplot(fig)
