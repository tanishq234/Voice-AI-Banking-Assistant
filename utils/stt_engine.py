"""
STT Engine — SpeechRecognition (Google Speech API)
Converts audio bytes / UploadedFile to text.
"""
import io
import os
import tempfile


def transcribe_audio(audio_file) -> str:
    """
    Transcribe audio from a Streamlit UploadedFile or BytesIO object.
    Uses SpeechRecognition with Google Web Speech API (free tier).
    Falls back gracefully if recognition fails.
    """
    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()

        if hasattr(audio_file, "read"):
            audio_bytes = audio_file.read()
            if hasattr(audio_file, "seek"):
                audio_file.seek(0)
        elif isinstance(audio_file, (bytes, bytearray)):
            audio_bytes = bytes(audio_file)
        else:
            audio_bytes = bytes(audio_file)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            with sr.AudioFile(tmp_path) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data, language="en-US")
            return text.strip()

        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"[STT RequestError] {e}")
            return ""
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass

    except ImportError:
        print("[STT] SpeechRecognition not installed")
        return ""
    except Exception as e:
        print(f"[STT Error] {e}")
        return ""
