import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
from faster_whisper import WhisperModel

# Load Whisper model once (uses CPU, no GPU needed)
print("Loading Whisper model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
print("Whisper ready.")

def record_audio(duration: int = 10, sample_rate: int = 16000) -> str:
    """Record audio from microphone and save to temp file. Returns file path."""
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )
    sd.wait()  # Wait until recording is done
    print("Recording done.")

    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio, sample_rate)
    return tmp.name

def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file to text using Whisper."""
    segments, _ = whisper_model.transcribe(audio_path, language="en")
    text = " ".join(segment.text for segment in segments).strip()
    os.unlink(audio_path)  # Clean up temp file
    return text

def record_and_transcribe(duration: int = 10) -> str:
    """Record audio and return transcribed text."""
    audio_path = record_audio(duration)
    return transcribe_audio(audio_path)