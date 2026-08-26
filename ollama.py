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
    .stApp {
        background: linear-gradient(-45deg, #0a0f24, #1a1b4b, #2b1a3d, #0d1b2a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e0e0e0;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .block-container {
        padding-top: 2rem !important;
    }
    header {visibility: hidden;}

    .chat-wrapper {
        display: flex;
        width: 100%;
        margin-bottom: 24px;
        animation: fadeIn 0.4s ease-out forwards;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-wrapper { justify-content: flex-end; }
    .bot-wrapper { justify-content: flex-start; }

    .user {
        background: rgba(43, 88, 118, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 16px 24px;
        border-radius: 20px 20px 4px 20px;
        color: #f8f9fa;
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        max-width: 80%;
    }
    
    .bot {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 16px 24px;
        border-radius: 20px 20px 20px 4px;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        max-width: 80%;
        position: relative;
    }
    
    .bot::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: inherit;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
        pointer-events: none;
    }
    
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 20px rgba(138, 180, 248, 0.2);
    }
    .stTextInput>div>div>input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }

    .app-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(to right, #e2e2e2, #8b9bb4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
        font-family: 'Outfit', 'Inter', sans-serif;
        letter-spacing: -1px;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .app-subtitle {
        font-size: 15px;
        font-weight: 400;
        color: #8b9bb4;
        text-align: center;
        margin-top: 0px;
        margin-bottom: 40px;
        font-family: 'Inter', sans-serif;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
</style>
<div class="app-title">Gen AI ChatBot</div>
<div class="app-subtitle">Premium Intelligence Engine</div>
""", unsafe_allow_html=True)


# -------------------------------------
# Chat Memory (Limited to last 4 messages)
# -------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for m in st.session_state.messages:
    if m["role"] == "user":
        st.markdown(f"<div class='chat-wrapper user-wrapper'><div class='user'>🙋‍♂️ {m['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-wrapper bot-wrapper'><div class='bot'>🤖 {m['content']}</div></div>", unsafe_allow_html=True)

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

    response = client.chat.completions.create(
        model="llama3-8b-8192",
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


