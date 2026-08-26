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
        background-color: #f4f4f2;
    }
    
    .chat-wrapper {
        display: flex;
        width: 100%;
        margin-bottom: 20px;
    }
    .user-wrapper {
        justify-content: flex-end;
    }
    .bot-wrapper {
        justify-content: flex-start;
    }

    .user {
        background: #2c3e50;
        padding: 15px 22px;
        border-radius: 18px 18px 4px 18px;
        color: #ffffff;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        max-width: 80%;
    }
    .bot {
        background: #ffffff;
        padding: 15px 22px;
        border-radius: 18px 18px 18px 4px;
        color: #2c3e50;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 16px;
        line-height: 1.5;
        border: 1px solid #e1e4e8;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        max-width: 80%;
    }
    
    .stTextInput>div>div>input {
        background: #ffffff;
        color: #333333;
        border: 1px solid #d1d5da;
        border-radius: 10px;
        padding: 12px 15px;
        font-size: 16px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    .stTextInput>div>div>input:focus {
        border-color: #2c3e50;
        box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.2);
    }

    .app-title {
        font-size: 42px;
        font-weight: normal;
        color: #1a252f;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 5px;
        font-family: 'Garamond', 'Georgia', serif;
        letter-spacing: -0.5px;
    }
    .app-subtitle {
        font-size: 14px;
        font-weight: 500;
        color: #7f8c8d;
        text-align: center;
        margin-top: 0px;
        margin-bottom: 40px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
</style>
<div class="app-title">Gen AI ChatBot</div>
<div class="app-subtitle">Powered by Llama • Fast • Smart</div>
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
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
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


