# 🏦 Kentiq AI Voice Banking Assistant — Dubai Bank

A fully functional, voice-enabled AI banking assistant built with **Streamlit + Python**, satisfying all requirements from the Avyukta Intellicall Interview Project SOW.

---

## ✅ All SOW Requirements Implemented

| Milestone | Feature | Status |
|-----------|---------|--------|
| M1 | Voice Interface Setup (STT + TTS + Welcome Message) | ✅ |
| M2 | Account Balance Inquiry (voice-triggered) | ✅ |
| M3 | Money Transfer — 4-step voice workflow + confirmation | ✅ |
| M4 | Cheque Upload & Validation (OpenCV + PIL) | ✅ |
| M5 | Voice/Video KYC — audio recording + file save | ✅ |
| M6 | Integration, Error Handling, Edge Cases | ✅ |

---

## 🚀 Run Locally

```bash
# 1. Clone / unzip project
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```
Opens at: http://localhost:8501

> **Browser:** Use **Google Chrome** or **Edge** for best voice support.

---

## ☁️ Deploy Online (Free)

### Option 1 — Streamlit Community Cloud (Official, Recommended)
1. Push this folder to a **public GitHub repo**
2. Go to → https://share.streamlit.io
3. Click **"New app"** → select your repo → set `app.py` as main file
4. Click **Deploy** → live URL in ~2 minutes

### Option 2 — Render.com
1. Push to GitHub
2. Go to https://render.com → New **Web Service**
3. Connect repo → Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.headless true`
4. Deploy → free public URL

### Option 3 — Railway.app
1. Push to GitHub
2. https://railway.app → New Project → Deploy from GitHub
3. Add env var: `PORT=8501`
4. Start Command: `streamlit run app.py --server.port $PORT --server.headless true`

---

## 🏗️ Project Structure

```
kentiq_bot/
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── packages.txt             # System-level packages (for cloud)
├── .streamlit/
│   └── config.toml          # Streamlit theme & server config
├── utils/
│   ├── tts_engine.py        # Text-to-Speech (Web Speech API + gTTS)
│   ├── stt_engine.py        # Speech-to-Text (SpeechRecognition + Google)
│   ├── intent_engine.py     # NLP intent detection (regex-based)
│   ├── cheque_validator.py  # Cheque image validation (OpenCV + PIL)
│   └── dummy_data.py        # Mock account/banking data
└── recordings/              # KYC recordings saved locally here
```

---

## 🔧 Technologies Used (Per SOW)

| Purpose | Technology |
|---------|-----------|
| Frontend UI | Streamlit |
| Text-to-Speech | gTTS + Browser Web Speech API |
| Speech Recognition | Python `SpeechRecognition` (Google Speech API) |
| Image Validation | OpenCV (`opencv-python-headless`) + Pillow |
| NLP / Intent Detection | Regex-based NLP (Python `re`) |
| KYC Recording | `st.audio_input` → saved as .wav locally |

---

## 📊 Evaluation Criteria Coverage

| Criteria | Weight | How Met |
|----------|--------|---------|
| Functional Completion | 40% | All 5 features working end-to-end |
| Milestone Achievement | 25% | All 6 milestones implemented |
| Code Quality | 15% | Modular utils/, clean state machine, typed functions |
| User Experience | 10% | Voice orb, quick chips, flow status bar, animations |
| Documentation | 10% | This README + inline docstrings |

---

## 🔊 How Voice Works

1. **TTS (Output):** Bot responses are spoken automatically using the browser's built-in `speechSynthesis` Web API — no external API key needed.
2. **STT (Input):** Click the microphone button (`st.audio_input`) → records your voice → sent to Google Web Speech API for free transcription.

---

## 💡 Sample Interactions

| You say | Bot does |
|---------|---------|
| "What's my balance?" | Shows account balance card + speaks it |
| "Transfer money" | Starts 4-step voice transfer flow |
| "Upload cheque" | Opens cheque upload panel |
| "Start KYC" | Opens KYC panel for photo + voice recording |
| "Help" | Lists all available commands |
| *(unclear audio)* | "Sorry, I didn't understand that. Please repeat." |

---

*Built for Avyukta Intellicall Interview Project — Kentiq AI Voice Bot, Dubai Bank*
