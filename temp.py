import os
import speech_recognition as sr
from googletrans import Translator
import google.generativeai as genai
from gtts import gTTS
from playsound import playsound
import time

API_KEY = "AIzaSyAHyFoZA057NqlaVWw_cEr4LiPjaweIUzY"

def autodetect_multilingual_assistant():
    """
    Listens for speech, automatically detects the language, translates it to English,
    gets an answer from Gemini, and speaks the answer in English.
    """
    # 1. --- Configure APIs ---
    try:
        genai.configure(api_key=API_KEY)
    except KeyError:
        print("❌ Error: GOOGLE_API_KEY environment variable not set.")
        return

    recognizer = sr.Recognizer()
    translator = Translator()
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 2. --- Listen for Speech ---
    with sr.Microphone() as source:
        print("\nAdjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening... Speak in any supported language.")

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("⏳ No speech detected. Please try again.")
            return

    # 3. --- Auto-Detect Language and Transcribe using Whisper ---
    print("\n🕵️  Detecting language and transcribing...")
    try:
        # Using recognize_whisper for transcription and language detection
        # The first time you run this, it will download the Whisper model (~461 MB for "base")
        whisper_result = recognizer.recognize_whisper(audio, show_all=True)
        
        detected_language = whisper_result["language"]
        recognized_text = whisper_result["text"]
        
        # Check if any speech was actually transcribed
        if not recognized_text.strip():
            print("❓ Could not understand the audio. The speech was unclear.")
            return

        print(f"✅ Detected Language: {detected_language}")
        print(f"✅ Recognized Text: {recognized_text}")

    except sr.UnknownValueError:
        print("❓ Whisper could not understand the audio. Please try speaking more clearly.")
        return
    except sr.RequestError as e:
        print(f"API error with Whisper: {e}")
        return

    # 4. --- Translate to English ---
    # We only translate if the detected language is not English
    if detected_language != "en":
        print(f"\n🌐 Translating from '{detected_language}' to English...")
        try:
            translated_obj = translator.translate(recognized_text, dest='en')
            english_question = translated_obj.text
            print(f"✅ Translated Question: {english_question}")
        except Exception as e:
            print(f"Translation failed: {e}")
            return
    else:
        english_question = recognized_text

    # 5. --- Get an Answer from Gemini ---
    print("\n🤔 Thinking...")
    try:
        response = model.generate_content(english_question)
        english_answer = response.text
        print(f"🤖 Gemini's Answer: {english_answer}")
    except Exception as e:
        print(f"Failed to get response from Gemini: {e}")
        return

    # 6. --- Speak the English Answer ---
    try:
        print("\n🔊 Speaking answer...")
        tts = gTTS(text=english_answer, lang='en', slow=False)
        response_audio_file = "response.mp3"
        tts.save(response_audio_file)
        playsound(response_audio_file)
        os.remove(response_audio_file)
    except Exception as e:
        print(f"Failed to play audio: {e}")


if __name__ == "__main__":
    autodetect_multilingual_assistant()