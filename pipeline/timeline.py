import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def build_timeline(results):
    """Original function — unchanged."""
    timeline = {}
    for r in results:
        vid = r["video_id"]
        if vid not in timeline:
            timeline[vid] = []
        timeline[vid].append(r)
    for vid in timeline:
        timeline[vid].sort(key=lambda x: x["timestamp"])
    return timeline


def plot_timeline(results: list):
    """
    Draws a visual horizontal timeline of when each platform
    picked up the content. Returns a matplotlib figure.
    """
    if not results:
        return None

    # Sort by timestamp
    sorted_results = sorted(results, key=lambda x: x["timestamp"])
    base_time = sorted_results[0]["timestamp"]

    PLATFORM_COLORS = {
        "youtube":   "#FF0000",
        "instagram": "#E1306C",
        "twitter":   "#1DA1F2",
    }

    MOD_SYMBOLS = {
        "full":     "★",
        "cropped":  "▲",
        "edited":   "●",
        "styled":   "◆",
        "reversed": "▼",
        "speed":    "►",
    }

    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    # Draw the main timeline axis
    ax.axhline(y=0, color="#38bdf8", linewidth=2, zorder=1)

    # Plot each event
    for i, event in enumerate(sorted_results):
        minutes_after = (event["timestamp"] - base_time) / 60
        color = PLATFORM_COLORS.get(event["platform"], "#ffffff")
        symbol = MOD_SYMBOLS.get(event["type"], "●")

        # Alternate above/below the line to avoid overlap
        y_pos = 0.4 if i % 2 == 0 else -0.4

        # Vertical connector
        ax.plot([minutes_after, minutes_after], [0, y_pos],
                color=color, linewidth=1.5, zorder=2, linestyle="--", alpha=0.6)

        # Event dot
        ax.scatter(minutes_after, y_pos, color=color, s=120, zorder=3)

        # Label
        label = f"{symbol} {event['platform'].capitalize()}\n{event['channel']}\n{event['upload_time']}"
        va = "bottom" if y_pos > 0 else "top"
        ax.text(minutes_after, y_pos + (0.05 if y_pos > 0 else -0.05),
                label, color="white", fontsize=7.5,
                ha="center", va=va, zorder=4)

    # X axis styling
    ax.set_xlabel("Minutes after original upload", color="#9ca3af", fontsize=10)
    ax.set_xlim(-5, max((e["timestamp"] - base_time) / 60 for e in sorted_results) + 15)
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.tick_params(colors="#9ca3af")
    ax.spines[:].set_visible(False)

    # Legend
    legend_patches = [
        mpatches.Patch(color=c, label=p.capitalize())
        for p, c in PLATFORM_COLORS.items()
    ]
    ax.legend(handles=legend_patches, loc="upper left",
              facecolor="#1e293b", labelcolor="white", fontsize=9)

    ax.set_title("Content Propagation Timeline", color="#f8fafc",
                 fontsize=13, pad=10)

    plt.tight_layout()
    return fig
