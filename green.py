API_KEY = "AIzaSyAHyFoZA057NqlaVWw_cEr4LiPjaweIUzY"
import os
import google.generativeai as genai
from PIL import Image
import struct, time, wave, re
from pathlib import Path
from typing import Optional, Callable

from freewili import FreeWili
from freewili.framing import ResponseFrame
from freewili.types import EventType, AudioData

INPUT_WAV = Path("input.wav")

def _device_tts(fw: FreeWili, text: str):
    """Prefer device TTS; fall back to PC TTS."""
    for attr in ("play_audio_text_as_speech", "play_audio_text_to_speech",
                 "play_audio_tts", "text_to_speech"):
        fn = getattr(fw, attr, None)
        if callable(fn):
            try:
                fn(text).expect("Device TTS failed")
                return
            except Exception as e:
                print(f"[Device TTS] {attr} error:", e)
    try:
        import pyttsx3
        eng = pyttsx3.init()
        eng.say(text)
        eng.runAndWait()
    except Exception as e:
        print(f"[PC TTS fallback] {e}\n[TTS text] {text}")

def _record_5s(fw: FreeWili, sr: int = 8000):
    """
    Record exactly 5 seconds of audio events into INPUT_WAV (mono, 16-bit, sr).
    This function runs its own tight loop and returns when done.
    """
    # local state captured by callback
    wav_file: Optional[wave.Wave_write] = None
    is_recording = True

    def on_event(evt_type: EventType, frame: ResponseFrame, data: AudioData):
        if not is_recording:
            return
        if evt_type != EventType.Audio or wav_file is None:
            return
        # pack int16 samples into bytes
        wav_file.writeframes(b"".join(struct.pack("<h", s) for s in data.data))

    # open file and enable audio events
    wav_file = wave.open(str(INPUT_WAV), "wb")
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sr)

    fw.set_event_callback(on_event)
    fw.enable_audio_events(True).expect("Failed to enable audio events")
    print(f"Recording 5s to {INPUT_WAV} …")

    start = time.time()
    try:
        while time.time() - start < 5.0:
            fw.process_events()
            time.sleep(0.005)
    finally:
        # stop and close
        is_recording = False  # noqa: F841 (used by closure)
        fw.enable_audio_events(False).expect("Failed to disable audio events")
        wav_file.close()
        print(f"Saved: {INPUT_WAV}")

# stt_google.py
import speech_recognition as sr
from pathlib import Path

def transcribe_wav(wav_path: Path) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(str(wav_path)) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="en-US")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"[Error contacting Google] {e}"

def handle_green(fw: FreeWili):
    # --- Securely Configure your API Key ---
    # Make sure you have set your GOOGLE_API_KEY environment variable.
    """
    BLUE workflow:
      - TTS prompt
      - record 5s to input.wav
      - STT -> LLM -> TTS of answer only (logs stripped)
    """
    # Prompt first
    _device_tts(fw, "How can I help you?")
    time.sleep(0.25)  # small gap so prompt isn’t captured

    # Record 5s (blocks this call; main loop should not poll buttons during this)
    _record_5s(fw)

    try:
        # This function now correctly exists after your library update
        genai.configure(api_key=API_KEY)
    except KeyError:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        exit()
    # ------------------------------------

    # Load the image using the PIL library
    try:
        img = Image.open('tp.jpg')
    except FileNotFoundError:
        print("Error: 'tp.jpg' not found in the current directory.")
        exit()

    # CORRECT WAY: Instantiate the specific model you want to use
    model = genai.GenerativeModel('gemini-2.5-flash')

    print("🖼️  Sending image for captioning...")
    text = transcribe_wav(INPUT_WAV)

    # Generate content directly from the model instance
    response = model.generate_content([text, img])

    print("\n📝 Response:")
    print(response.text)
    _device_tts(fw, response.text or "Sorry, I could not get a response.")


if __name__ == "__main__":
    with FreeWili.find_first().expect("Failed to find a FreeWili device") as fw:
        print(f"✅ Successfully connected to {fw}")
        handle_green(fw)