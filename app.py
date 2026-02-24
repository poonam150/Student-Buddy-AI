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

genai.configure(api_key=api_key)

# --- THE FIX: NEWEST STABLE MODEL ---
# Using gemini-2.5-flash which is the 2026 workhorse model
MODEL_NAME = 'gemini-2.5-flash' 
model = genai.GenerativeModel(MODEL_NAME)

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

st.title("🤖 Student Buddy AI")

user_input = st.text_input("What's on your mind?", key="user_msg")

if user_input:
    score = TextBlob(user_input).sentiment.polarity
    
    with st.spinner("Buddy is thinking..."):
        try:
            response = model.generate_content(f"Reply as a supportive buddy to: {user_input}")
            bot_text = response.text
        except Exception as e:
            # --- MODEL SPY: IF IT FAILS, SHOW WHAT WE HAVE ACCESS TO ---
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                bot_text = f"Connection error. I tried {MODEL_NAME}, but your account shows these are available: {available_models}"
            except:
                bot_text = f"Error: {str(e)}"

    st.chat_message("assistant").write(bot_text)
    st.session_state.mood_history.append({"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Score": score})

if st.session_state.mood_history:
    st.divider()
    df = pd.DataFrame(st.session_state.mood_history)
    st.metric("Mood Score", f"{st.session_state.mood_history[-1]['Score']}")
    st.line_chart(df.set_index("Time")["Score"])












