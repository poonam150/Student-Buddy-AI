import streamlit as st
from textblob import TextBlob
import pandas as pd
import datetime
import google.generativeai as genai
import os

# 1. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- UI STYLE ---
st.markdown("<style>.stApp { background: #0e1117; color: white; }</style>", unsafe_allow_html=True)

if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

st.title("🤖 Student Buddy AI")

user_input = st.text_input("What's on your mind?", key="user_msg")

if user_input:
    # 1. Mood Analysis
    score = TextBlob(user_input).sentiment.polarity
    
    # 2. AI Talk
    with st.spinner("Buddy is thinking..."):
        try:
            prompt = f"You are a supportive student buddy. Reply to: '{user_input}' in 2 short sentences."
            response = model.generate_content(prompt)
            bot_text = response.text
        except Exception as e:
            # THIS WILL TELL US THE REAL ERROR
            bot_text = f"Connection error: {str(e)}"

    st.chat_message("assistant").write(bot_text)
    st.session_state.mood_history.append({"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Score": score})

# 3. DASHBOARD
if st.session_state.mood_history:
    st.divider()
    df = pd.DataFrame(st.session_state.mood_history)
    st.metric("Mood Score", f"{st.session_state.mood_history[-1]['Score']}")
    st.line_chart(df.set_index("Time")["Score"])











