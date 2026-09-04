# 🎬 AI Video Assistant

An intelligent meeting analysis tool that transcribes, summarizes, and enables interactive Q&A with video content using advanced AI technologies.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

- **🎤 Multi-Source Audio Processing**: Support for YouTube URLs and local audio/video files
- **🗣️ Advanced Transcription**: 
  - Local Whisper model for English transcription
  - Sarvam AI integration for Hinglish (Hindi-English) content with automatic translation
- **📊 Intelligent Analysis**:
  - Automatic title generation
  - Comprehensive meeting summarization
  - Action items extraction
  - Key decisions identification
  - Open questions tracking
- **💬 Interactive RAG Chat**: Ask questions about your meeting using Retrieval-Augmented Generation
- **🎨 Modern UI**: Beautiful, responsive Streamlit interface with dark mode and custom styling
- **🧠 Powered by AI**: LangChain orchestration with Mistral LLM and ChromaDB vector store

## 🚀 Tech Stack

- **Speech-to-Text**: OpenAI Whisper, Sarvam AI
- **LLM Framework**: LangChain with Mistral AI
- **Vector Store**: ChromaDB with Sentence Transformers embeddings
- **Frontend**: Streamlit with custom CSS
- **Audio Processing**: yt-dlp, pydub, FFmpeg

## 📋 Prerequisites

- Python 3.10 or higher
- FFmpeg (must be installed separately and available in PATH)
- Mistral API Key (for LLM features)
- Sarvam API Key (optional, only for Hinglish transcription)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-Video-Assistant.git
cd AI-Video-Assistant
```

2. **Install FFmpeg**
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

3. **Install Python dependencies**
```bash
pip install -r Requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
# Required for LLM features
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional: for Hinglish transcription
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional: Whisper model size (tiny, base, small, medium, large)
WHISPER_MODEL=small

# Optional: Sarvam model version
SARVAM_STT_MODEL=saaras:v2.5
```

**Get API Keys:**
- Mistral API: [console.mistral.ai](https://console.mistral.ai/)
- Sarvam AI: [sarvam.ai](https://www.sarvam.ai/)

## 🎯 Usage

### Web Interface (Streamlit)

Launch the interactive web application:

```bash
streamlit run app.py
```

Then:
1. Enter a YouTube URL or local file path in the sidebar
2. Select language (English or Hinglish)
3. Click "⚡ Analyse"
4. View transcription, summary, action items, and key insights
5. Chat with your meeting content using the RAG interface

### Command Line Interface

Run the CLI version:

```bash
python main.py
```

Follow the prompts to:
- Enter video source (YouTube URL or file path)
- Select language
- View analysis results
- Interact with the RAG chat interface

## 📂 Project Structure

```
AI-Video-Assistant/
├── app.py                 # Streamlit web interface
├── main.py                # CLI interface
├── Requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
│
├── core/                  # Core processing modules
│   ├── transcriber.py    # Audio transcription (Whisper/Sarvam)
│   ├── summarizer.py     # Text summarization & title generation
│   ├── extractor.py      # Extract action items, decisions, questions
│   ├── rag_engine.py     # RAG pipeline with ChromaDB
│   └── vector_store.py   # Vector store management
│
└── utils/                 # Utility modules
    └── audio_processor.py # Audio extraction and processing
```

## 🔧 Configuration

### Whisper Model Selection

Choose the appropriate model based on your needs:

| Model  | Size  | Speed | Accuracy | VRAM    |
|--------|-------|-------|----------|---------|
| tiny   | 39M   | Fast  | Basic    | ~1GB    |
| base   | 74M   | Fast  | Good     | ~1GB    |
| small  | 244M  | Medium| Better   | ~2GB    |
| medium | 769M  | Slow  | Great    | ~5GB    |
| large  | 1550M | Slower| Best     | ~10GB   |

Set in `.env`: `WHISPER_MODEL=small`

### Language Support

- **English**: Uses local Whisper model for transcription
- **Hinglish**: Uses Sarvam AI for transcription with automatic translation to English

## 🎨 Features Showcase

### Pipeline Stages
1. **Audio Processing**: Extract and prepare audio from various sources
2. **Transcription**: Convert speech to text with high accuracy
3. **Title Generation**: AI-generated descriptive titles
4. **Summarization**: Concise meeting summaries
5. **Extraction**: Automatic identification of action items, decisions, and questions
6. **RAG Engine**: Build searchable knowledge base for interactive Q&A

### RAG Chat Examples
- "What were the main decisions made in this meeting?"
- "List all action items assigned to the team"
- "What questions remain unanswered?"
- "Summarize the discussion about the project timeline"


**⭐ If you find this project useful, please consider giving it a star!**
