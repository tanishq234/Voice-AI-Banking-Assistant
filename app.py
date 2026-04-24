"""
Kentiq AI Voice Banking Assistant — Dubai Bank
Full Streamlit Application satisfying all SOW requirements.
"""
import os, time, re
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

from utils.tts_engine      import get_tts_html
from utils.intent_engine   import detect_intent
from utils.cheque_validator import validate_cheque_image
from utils.dummy_data      import ACCOUNT_DATA, generate_txn_id

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kentiq AI Voice Bot – Dubai Bank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

:root {
  --gold:#C9A84C; --gold-l:#E8C97A; --gold-d:#7A6030;
  --navy:#0A1628; --navy-m:#0F2040; --navy-l:#162848;
  --teal:#00C9C8; --teal-d:#007F7E;
  --red:#E8453C; --green:#2ECC8F;
  --white:#F4F1EB; --grey:#8899AA;
}
html,body,[class*="css"]{font-family:'Syne',sans-serif!important;background:var(--navy)!important;color:var(--white)!important;}
.stApp{background:var(--navy)!important;}
.block-container{padding:0.8rem 1.2rem 0.5rem!important;max-width:1200px;}
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important;}

/* ── HEADER ── */
.kb-header{display:flex;align-items:center;justify-content:space-between;
  padding:14px 22px;border-bottom:1px solid rgba(201,168,76,.25);
  background:rgba(15,32,64,.85);backdrop-filter:blur(12px);
  border-radius:16px;margin-bottom:16px;}
.kb-logo{display:flex;align-items:center;gap:13px;}
.kb-icon{width:46px;height:46px;border-radius:13px;
  background:linear-gradient(135deg,#162848,#0F2040);
  border:1.5px solid #7A6030;display:flex;align-items:center;
  justify-content:center;font-size:22px;box-shadow:0 0 18px rgba(201,168,76,.2);}
.kb-brand{font-size:17px;font-weight:800;color:var(--gold);letter-spacing:.04em;}
.kb-sub{font-size:10px;font-family:'IBM Plex Mono',monospace;color:var(--grey);letter-spacing:.1em;text-transform:uppercase;}
.kb-status{display:flex;align-items:center;gap:7px;padding:5px 13px;
  border-radius:20px;background:rgba(46,204,143,.1);border:1px solid rgba(46,204,143,.3);
  font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--green);}
.s-dot{width:7px;height:7px;border-radius:50%;background:var(--green);animation:pd 2s infinite;}
@keyframes pd{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.4)}}

/* ── SECTION TITLES ── */
.sec-title{font-size:13px;font-weight:700;color:var(--gold);letter-spacing:.06em;
  text-transform:uppercase;font-family:'IBM Plex Mono',monospace;
  border-left:3px solid var(--gold);padding-left:10px;margin-bottom:10px;}

