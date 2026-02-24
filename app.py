import streamlit as st
import pandas as pd
import datetime
from google import genai
import os

# 1. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

# Using the new 2026 Client logic
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Student Buddy AI Pro", page_icon="🧘‍♂️")

# --- UI STYLE ---
st.markdown("<style>.stApp { background: #0e1117; color: white; }</style>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Student Buddy AI Pro")

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. CHAT LOGIC
if prompt := st.chat_input("How are you feeling, friend?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Buddy is thinking..."):
            try:
                # Using Gemini 2.0 Flash - the most stable model in 2026
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"You are a kind student buddy. Reply to: '{prompt}' in 2 warm sentences."
                )
                bot_reply = response.text
            except Exception as e:
                # VARIED BACKUP: If API fails, it picks a random tip so it's NOT a loop
                backups = [
                    "I'm here for you. Why don't we try taking three deep breaths together?",
                    "That sounds like a lot to handle. Remember, you've overcome tough days before.",
                    "I'm listening. Sometimes just saying it out loud helps a little bit, doesn't it?"
                ]
                import random
                bot_reply = random.choice(backups)
            
            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})














