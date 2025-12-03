import streamlit as st
from groq import Groq
import os

# ----------------------------
# Load API Key
# ----------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY in Streamlit Secrets")
else:
    client = Groq(api_key=GROQ_API_KEY)

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(
    page_title="Groq ChatGPT",
    layout="centered",
    page_icon="🤖"
)

# ----------------------------
# BEAUTIFUL UI (CSS)
# ----------------------------
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #090a0f, #1f2633);
        color: white !important;
    }
    .main {
        background: linear-gradient(135deg, #090a0f, #1f2633);
    }
    .title {
        font-size: 42px;
        font-weight: 900;
        color: #00eaff;
        text-align: center;
        text-shadow: 0px 0px 20px rgba(0, 238, 255, 0.7);
        margin-bottom: 5px;
    }
    .sub {
        text-align: center;
        font-size: 16px;
        color: #d0d0d0;
        margin-top: -10px;
        margin-bottom: 25px;
    }
    .chat-container {
        background: #12151c;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #00eaff60;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(0, 238, 255, 0.1);
    }
    .user-msg {
        color: #fff;
        padding: 10px;
        background: #1e2a38;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .bot-msg {
        color: #00eaff;
        padding: 10px;
        background: #0d1117;
        border-radius: 10px;
        margin-bottom: 5px;
        border-left: 3px solid #00eaff;
    }
    .stTextInput>div>div>input {
        background: #1b1f29;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Title
# ----------------------------
st.markdown("<div class='title'>Simple GEN AI CHATBOT</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Powered by Llama 3.1 — Fast, Smart, Free</div>", unsafe_allow_html=True)

# ----------------------------
# Chat History
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-container'><div class='user-msg'>🙋‍♂️ {msg['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><div class='bot-msg'>🤖 {msg['content']}</div></div>", unsafe_allow_html=True)

# ----------------------------
# User Input
# ----------------------------
user_input = st.text_input("Type your message...", key="input")

# ----------------------------
# Groq Chat Function
# ----------------------------
def chat_with_groq(text):
    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    messages.append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=300
    )

    return response.choices[0].message["content"]

# ----------------------------
# Handle user message
# ----------------------------
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get chatbot response
    with st.spinner("Thinking..."):
        bot_reply = chat_with_groq(user_input)

    # Add response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Rerun to update UI
    st.experimental_rerun()

# Footer
st.markdown("<br><center style='color:#7a7a7a'>Made with ❤️ using Groq + Streamlit</center>", unsafe_allow_html=True)
