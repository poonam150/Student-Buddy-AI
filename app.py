import streamlit as st
from textblob import TextBlob
import pandas as pd
import datetime
import google.generativeai as genai
import os

# 1. SETUP - Loading the Google Password
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

# Configuring the AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- UI THEME ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c2c 0%, #0e1117 100%); color: #e0e0e0; }
    .stTextInput input { border-radius: 15px; background-color: rgba(255,255,255,0.05); color: white; border: 1px solid #4facfe; }
    .stButton>button { border-radius: 20px; background: linear-gradient(90deg, #4facfe, #00f2fe); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

# 3. INTERFACE
st.title("🤖 Student Buddy AI")
st.write("A real AI companion that listens and tracks your emotional well-being.")

user_input = st.text_input("What's on your mind?", key="user_msg")

if user_input:
    # --- SENTIMENT ANALYSIS ---
    analysis = TextBlob(user_input)
    score = round(analysis.sentiment.polarity, 2)
    
    # --- REAL AI CONVERSATION ---
    with st.spinner("Buddy is thinking..."):
        try:
            # The AI prompt
            prompt = f"You are a kind, empathetic student counselor. A student says: '{user_input}'. Reply like a friend in 2-3 sentences and give a small piece of advice."
            response = model.generate_content(prompt)
            bot_text = response.text
        except Exception as e:
            bot_text = "I'm listening, but my connection is a bit slow. How are you doing otherwise?"

    # Show the AI response
    st.chat_message("assistant").write(bot_text)
    
    # Save to history
    st.session_state.mood_history.append({"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Score": score})

# 4. DASHBOARD
if st.session_state.mood_history:
    st.divider()
    df = pd.DataFrame(st.session_state.mood_history)
    
    col1, col2 = st.columns(2)
    current_mood_val = st.session_state.mood_history[-1]["Score"]
    col1.metric("Current Mood", f"{current_mood_val}")
    
    avg_score = df["Score"].mean()
    status = "Positive ✨" if avg_score > 0.1 else "Neutral ⚖️" if avg_score > -0.1 else "Needs Support 💙"
    col2.metric("Overall Vibe", status)

    st.subheader("📈 Emotional Trend")
    st.line_chart(df.set_index("Time")["Score"])








