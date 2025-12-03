import streamlit as st
from groq import Groq
import os

# -------------------------------------
# Load API Key
# -------------------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY in Streamlit Secrets")
else:
    client = Groq(api_key=GROQ_API_KEY)

# -------------------------------------
# Streamlit Page Setup
# -------------------------------------
st.set_page_config(page_title="GEN AI Chatbot", layout="centered", page_icon="🤖")

# -------------------------------------
# UI Styling
# -------------------------------------
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #090a0f, #1f2633);
        color: white !important;
    }
    .chat-box {
        background: #12151c;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #00eaff60;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(0, 238, 255, 0.1);
    }
    .user {
        background: #1e2a38;
        padding: 10px;
        border-radius: 10px;
        color: #fff;
    }
    .bot {
        background: #0d1117;
        padding: 10px;
        border-radius: 10px;
        color: #00eaff;
        border-left: 3px solid #00eaff;
    }
    .stTextInput>div>div>input {
        background: #1b1f29;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .app-title {
        font-size: 45px;
        font-weight: 900;
        color: #00eaff;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
        text-shadow: 0px 0px 25px rgba(0, 238, 255, 0.8);
        font-family: 'Segoe UI', sans-serif;
    }
    .app-subtitle {
        font-size: 18px;
        font-weight: 400;
        color: #cdd6f4;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 30px;
        font-family: 'Segoe UI', sans-serif;
    }
</style>
<div class="app-title">GEN AI ChatBot</div>
<div class="app-subtitle">Powered by Llama 3.3 — Fast • Smart • Accurate</div>
""", unsafe_allow_html=True)


# -------------------------------------
# Chat Memory (Limited to last 4 messages)
# -------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for m in st.session_state.messages:
    if m["role"] == "user":
        st.markdown(f"<div class='chat-box'><div class='user'>🙋‍♂️ {m['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-box'><div class='bot'>🤖 {m['content']}</div></div>", unsafe_allow_html=True)

# -------------------------------------
# Input Box
# -------------------------------------
user_input = st.text_input("Type your message...")

# -------------------------------------
# Chat Function
# -------------------------------------
def chat_with_groq(prompt):
    limited_memory = st.session_state.messages[-4:]

    messages = [{"role": m["role"], "content": m["content"]} for m in limited_memory]
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=300
    )

    return response.choices[0].message.content

# -------------------------------------
# PROCESS USER MESSAGE ONLY WHEN ENTER PRESSED
# -------------------------------------
if user_input and st.session_state.get("last_input") != user_input:

    # store input so it doesn't repeat
    st.session_state.last_input = user_input

    # save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        bot_reply = chat_with_groq(user_input)

    # save bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    st.rerun()   # refresh UI BUT no re-generation


