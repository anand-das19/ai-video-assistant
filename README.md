# 🎬 AI Video Assistant

An intelligent meeting and video analysis assistant that transforms lengthy video or meeting content into searchable, actionable knowledge using cutting-edge speech processing and Retrieval-Augmented Generation (RAG).

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7.svg)](https://render.com/)

---

## 🌐 Live Demo & Repository

- **Live Deployed Demo**: [AI Video Assistant on Render](https://ai-video-assistant.onrender.com) *(Update with your live Render URL)*
- **GitHub Repository**: [https://github.com/anand-das19/ai-video-assistant](https://github.com/anand-das19/ai-video-assistant)

> [!NOTE]
> Hosted on Render Free Web Service. Free instances may spin down after inactivity; initial wake-up may take 45–60 seconds.

---

## 🎯 The Challenge Addressed

Professionals and students spend hours watching recorded meetings, webinars, and lectures to extract actionable insights. **AI Video Assistant** automates this workflow:
1. Ingests video audio from public YouTube links or local recordings.
2. Transcribes spoken dialogue with high fidelity using OpenAI Whisper (English) or Sarvam AI (Hinglish with English translation).
3. Synthesizes a structured meeting overview: descriptive title, executive summary, action items with owners/deadlines, key decisions, and open questions.
4. Indexes the transcript into an isolated vector database (ChromaDB) to empower users to ask questions grounded strictly in the transcript via RAG.

---

## 🌟 Key Features

- **Multi-Source Audio Acquisition**: Direct public YouTube URL download via `yt-dlp` and local media conversion (`.mp4`, `.mp3`, `.wav`, etc.).
- **Automatic Audio Normalization**: Converts input audio to 16kHz mono WAV format and chunks long audio files for stable processing.
- **Accurate Speech-to-Text**:
  - **English**: Local OpenAI Whisper model (`small` by default, cached in-memory).
  - **Hinglish**: Integrated Sarvam AI API for Hindi-English audio with automatic translation to English.
- **Structured AI Insights (Mistral AI + LangChain)**:
  - Concise Title Generation
  - Executive Meeting Summary
  - Action Items Extraction (Task, Owner, Deadline)
  - Key Decisions Tracking
  - Unresolved Questions Identification
- **Transcript-Grounded RAG Q&A**: ChromaDB vector store paired with Mistral AI via LangChain LCEL pipelines. Answers only using transcript context to prevent hallucinations.
- **Session-Isolated Vector Stores**: Unique temporary Chroma collections and isolated temporary directories per run to avoid cross-user data leaks.
- **Clean & Safe Streamlit UI**: Dark-mode cybernetic dashboard with HTML-escaped text rendering to eliminate XSS/injection risks.

---

## 🚀 Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Core runtime |
| **Frontend** | Streamlit | Responsive web UI and state management |
| **Speech-to-Text** | OpenAI Whisper / Sarvam AI | Audio transcription & Hindi-to-English translation |
| **LLM & Orchestration**| Mistral AI (`mistral-small-latest`) & LangChain | LCEL chains for extraction, summarization, and RAG |
| **Vector Store** | ChromaDB & Sentence Transformers | Ephemeral semantic search & context retrieval |
| **Audio Processing** | FFmpeg, `yt-dlp`, `pydub` | Video audio extraction, format conversion & chunking |
| **Containerization** | Docker | Reproducible container runtime for cloud deployment |

---

## 📋 Prerequisites & System Requirements

- **Python**: Version `3.10` or `3.11` (Python `3.11` recommended)
- **FFmpeg**: **Required system package**. FFmpeg must be installed and available on the system PATH for audio conversion.
  - **Ubuntu / Debian**: `sudo apt update && sudo apt install -y ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Windows**: Install via `winget install Gyan.FFmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html) and add `bin/` to system PATH.

---

## 🔐 Environment Variables

Create a `.env` file in the root directory (see `.env.example`):

| Variable | Required | Description |
| :--- | :--- | :--- |
| `MISTRAL_API_KEY` | **Yes** | API key from [Mistral AI Console](https://console.mistral.ai/) |
| `SARVAM_API_KEY` | Optional | API key from [Sarvam AI](https://www.sarvam.ai/) (for Hinglish audio) |
| `WHISPER_MODEL` | Optional | Whisper model size (`tiny`, `base`, `small`, `medium`, `large`). Defaults to `small`. |
| `SARVAM_STT_MODEL` | Optional | Sarvam model identifier. Defaults to `saaras:v2.5`. |

> [!WARNING]
> Never commit `.env` or real API keys to version control. Set keys directly in your cloud hosting provider's dashboard.

---

## 🛠️ Local Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Video-Assistant.git
   cd AI-Video-Assistant
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual MISTRAL_API_KEY
   ```

5. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

6. **Run via CLI (optional)**
   ```bash
   python main.py
   ```

---

## ☁️ Deployment on Render (Free Web Service)

This repository includes a production-ready `Dockerfile` and `render.yaml` for zero-configuration deployment on Render.

### Option A: Automatic Blueprint Deployment (Recommended)
1. Fork or push this repository to your GitHub account.
2. In [Render Dashboard](https://dashboard.render.com/), click **New +** > **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml`.
4. Add your `MISTRAL_API_KEY` (and optionally `SARVAM_API_KEY`) under Environment Variables.
5. Click **Apply**.

### Option B: Manual Docker Web Service
1. In Render Dashboard, click **New +** > **Web Service**.
2. Select **Build and deploy from a Git repository**.
3. Choose **Docker** as the Environment / Runtime.
4. Set the **Instance Type** to **Free**.
5. Add Environment Variables:
   - `MISTRAL_API_KEY`: *your-mistral-api-key*
   - `SARVAM_API_KEY`: *(optional)*
   - `WHISPER_MODEL`: `small`
6. Click **Create Web Service**.

### Runtime & Port Binding Details
- Streamlit binds to `0.0.0.0` and listens on Render's dynamic `$PORT`:
  ```bash
  streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
  ```
- The Whisper model is loaded and cached in memory to avoid repeated loads on subsequent requests.
- All downloaded audio files and WAV chunks are stored in an isolated temporary directory and automatically deleted in a `finally` block once transcription completes.

---

## ⚠️ Known Limitations & Evaluation Notes

1. **Free CPU Latency**: Whisper model execution runs on CPU in Render's Free tier. The first transcription request can take 1–2 minutes as the model loads into RAM. For testing and evaluation, shorter YouTube videos (2–5 minutes) are recommended.
2. **Ephemeral Storage**: Render Free Web Services use ephemeral disks. Downloaded audio and vector database indices exist only for the duration of the analysis session.
3. **Free Tier Inactivity**: When idle for 15+ minutes, Render spins down free containers. The first request after idle will experience a spin-up delay (~50 seconds).
4. **Browser Inputs**: Cloud deployment supports public YouTube URLs. Local file path inputs are intended for local development only.

---

## 📂 Project Architecture

```
AI-Video-Assistant/
├── .env.example           # Example environment variable template
├── .gitignore             # Git ignore configuration
├── .dockerignore          # Docker build exclusion rules
├── .python-version        # Declared Python version (3.11.9)
├── Dockerfile             # Production container definition (Debian + FFmpeg)
├── render.yaml            # Render Blueprint deployment configuration
├── requirements.txt       # Production Python dependencies
├── app.py                 # Streamlit web application
├── main.py                # Command-line interface
├── test.py                # End-to-end integration test script
│
├── core/                  # Core AI & RAG Engine
│   ├── transcriber.py     # Whisper & Sarvam speech-to-text with caching
│   ├── summarizer.py      # Map-reduce summarization & title generation
│   ├── extractor.py       # Action items, key decisions & questions extraction
│   ├── rag_engine.py      # Transcript-grounded RAG query pipeline
│   └── vector_store.py    # Session-isolated ChromaDB vector storage
│
└── utils/                 # Audio & Media Utilities
    └── audio_processor.py # yt-dlp downloader, FFmpeg converter & chunking
```

---

## 📄 License

This project is licensed under the MIT License.
