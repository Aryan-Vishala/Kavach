# 🛡️ Kavach — AI Content Intelligence System

## 🚨 Problem Statement

Sports organizations generate massive volumes of high-value digital media that rapidly scatter across global platforms. Once released, this content becomes extremely difficult to track.

This visibility gap leads to:

* ❌ Unauthorized redistribution
* ❌ Content manipulation (cropping, editing, filters)
* ❌ Intellectual property violations
* ❌ Revenue and brand value loss

With the rise of AI-generated edits and rapid social media propagation, traditional watermarking and manual monitoring are no longer sufficient.

---

## 🎯 Objective

To develop a scalable, intelligent system that:

* Identifies unauthorized use of official sports media
* Tracks how content propagates across platforms
* Detects modified versions (cropped, edited, sped-up, reversed)
* Provides actionable insights into content misuse
* Enables proactive protection of digital assets

---

## 💡 Our Solution

**Kavach** is an AI-powered Content Intelligence System that goes beyond simple video matching.

It reconstructs the **full lifecycle of content propagation** across platforms like YouTube, Instagram, and Twitter—detecting not just copies, but *how content evolves*.

---

## 🧠 How It Works

### 🔹 1. Feature Extraction (CNN-based)

We use deep learning (via PyTorch CNN models) to extract **robust visual embeddings** from video frames.

```text
Video → Frames → CNN → Feature Embeddings
```

---

### 🔹 2. Intelligent Matching

Instead of naive frame comparison, Kavach uses:

* ✔ Subclip matching (detects short clips inside long videos)
* ✔ Region-aware comparison (handles cropped content)
* ✔ Multi-signal similarity (average, max, consistency, variance)

---

### 🔹 3. Modification Detection

The system classifies how content has been altered:

* 🟢 Full Copy
* 🟠 Cropped
* 🔴 Edited
* 🎨 Styled (filters/colors)
* 🔄 Reversed
* ⏩ Speed Modified

---

### 🔹 4. Propagation Intelligence Engine

Kavach reconstructs **how content spreads**:

```text
Original
   ↓
YouTube (Full Upload)
   ↓
Instagram (Cropped)
   ↓
Twitter (Edited / Reversed / Speed)
```

---

### 🔹 5. AI Classification Layer

A lightweight Machine Learning model (Decision Tree) analyzes:

* Visual similarity
* Frame coverage
* Temporal consistency
* Variation across frames

This enables **robust and explainable classification**.

---

### 🔹 6. Real-Time Intelligence Dashboard

A premium Streamlit-based UI visualizes:

* 📊 Content Intelligence Summary
* 🎥 Platform-wise video variants
* 🌐 Propagation Network Graph
* ⏳ Animated Timeline
* 🧪 Modification Distribution
* 🕵️ Leak Source Analysis

---

## ⚡ Performance Optimization

To ensure real-time responsiveness:

* ✅ Embeddings precomputed and cached (.npy)
* ✅ Demo mode uses precomputed intelligence (instant UI)
* ✅ Frame sampling + stride-based matching
* ✅ Early rejection for non-matching content

---

## 🎬 Live Demo

🔗 **Live Prototype:**
*(Add your Streamlit Cloud link here)*

---

## 🎥 Demo Video

🔗 *(Add your video link here)*

---

## 🛠️ Tech Stack

* **Deep Learning:** PyTorch, Torchvision
* **Computer Vision:** OpenCV
* **ML Model:** Scikit-learn (Decision Tree)
* **Backend Logic:** Python
* **Visualization:** NetworkX, Matplotlib
* **Frontend/UI:** Streamlit
* **Data Handling:** NumPy, Pandas

---

## 📁 Project Structure

```
Kavach/
│
├── app.py                  # Streamlit dashboard
├── main.py                 # CLI pipeline
│
├── core/                   # Feature extraction
├── pipeline/               # Matching & propagation logic
├── storage/                # Embeddings & DB
│
├── data/                   # Demo dataset
├── demo_cache.json         # Precomputed results
│
├── requirements.txt
└── README.md
```

---

## 🚀 Key Features

* 🔍 Multi-platform content detection
* 🎥 Subclip and partial match detection
* 🧠 AI-based modification classification
* 🌐 Propagation network reconstruction
* 📊 Intelligence-driven dashboard
* ⚡ Real-time demo via cached pipeline
* 🔒 Scalable architecture (cloud-ready)

---

## ☁️ Scalability & Future Scope

Kavach is designed to scale using cloud infrastructure:

* ☁️ Google Cloud Storage for media ingestion
* ⚡ Distributed processing for large-scale monitoring
* 🌍 Multi-platform API integration (YouTube, Instagram, etc.)
* 🤖 Advanced AI models for deeper manipulation detection

---

## 🧠 Impact

Kavach transforms content protection from:

```text
Reactive Monitoring ❌
```

to:

```text
Proactive Intelligence ✔
```

---

## 🏁 Conclusion

Kavach is not just a detection tool—it is a **Content Intelligence Platform** that empowers sports organizations to:

* Protect digital assets
* Understand content propagation
* Detect misuse instantly
* Take proactive enforcement actions

---

## 👨💻 Built For

Hackathon Challenge: **AI-driven Media Protection & Content Intelligence**

---

## 🙌 Final Note

> “In a world where content spreads faster than control, Kavach ensures protection through intelligence.”