/* ── CHAT ── */
.chat-wrap{height:400px;overflow-y:auto;padding:4px 2px;margin-bottom:6px;}
.chat-wrap::-webkit-scrollbar{width:3px;}
.chat-wrap::-webkit-scrollbar-thumb{background:var(--gold-d);border-radius:3px;}
.msg{display:flex;gap:9px;margin-bottom:10px;animation:mi .28s ease;}
@keyframes mi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg.user{flex-direction:row-reverse;}
.av{width:32px;height:32px;border-radius:9px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:14px;}
.msg.bot  .av{background:linear-gradient(135deg,#162848,#0F2040);border:1px solid #7A6030;}
.msg.user .av{background:linear-gradient(135deg,#007F7E,#005A5A);border:1px solid #007F7E;}
.bub{padding:10px 14px;border-radius:13px;font-size:13.5px;line-height:1.6;max-width:78%;}
.msg.bot  .bub{background:var(--navy-l);border:1px solid rgba(201,168,76,.14);border-bottom-left-radius:4px;}
.msg.user .bub{background:linear-gradient(135deg,#007F7E,#005050);border-bottom-right-radius:4px;}
.ts{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--grey);margin-top:3px;}
.msg.user .ts{text-align:right;}

/* ── CARDS ── */
.bal-card{background:linear-gradient(135deg,#0F2040,#162848);
  border:1px solid rgba(201,168,76,.35);border-radius:15px;padding:16px 20px;margin:7px 0;}
.bal-lbl{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--grey);text-transform:uppercase;letter-spacing:.1em;}
.bal-amt{font-size:28px;font-weight:800;color:var(--gold-l);margin:4px 0 2px;}
.bal-acct{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--grey);}
.txn-card{background:var(--navy-l);border:1px solid rgba(0,201,200,.25);
  border-radius:13px;padding:12px 16px;margin:7px 0;
  font-family:'IBM Plex Mono',monospace;font-size:12px;line-height:1.85;}
.txn-lbl{color:var(--grey);font-size:10px;text-transform:uppercase;letter-spacing:.07em;}
.txn-val{color:var(--teal);}
.txn-amt{color:var(--gold-l);font-size:17px;font-weight:600;}
.ok-banner{background:rgba(46,204,143,.12);border:1px solid rgba(46,204,143,.32);
  border-radius:11px;padding:10px 14px;color:var(--green);font-size:13px;margin:5px 0;}
.err-banner{background:rgba(232,69,60,.1);border:1px solid rgba(232,69,60,.32);
  border-radius:11px;padding:10px 14px;color:var(--red);font-size:13px;margin:5px 0;}

/* ── VOICE ORB ── */
.orb-wrap{display:flex;flex-direction:column;align-items:center;gap:5px;padding:8px 0;}
.orb{width:70px;height:70px;border-radius:50%;
  background:radial-gradient(circle at 35% 35%,#162848,#0A1628);
  border:2px solid #7A6030;display:flex;align-items:center;
  justify-content:center;font-size:27px;}
.orb-lbl{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--grey);
  letter-spacing:.09em;text-transform:uppercase;}

/* ── INPUT ── */
.stTextInput>div>div>input{
  background:#162848!important;border:1px solid rgba(201,168,76,.2)!important;
  border-radius:11px!important;color:#F4F1EB!important;
  font-family:'Syne',sans-serif!important;font-size:13.5px!important;padding:10px 14px!important;}
.stTextInput>div>div>input:focus{border-color:#7A6030!important;box-shadow:none!important;}
.stTextInput>div>div>input::placeholder{color:#8899AA!important;}
.stTextInput label{display:none!important;}

/* ── BUTTONS ── */
.stButton>button{
  background:linear-gradient(135deg,#7A6030,#C9A84C)!important;
  color:#0A1628!important;border:none!important;border-radius:11px!important;
  font-family:'Syne',sans-serif!important;font-weight:700!important;
  font-size:13px!important;padding:9px 18px!important;width:100%!important;
  transition:opacity .2s!important;}
.stButton>button:hover{opacity:.82!important;}

/* ── UPLOAD ── */
[data-testid="stFileUploader"]{
  border:2px dashed #7A6030!important;border-radius:13px!important;
  background:rgba(201,168,76,.03)!important;padding:8px!important;}
[data-testid="stFileUploader"]:hover{border-color:#C9A84C!important;}
[data-testid="stFileUploader"] label{color:var(--grey)!important;font-size:12px!important;}

/* ── AUDIO RECORDER ── */
[data-testid="stAudioInput"]{
  background:rgba(0,201,200,.05)!important;
  border:1px solid rgba(0,201,200,.25)!important;
  border-radius:13px!important;padding:8px!important;}
[data-testid="stAudioInput"] label{color:var(--teal)!important;font-size:12px!important;}

/* ── DIVIDER ── */
hr{border-color:rgba(201,168,76,.12)!important;margin:8px 0!important;}

/* ── ACCT PANEL ── */
.acct-panel{background:#162848;border:1px solid rgba(201,168,76,.2);
  border-radius:12px;padding:13px 15px;
  font-family:'IBM Plex Mono',monospace;font-size:12px;}
.acct-name{color:var(--gold-l);font-weight:600;font-size:13.5px;margin-bottom:4px;}
.acct-num{color:var(--grey);}
.acct-bal{color:var(--teal);margin-top:3px;font-size:13px;}

/* ── FLOW BAR ── */
.flow-bar{background:rgba(0,201,200,.08);border:1px solid rgba(0,201,200,.25);
  border-radius:9px;padding:7px 14px;font-family:'IBM Plex Mono',monospace;
  font-size:11px;color:var(--teal);text-align:center;margin-top:6px;}

/* ── STEP ── */
.step-row{display:flex;align-items:center;gap:6px;margin-bottom:6px;
  font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--teal);}
.step-dot{width:20px;height:20px;border-radius:50%;background:rgba(0,201,200,.15);
  border:1px solid #007F7E;display:inline-flex;align-items:center;
  justify-content:center;font-size:10px;font-weight:600;color:var(--teal);}

/* ── SPINNER ── */
.stSpinner>div{border-top-color:var(--gold)!important;}

/* ── SELECTBOX ── */
.stSelectbox>div>div{background:#162848!important;border-color:rgba(201,168,76,.2)!important;color:var(--white)!important;}

/* ── EXPANDER ── */
.streamlit-expanderHeader{background:#162848!important;color:var(--gold-l)!important;border-radius:10px!important;}
</style>
""", unsafe_allow_html=True)

DEFAULTS = dict(
    messages=[],
    flow=None,
    flow_step=0,
    transfer_data={},
    welcome_done=False,
    speak_queue=[],      
    audio_key=0,         
)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def now_str():
    return datetime.now().strftime("%I:%M %p")

def add_msg(role: str, text: str, html: str = "", card: str = ""):
    st.session_state.messages.append({
        "role": role,
        "text": text,
        "html": html or text,
        "card": card,
        "time": now_str(),
    })

def bot_say(text: str, html: str = "", card: str = ""):
    """Add bot message and queue TTS."""
    add_msg("bot", text, html, card)
    st.session_state.speak_queue.append(text)
    st.session_state.audio_key += 1

def render_chat():
    parts = []
    for m in st.session_state.messages:
        av = "🤖" if m["role"] == "bot" else "👤"
        parts.append(f"""
        <div class="msg {m['role']}">
          <div class="av">{av}</div>
          <div>
            <div class="bub">{m['html']}{m['card']}</div>
            <div class="ts">{m['time']}</div>
          </div>
        </div>""")
    html = (
        '<div class="chat-wrap" id="cw">' +
        "".join(parts) +
        '</div><script>var c=document.getElementById("cw");if(c)c.scrollTop=c.scrollHeight;</script>'
    )
    st.markdown(html, unsafe_allow_html=True)

def play_tts():
    """Inject browser TTS for all queued texts."""
    if not st.session_state.speak_queue:
        return
    text = " ... ".join(st.session_state.speak_queue)
    st.session_state.speak_queue = []
    safe = text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    components.html(f"""
    <script>
    (function(){{
        if(!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        var u=new SpeechSynthesisUtterance('{safe}');
        u.rate=0.93; u.pitch=1.05; u.volume=1; u.lang='en-US';
        function go(){{
            var vs=window.speechSynthesis.getVoices();
            var v=vs.find(function(x){{return /Google.*English|Samantha|Karen|Daniel|Moira|Zira/i.test(x.name);}});
            if(v) u.voice=v;
            window.speechSynthesis.speak(u);
        }}
        if(window.speechSynthesis.getVoices().length>0){{go();}}
        else{{window.speechSynthesis.onvoiceschanged=go;}}
    }})();
    </script>""", height=0)

def show_balance():
    a = ACCOUNT_DATA
    card = f"""
    <div class="bal-card">
      <div class="bal-lbl">Available Balance</div>
      <div class="bal-amt">{a['balance']}</div>
      <div class="bal-acct">Account: {a['masked_number']} &nbsp;·&nbsp; {a['name']}</div>
    </div>"""
    bot_say(
        f"Your current account balance is {a['balance']} "
        f"for the account ending in {a['last4']}.",
        html="Here is your current account balance:",
        card=card,
    )

STEPS = [
    ("beneficiary", "Please tell me the beneficiary's full name."),
    ("bank",        "Which bank should the transfer go to?"),
    ("account",     "Please provide the beneficiary's account number."),
    ("amount",      "How much would you like to transfer? Please state the amount in AED."),
]

def start_transfer():
    st.session_state.flow      = "transfer"
    st.session_state.flow_step = 0
    st.session_state.transfer_data = {}
    bot_say("Sure! Let me set up your money transfer. " + STEPS[0][1])

def handle_transfer(t: str):
    idx = st.session_state.flow_step
    key, _ = STEPS[idx]
    st.session_state.transfer_data[key] = t
    st.session_state.flow_step += 1

    if st.session_state.flow_step < len(STEPS):
        bot_say(STEPS[st.session_state.flow_step][1])
    else:
        st.session_state.flow = "transfer_confirm"
        d  = st.session_state.transfer_data
        mk = _mask_acct(d["account"])
        am = _fmt_amount(d["amount"])
        card = f"""
        <div class="txn-card">
          <div><span class="txn-lbl">Beneficiary</span><br/><span class="txn-val">{d['beneficiary']}</span></div>
          <div><span class="txn-lbl">Bank</span><br/><span class="txn-val">{d['bank']}</span></div>
          <div><span class="txn-lbl">Account</span><br/><span class="txn-val">{mk}</span></div>
          <div><span class="txn-lbl">Amount</span><br/><span class="txn-amt">{am}</span></div>
        </div>"""
        bot_say(
            f"Please confirm: transfer of {am} to {d['beneficiary']} "
            f"at {d['bank']}. Say Yes to confirm or No to cancel.",
            html="Please review the transfer details. Say <strong>Yes</strong> to confirm or <strong>No</strong> to cancel.",
            card=card,
        )

def handle_transfer_confirm(t: str):
    if re.search(r'\b(yes|yeah|yep|confirm|ok|okay|sure|proceed|go ahead|correct|affirmative)\b', t, re.I):
        st.session_state.flow = None
        d = st.session_state.transfer_data
        txn = generate_txn_id()
        banner = f'<div class="ok-banner">✅ Transfer successful! &nbsp; Transaction ID: <strong>#{txn}</strong></div>'
        bot_say(
            f"Your transfer to {d['beneficiary']} at {d['bank']} "
            f"has been processed successfully. Transaction ID: {txn}. "
            "Thank you for banking with Dubai Bank.",
            html="Transfer completed successfully!",
            card=banner,
        )
        st.session_state.transfer_data = {}
    elif re.search(r'\b(no|nope|cancel|stop|abort)\b', t, re.I):
        st.session_state.flow = None
        st.session_state.transfer_data = {}
        bot_say("Transfer cancelled. Your account has not been charged. Is there anything else I can help you with?")
    else:
        bot_say("Please say Yes to confirm the transfer, or No to cancel.")

def _mask_acct(raw: str) -> str:
    digits = re.sub(r'\D', '', raw)
    return ("**** **** " + digits[-4:]) if len(digits) >= 4 else ("**** " + raw)

def _fmt_amount(raw: str) -> str:
    m = re.search(r'[\d,]+(?:\.\d{1,2})?', raw)
    if m:
        try:
            return f"AED {float(m.group().replace(',','')): ,.2f}".replace(" ", "")
        except Exception:
            pass
    return "AED " + raw

def start_cheque():
    st.session_state.flow = "cheque"
    bot_say("Sure! Please upload your cheque image using the uploader in the right panel.")

def handle_cheque_text(t: str):
    if re.search(r'\b(cancel|stop|no)\b', t, re.I):
        st.session_state.flow = None
        bot_say("Cheque verification cancelled. How else can I help you?")
    else:
        bot_say("Please upload your cheque image in the right panel, or say Cancel to abort.")

def start_kyc():
    st.session_state.flow = "kyc"
    bot_say(
        "Starting KYC verification. Please upload your photo ID or selfie "
        "in the right panel. Say Cancel anytime to abort."
    )

def handle_kyc_text(t: str):
    if re.search(r'\b(cancel|stop|no)\b', t, re.I):
        st.session_state.flow = None
        bot_say("KYC cancelled. You can restart anytime by saying Start KYC.")
    else:
        bot_say("Please upload your ID photo in the right panel to complete KYC, or say Cancel.")

def show_help():
    html = (
        "Here is what I can do for you:<br/><br/>"
        "💰 <strong>Balance Inquiry</strong> — Say: <em>What's my balance</em><br/>"
        "💸 <strong>Money Transfer</strong> — Say: <em>Transfer money</em><br/>"
        "📄 <strong>Cheque Verification</strong> — Say: <em>Upload cheque</em> or <em>Scan cheque</em><br/>"
        "🪪 <strong>KYC Verification</strong> — Say: <em>Start KYC</em><br/><br/>"
        "Tap the mic 🎤 to speak or type in the box below."
    )
    bot_say(
        "I can help with account balance, money transfer, cheque verification, and KYC. "
        "Use the microphone to speak or type your request.",
        html=html,
    )

def process_input(raw: str):
    t = raw.strip()
    if not t:
        return
    add_msg("user", t)

    if st.session_state.flow == "transfer":
        handle_transfer(t)
        return
    if st.session_state.flow == "transfer_confirm":
        handle_transfer_confirm(t)
        return
    if st.session_state.flow == "cheque":
        handle_cheque_text(t)
        return
    if st.session_state.flow == "kyc":
        handle_kyc_text(t)
        return

    intent = detect_intent(t)
    dispatch = {
        "greeting": lambda: bot_say(
            "Hello! I'm Kentiq AI, your Dubai Bank voice assistant. "
            "I can help with account balance, money transfer, cheque verification, or KYC. "
            "What would you like to do?"
        ),
        "balance":  show_balance,
        "transfer": start_transfer,
        "cheque":   start_cheque,
        "kyc":      start_kyc,
        "help":     show_help,
    }
    if intent in dispatch:
        dispatch[intent]()
    else:
        bot_say(
            "Sorry, I didn't understand that. Please repeat. "
            "You can say: Balance, Transfer money, Upload cheque, Start KYC, or Help."
        )

if not st.session_state.welcome_done:
    WELCOME = "Welcome to Kentiq AI Voice Bot from Dubai Bank Bank. How can I help you?"
    bot_say(WELCOME)
    st.session_state.welcome_done = True

st.markdown("""
<div class="kb-header">
  <div class="kb-logo">
    <div class="kb-icon">🏦</div>
    <div>
      <div class="kb-brand">KENTIQ AI</div>
      <div class="kb-sub">Dubai Bank · Voice Assistant</div>
    </div>
  </div>
  <div class="kb-status"><span class="s-dot"></span>ONLINE</div>
</div>""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2], gap="medium")


with col_left:
    st.markdown('<div class="sec-title">💬 Conversation</div>', unsafe_allow_html=True)
    render_chat()

    play_tts()

    st.markdown("<hr/>", unsafe_allow_html=True)

    with st.form("input_form", clear_on_submit=True, border=False):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_text = st.text_input(
                "msg",
                placeholder="Type here or use voice input →",
                label_visibility="collapsed",
            )
        with c2:
            submitted = st.form_submit_button("Send ➤")
        if submitted and user_text.strip():
            process_input(user_text)
            st.rerun()

    st.markdown('<div class="sec-title" style="margin-top:8px;">⚡ Quick Actions</div>', unsafe_allow_html=True)
    ca, cb, cc, cd, ce = st.columns(5)
    with ca:
        if st.button("💰\nBalance"):
            add_msg("user", "Check my balance")
            show_balance()
            st.rerun()
    with cb:
        if st.button("💸\nTransfer"):
            add_msg("user", "Transfer money")
            start_transfer()
            st.rerun()
    with cc:
        if st.button("📄\nCheque"):
            add_msg("user", "Upload cheque")
            start_cheque()
            st.rerun()
    with cd:
        if st.button("🪪\nKYC"):
            add_msg("user", "Start KYC")
            start_kyc()
            st.rerun()
    with ce:
        if st.button("❓\nHelp"):
            add_msg("user", "Help")
            show_help()
            st.rerun()

    if st.session_state.flow:
        labels = {
            "transfer":         f"💸 Money Transfer — collecting step {st.session_state.flow_step + 1} of {len(STEPS)}",
            "transfer_confirm": "💸 Money Transfer — awaiting confirmation (Yes / No)",
            "cheque":           "📄 Cheque Verification — awaiting upload in right panel",
            "kyc":              "🪪 KYC Verification — awaiting photo in right panel",
        }
        lbl = labels.get(st.session_state.flow, f"⚙️ Active: {st.session_state.flow}")
        st.markdown(f'<div class="flow-bar">{lbl}</div>', unsafe_allow_html=True)

with col_right:

    st.markdown('<div class="sec-title">🎙️ Voice Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="orb-wrap"><div class="orb">🎤</div><div class="orb-lbl">Microphone</div></div>', unsafe_allow_html=True)

    audio_value = st.audio_input(
        "🎤 Click the mic button to speak",
        key="voice_input",
        label_visibility="visible",
    )
    if audio_value is not None:
        from utils.stt_engine import transcribe_audio
        with st.spinner("🔄 Recognising speech…"):
            transcript = transcribe_audio(audio_value)
        if transcript:
            st.markdown(
                f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:12px;'
                f'color:#00C9C8;text-align:center;padding:4px;">Heard: "{transcript}"</div>',
                unsafe_allow_html=True,
            )
            process_input(transcript)
            st.rerun()
        else:
            st.markdown(
                '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:12px;'
                'color:#E8453C;text-align:center;padding:4px;">'
                'Sorry, I didn\'t understand that. Please repeat.</div>',
                unsafe_allow_html=True,
            )
            bot_say("Sorry, I didn't understand that. Please repeat.")
            st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">👤 Account</div>', unsafe_allow_html=True)
    a = ACCOUNT_DATA
    st.markdown(f"""
    <div class="acct-panel">
      <div class="acct-name">{a['name']}</div>
      <div class="acct-num">{a['masked_number']}</div>
      <div class="acct-bal">{a['balance']}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    is_cheque = st.session_state.flow in ("cheque", None)
    with st.expander("📄 Cheque Verification", expanded=(st.session_state.flow == "cheque")):
        st.markdown('<div class="step-row"><div class="step-dot">1</div>Upload cheque image (JPG / PNG / PDF)</div>', unsafe_allow_html=True)
        cheque_file = st.file_uploader(
            "Upload cheque",
            type=["jpg", "jpeg", "png", "pdf"],
            key="cheque_upload",
            label_visibility="collapsed",
        )
        if cheque_file:
            if cheque_file.type.startswith("image/"):
                st.image(cheque_file, caption="Uploaded Image", use_column_width=True)
            with st.spinner("🔍 Validating cheque…"):
                ok, reason = validate_cheque_image(cheque_file)
                time.sleep(0.8)

            if ok:
                ref = generate_txn_id("CHQ")
                banner = f'<div class="ok-banner">✅ Cheque validated! Reference: <strong>#{ref}</strong></div>'
                add_msg("user", "[Uploaded cheque image]")
                bot_say(
                    f"Cheque verified successfully. Reference number {ref} assigned.",
                    html="Cheque image received and validated.",
                    card=banner,
                )
            else:
                banner = f'<div class="err-banner">❌ Invalid: {reason}</div>'
                add_msg("user", "[Uploaded cheque image]")
                bot_say(
                    f"Sorry, the uploaded image could not be verified as a valid cheque. {reason}. "
                    "Please upload a clear photo of the cheque.",
                    html="Cheque validation failed.",
                    card=banner,
                )

            st.session_state.flow = None
            st.rerun()

        if st.session_state.flow == "cheque":
            if st.button("✖ Cancel Cheque Verification", key="cancel_cheque"):
                st.session_state.flow = None
                add_msg("user", "Cancel cheque verification")
                bot_say("Cheque verification cancelled. How else can I help you?")
                st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    with st.expander("🪪 KYC Verification", expanded=(st.session_state.flow == "kyc")):
        st.markdown('<div class="step-row"><div class="step-dot">1</div>Upload photo ID or selfie</div>', unsafe_allow_html=True)
        kyc_file = st.file_uploader(
            "Upload KYC photo",
            type=["jpg", "jpeg", "png"],
            key="kyc_upload",
            label_visibility="collapsed",
        )
        if kyc_file:
            st.image(kyc_file, caption="KYC Photo", width=200)

            save_dir = "recordings"
            os.makedirs(save_dir, exist_ok=True)
            ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"KYC_{ts}_{kyc_file.name}"
            fpath = os.path.join(save_dir, fname)
            with open(fpath, "wb") as f:
                f.write(kyc_file.getvalue())

            banner = f'<div class="ok-banner">✅ KYC submitted! File saved: <strong>{fname}</strong>. Under review.</div>'
            add_msg("user", "[Uploaded KYC photo]")
            bot_say(
                f"KYC verification completed successfully. Your identity photo "
                f"has been saved and submitted for review. Thank you for using Dubai Bank.",
                html="KYC recording completed and submitted.",
                card=banner,
            )
            st.session_state.flow = None
            st.rerun()

        st.markdown('<div class="step-row"><div class="step-dot">2</div>Optional: record voice for KYC</div>', unsafe_allow_html=True)
        kyc_voice = st.audio_input("🎤 Record voice KYC clip", key="kyc_voice", label_visibility="visible")
        if kyc_voice is not None:
            save_dir = "recordings"
            os.makedirs(save_dir, exist_ok=True)
            ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
            vname = f"KYC_voice_{ts}.wav"
            vpath = os.path.join(save_dir, vname)
            with open(vpath, "wb") as f:
                f.write(kyc_voice.getvalue())
            st.markdown(
                f'<div class="ok-banner" style="font-size:12px;">🎙️ Voice clip saved: {vname}</div>',
                unsafe_allow_html=True,
            )

        if st.session_state.flow == "kyc":
            if st.button("✖ Cancel KYC", key="cancel_kyc"):
                st.session_state.flow = None
                add_msg("user", "Cancel KYC")
                bot_say("KYC cancelled. You can restart anytime by saying Start KYC.")
                st.rerun()
