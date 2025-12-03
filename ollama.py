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
st.set_page_config(
    page_title="Simple GEN AI Chatbot",
    layout="centered",
    page_icon="🤖"
)

# -------------------------------------
# UI Styling
# -------------------------------------
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #090a0f, #1f2633);
        color: white !important;
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
        margin-bottom: 5px;
        color: #fff;
    }
    .bot {
        background: #0d1117;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        color: #00eaff;
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

# -------------------------------------
# Title
# -------------------------------------
st.markdown("<div class='title'>Simple GEN AI CHATBOT</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Powered by Llama 3 — Smart, Fast, Free (Groq)</div>", unsafe_allow_html=True)

# -------------------------------------
# Chat History (Limited Memory)
# -------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for m in st.session_state.messages:
    if m["role"] == "user":
        st.markdown(f"<div class='chat-box'><div class='user'>🙋‍♂️ {m['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-box'><div class='bot'>🤖 {m['content']}</div></div>", unsafe_allow_html=True)

# -------------------------------------
# User Input
# -------------------------------------
user_input = st.text_input("Type your message...")

# -------------------------------------
# Limited-memory chat function (BEST)
# -------------------------------------
def chat_with_groq(prompt):

    limited_memory = st.session_state.messages[-4:]

    messages = [{"role": m["role"], "content": m["content"]} for m in limited_memory]
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # FINAL WORKING MODEL
        messages=messages,
        max_tokens=300
    )

    return response.choices[0].message.content

# -------------------------------------
# Handle response
# -------------------------------------
if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        bot_reply = chat_with_groq(user_input)

    # Save bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    st.rerun()

# Footer
st.markdown("<br><center style='color:#777'>Made with ❤️ using Groq + Streamlit</center>", unsafe_allow_html=True)

