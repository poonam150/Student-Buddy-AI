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

client = genai.Client(api_key=api_key)

# 2. MODEL DISCOVERY (Breaks the "Loop" of 404 errors)
@st.cache_resource
def get_best_model():
    try:
        # Try the 2026 standard first
        client.models.get(model="gemini-3-flash")
        return "gemini-3-flash"
    except:
        try:
            # Fallback to 2.5 stable
            client.models.get(model="gemini-2.5-flash")
            return "gemini-2.5-flash"
        except:
            return "gemini-2.0-flash-001"

ACTIVE_MODEL = get_best_model()

st.set_page_config(page_title="BuddyAI Pro 2026", page_icon="🧘‍♂️")

# --- UI STYLE ---
st.markdown("<style>.stApp { background: #0e1117; color: white; }</style>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Student Buddy AI Pro")
st.caption(f"Connected to: {ACTIVE_MODEL}")

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. CHAT LOGIC
if prompt := st.chat_input("How are you feeling, friend?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Buddy is thinking..."):
            try:
                response = client.models.generate_content(
                    model=ACTIVE_MODEL, 
                    contents=f"Context: Supportive student counselor. Reply to: '{prompt}' in 2-3 warm sentences."
                )
                bot_reply = response.text
            except Exception as e:
                import random
                bot_reply = random.choice([
                    "I'm here for you. Let's take a deep breath together.",
                    "That sounds tough. Remember, you're doing your best.",
                    "I'm listening. Tell me more about what's on your mind."
                ])
            
            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})















