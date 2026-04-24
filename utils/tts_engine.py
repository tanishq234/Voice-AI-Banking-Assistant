"""
TTS Engine
Primary:  Browser Web Speech API (injected via HTML script tag)
Fallback:  gTTS → base64 MP3 autoplay
"""
import base64
import io


def text_to_audio_b64(text: str) -> str:
    """Convert text to base64 MP3 using gTTS. Returns empty string on failure."""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en", slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")
    except Exception:
        return ""


def get_tts_html(text: str) -> str:
    """
    Return HTML that plays text via browser SpeechSynthesis API.
    Works 100% offline in any modern browser — no external API needed.
    """
    safe = (text
            .replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace('"', '\\"')
            .replace("\n", " "))
    return f"""
    <script>
    (function() {{
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance('{safe}');
        u.rate = 0.93; u.pitch = 1.05; u.volume = 1; u.lang = 'en-US';
        function setVoice() {{
            var voices = window.speechSynthesis.getVoices();
            var v = voices.find(function(x) {{
                return /Google.*English|Samantha|Karen|Daniel|Moira|Zira/i.test(x.name);
            }});
            if (v) u.voice = v;
            window.speechSynthesis.speak(u);
        }}
        if (window.speechSynthesis.getVoices().length > 0) {{
            setVoice();
        }} else {{
            window.speechSynthesis.onvoiceschanged = setVoice;
        }}
    }})();
    </script>"""


def speak_text(text: str, save_path: str = None):
    """Save TTS audio to file using gTTS (for KYC/recording flows)."""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en", slow=False)
        if save_path:
            tts.save(save_path)
            return save_path
    except Exception as e:
        print(f"[TTS save error] {e}")
    return None
