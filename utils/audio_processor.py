import os
import re
import tempfile
import yt_dlp
from pydub import AudioSegment

YOUTUBE_URL_REGEX = re.compile(
    r'^(https?://)?(www\.|m\.)?(youtube\.com/(watch\?v=|embed/|v/|shorts/)|youtu\.be/)[\w\-]+'
)

def is_valid_youtube_url(url: str) -> bool:
    """Validate if the string is a recognized YouTube URL format."""
    if not url or not isinstance(url, str):
        return False
    return bool(YOUTUBE_URL_REGEX.search(url.strip()))

def download_youtube_audio(url: str, output_dir: str = None) -> str:
    """
    Downloads audio from YouTube and converts it to WAV format.
    Stores audio in the provided output_dir or an isolated temporary directory.
    """
    url_clean = url.strip()
    if not is_valid_youtube_url(url_clean):
        raise ValueError(
            "Invalid or unsupported YouTube URL format. "
            "Please provide a valid YouTube link (e.g. https://www.youtube.com/watch?v=... or https://youtu.be/...)."
        )

    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="ytdl_")
    os.makedirs(output_dir, exist_ok=True)

    out_template = os.path.join(output_dir, "audio.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_clean])
    except yt_dlp.utils.DownloadError as e:
        raise RuntimeError(
            f"Failed to download YouTube audio. The video may be private, age-restricted, "
            f"unavailable, or geoblocked. Details: {str(e)}"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while downloading YouTube audio: {str(e)}") from e

    expected_wav = os.path.join(output_dir, "audio.wav")
    if os.path.exists(expected_wav):
        return expected_wav

    # Fallback search in output_dir for any .wav produced
    wav_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".wav")]
    if wav_files:
        return wav_files[0]

    raise FileNotFoundError("Audio extraction completed, but no WAV file was found in output directory.")

def convert_to_wav(input_path: str, output_dir: str = None) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Local file not found: '{input_path}'. In cloud deployment, use a YouTube URL.")

    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="wav_convert_")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_converted.wav")

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # 16kHz mono
    audio.export(output_path, format="wav")
    return output_path

def chunk_audio(wav_path: str, chunk_minutes: int = 10, output_dir: str = None) -> list:
    """Split audio into manageable chunks for transcription."""
    if not os.path.isfile(wav_path):
        raise FileNotFoundError(f"WAV file not found for chunking: {wav_path}")

    if output_dir is None:
        output_dir = os.path.dirname(wav_path)
    os.makedirs(output_dir, exist_ok=True)

    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []
    base_name = os.path.splitext(os.path.basename(wav_path))[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = os.path.join(output_dir, f"{base_name}_chunk_{i}.wav")
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks

def process_input(source: str, output_dir: str = None) -> list:
    """Process video/audio source into wav chunks within an isolated directory."""
    source_clean = source.strip()
    if source_clean.startswith("http://") or source_clean.startswith("https://"):
        print("Detected URL. Downloading audio...")
        wav_path = download_youtube_audio(source_clean, output_dir=output_dir)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source_clean, output_dir=output_dir)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path, output_dir=output_dir)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
