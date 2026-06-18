import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile


left, center, right = st.columns([1.3, 1, 1])

with center:
    st.image(
        "https://th.bing.com/th/id/OIP.j7zMGAA0gMrYGTu5Nco1gAHaHa?w=185&h=185&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",
        width=150
    )
# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

/* App Background */
.stApp{
    background: linear-gradient(135deg,#667eea,#764ba2,#6dd5ed);
    background-size:400% 400%;
}

/* Main Container */
.block-container{
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(18px);
    border-radius:25px;
    padding:2rem;
    margin-top:20px;
    box-shadow:0 8px 32px rgba(31,38,135,0.37);
}

/* Buttons */
.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#4F46E5,#06B6D4);
    color:white;
    border:none;
    border-radius:12px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    transform:scale(1.03);
    transition:0.3s;
}

/* Download Button */
.stDownloadButton>button{
    width:100%;
    background:#10B981;
    color:white;
    border:none;
    border-radius:12px;
    height:45px;
}

/* Text Areas */
textarea{
    background:rgba(255,255,255,0.15)!important;
    color:white!important;
    border-radius:12px!important;
}

/* Selectbox */
div[data-baseweb="select"]{
    background:rgba(255,255,255,0.15);
    border-radius:12px;
}

/* Metrics */
div[data-testid="metric-container"]{
    background:rgba(255,255,255,0.15);
    border-radius:15px;
    padding:15px;
    box-shadow:0 4px 20px rgba(0,0,0,0.2);
}

/* Expander */
.streamlit-expanderHeader{
    font-size:18px;
    font-weight:bold;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:rgba(255,255,255,0.15);
    backdrop-filter:blur(15px);
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🌍 AI Translator")
st.sidebar.success("✅ Ready to Translate")

st.sidebar.markdown("""
### 🚀 Features

- 🌐 Multi-language Translation
- 🔄 Swap Languages
- 🔊 Text-to-Speech
- 📥 Download Translation
- 🕒 Translation History
- 📊 Translation Statistics

---
Developed for **CodeAlpha AI Internship**
""")

# ---------------- HEADER ---------------- #
st.markdown("""
<div style="
background:rgba(255,255,255,0.18);
backdrop-filter:blur(18px);
padding:35px;
border-radius:25px;
text-align:center;
box-shadow:0 8px 32px rgba(31,38,135,0.37);
">

<h1 style="
color:white;
font-size:48px;
margin-bottom:10px;
">
🌍 AI Language Translator
</h1>

<p style="
color:white;
font-size:20px;
">
Translate text into 100+ languages instantly
</p>

</div>
""", unsafe_allow_html=True)

# ---------------- LANGUAGES ---------------- #
languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Urdu": "ur",
    "Odia": "or",

    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Polish": "pl",
    "Turkish": "tr",
    "Greek": "el",
    "Romanian": "ro",
    "Hungarian": "hu",
    "Czech": "cs",
    "Swedish": "sv",
    "Norwegian": "no",
    "Danish": "da",
    "Finnish": "fi",

    "Arabic": "ar",
    "Hebrew": "iw",
    "Persian": "fa",

    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko",
    "Thai": "th",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Malay": "ms",

    "Swahili": "sw",
    "Ukrainian": "uk"
}

# ---------------- SESSION STATE ---------------- #
if "source" not in st.session_state:
    st.session_state.source = "English"

if "target" not in st.session_state:
    st.session_state.target = "Hindi"

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INPUT ---------------- #
text = st.text_area(
    "📝 Enter Text",
    placeholder="Type something here..."
)

st.caption(f"Characters: {len(text)}")

# ---------------- LANGUAGE SELECTION ---------------- #
col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "🌐 Source Language",
        list(languages.keys()),
        index=list(languages.keys()).index(st.session_state.source)
    )

with col2:
    target = st.selectbox(
        "🌎 Target Language",
        list(languages.keys()),
        index=list(languages.keys()).index(st.session_state.target)
    )

st.session_state.source = source
st.session_state.target = target

# ---------------- BUTTONS ---------------- #
c1, c2 = st.columns(2)

with c1:
    swap = st.button("🔄 Swap Languages")

with c2:
    translate = st.button("🚀 Translate")

if swap:
    st.session_state.source, st.session_state.target = (
        st.session_state.target,
        st.session_state.source
    )
    st.rerun()

# ---------------- TRANSLATION ---------------- #
if translate:

    if text.strip() == "":
        st.warning("Please enter some text.")

    else:
        try:

            translated = GoogleTranslator(
                source=languages[source],
                target=languages[target]
            ).translate(text)

            entry = {
                "source": source,
                "target": target,
                "input": text,
                "output": translated
            }

            if (
                not st.session_state.history
                or st.session_state.history[-1] != entry
            ):
                st.session_state.history.append(entry)

            st.subheader("✨ Translated Text")

            st.text_area(
                "Output",
                translated,
                height=150
            )

            st.download_button(
                "📥 Download Translation",
                translated,
                file_name="translation.txt",
                mime="text/plain"
            )

            tts = gTTS(
                text=translated,
                lang=languages[target]
            )

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            ) as fp:
                tts.save(fp.name)

            st.audio(fp.name)

        except Exception as e:
            st.error(f"Translation Error: {e}")

# ---------------- HISTORY ---------------- #
st.markdown("---")
st.subheader("🕒 Translation History")

if st.session_state.history:

    for item in reversed(st.session_state.history):

        with st.expander(
            f"{item['source']} ➜ {item['target']}"
        ):

            st.write("**Input:**")
            st.write(item["input"])

            st.write("**Output:**")
            st.write(item["output"])

else:
    st.info("No translations yet.")

# ---------------- STATISTICS ---------------- #
st.markdown("---")
st.subheader("📊 Translation Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Translations",
        len(st.session_state.history)
    )

with col2:
    total_chars = sum(
        len(item["input"])
        for item in st.session_state.history
    )

    st.metric(
        "Characters",
        total_chars
    )

with col3:
    unique_languages = len(
        set(item["target"] for item in st.session_state.history)
    )

    st.metric(
        "Languages",
        unique_languages
    )

# ---------------- CLEAR HISTORY ---------------- #
if st.button("🗑 Clear History"):
    st.session_state.history.clear()
    st.rerun()

# ---------------- FOOTER ---------------- #
st.markdown("---")

st.markdown("""
<div style='
text-align:center;
padding:20px;
color:white;
'>

<h4>🌍 AI Language Translator</h4>

Made with ❤️ using Streamlit

<br>

<b>Sriharini Guntupalli</b>

<br>

CodeAlpha AI Internship 2026

</div>
""", unsafe_allow_html=True)