# app.py — Beautiful UI version (logic unchanged)
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load .env for local use
load_dotenv()

# --------------------------
# 🎨 Streamlit Page Config
# --------------------------
st.set_page_config(
    page_title="Groq Llama Translator",
    page_icon="🌐",
    layout="centered"
)

# --------------------------
# 🌈 CUSTOM CSS FOR BEAUTIFUL UI
# --------------------------
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #090a0f, #1f2633);
        color: white;
    }
    .title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #00eaff;
        margin-bottom: 5px;
        text-shadow: 0px 0px 20px rgba(0, 238, 255, 0.8);
    }
    .sub {
        text-align: center;
        color: #b5b5b5;
        margin-top: -10px;
        margin-bottom: 30px;
        font-size: 16px;
    }
    .textbox label {
        color: #e0e0e0 !important;
        font-size: 18px;
    }
    .stTextInput>div>div>input {
        background: #1b1f29;
        color: white;
        border-radius: 8px;
    }
    .output-box {
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        background: #12151c;
        border: 1px solid #00eaff50;
        box-shadow: 0 0 20px rgba(0, 238, 255, 0.2);
    }
    .footer {
        margin-top: 40px;
        text-align: center;
        color: #7a7a7a;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------
# 🚀 Title Section
# --------------------------
st.markdown("<div class='title'>🌐 English → French Translator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Powered by Groq's ultra-fast Llama models ⚡</div>", unsafe_allow_html=True)


# --------------------------
# 🔐 API KEY LOAD
# --------------------------
GROQ_API_KEY = (
    st.secrets.get("GROQ_API_KEY")
    if hasattr(st, "secrets")
    else None
) or os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY. Add it in Streamlit Secrets.")
else:
    client = Groq(api_key=GROQ_API_KEY)


# --------------------------
# ✏️ Input Box
# --------------------------
input_text = st.text_input("Enter your English text:", key="input_msg")


# --------------------------
# 🧠 Translation Function (your logic unchanged)
# --------------------------
def translate_with_groq(question):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that translates English to French."},
        {"role": "user", "content": f"Question: {question}"},
    ]

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=1024,
    )

    # Same extraction logic
    try:
        return resp.choices[0].message["content"]
    except:
        try:
            return resp.choices[0].text
        except:
            return str(resp)


# --------------------------
# 🟦 Output Section
# --------------------------
if input_text:
    with st.spinner("Translating..."):
        output = translate_with_groq(input_text)

    st.markdown("<div class='output-box'>", unsafe_allow_html=True)
    st.markdown("### 🇫🇷 French Translation:")
    st.write(output)
    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------
# 📝 Footer
# --------------------------
st.markdown("<div class='footer'>Made with ❤️ using Groq + Llama + Streamlit</div>", unsafe_allow_html=True)

