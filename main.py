import os
import shutil
import tempfile
from dotenv import load_dotenv
from utils.audio_processor import process_input, is_valid_youtube_url
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

def run_pipeline(source: str, language: str = "english") -> dict:
    source_clean = source.strip()
    print("Starting AI Video Assistant pipeline...")

    if source_clean.startswith("http://") or source_clean.startswith("https://"):
        if not is_valid_youtube_url(source_clean):
            raise ValueError(f"Invalid or unsupported YouTube URL: {source_clean}")
    elif not os.path.isfile(source_clean):
        raise FileNotFoundError(f"Local file not found: {source_clean}")

    if not os.getenv("MISTRAL_API_KEY"):
        raise ValueError("MISTRAL_API_KEY environment variable is not set.")

    temp_run_dir = tempfile.mkdtemp(prefix="ai_video_cli_")
    try:
        chunks = process_input(source_clean, output_dir=temp_run_dir)
        transcript = transcribe_all(chunks, language)
    finally:
        if os.path.exists(temp_run_dir):
            shutil.rmtree(temp_run_dir, ignore_errors=True)

    print(f"Raw transcription (first 300 characters): {transcript[:300]}")

    title = generate_title(transcript)
    summary = summarize(transcript)
    action_item = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)
    
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"
    result = run_pipeline(source, language)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['open_questions']}")
    print("=" * 60)

    # Chat with your meeting via RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
    rag_chain = result["rag_chain"]
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue
        answer = ask_question(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")