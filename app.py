import streamlit as st
from textblob import TextBlob
import pandas as pd
import datetime
import random

# 1. PAGE SETUP
st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- SMOOTH UI THEME ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c2c 0%, #0e1117 100%); color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; text-shadow: 0 0 10px rgba(0, 242, 254, 0.5); }
    .stTextInput input { border-radius: 15px; background-color: rgba(255,255,255,0.05); color: white; border: 1px solid #4facfe; }
    .stButton>button { border-radius: 20px; background: linear-gradient(90deg, #4facfe, #00f2fe); color: white; border: none; }
    .suggestion-box { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border-left: 5px solid #00f2fe; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. INSTANT NLP LOGIC (Zero Lag)
def get_counselor_advice(sentiment_score):
    if sentiment_score < -0.1:
        return [
            "Take 5 deep breaths. You are stronger than this moment. 🧘‍♂️",
            "Try a 5-minute walk to clear your head. 🚶‍♂️",
            "Journaling your thoughts can help release stress. 📝"
        ]
    elif sentiment_score > 0.1:
        return [
            "You're in a great head space! What's one thing you achieved today? 🌟",
            "Keep this energy going by helping a friend. 😊",
            "Lock in this mood by writing down what made you happy. ✍️"
        ]
    else:
        return [
            "Focus on one small task at a time. You've got this. ✅",
            "Stay hydrated—grab a glass of water. 💧",
            "A quick 1-minute stretch can boost your focus. 🤸‍♂️"
        ]

# 3. INITIALIZATION
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

# 4. SIDEBAR
with st.sidebar:
    st.title("☀️ Zen Zone")
    if st.button("✨ Daily Motivation"):
        quotes = ["Progress over perfection.", "You are enough.", "Believe in yourself."]
        st.success(random.choice(quotes))
    st.divider()
    st.write("Using TextBlob NLP for Sentiment Analysis.")

# 5. MAIN INTERFACE
st.title("🤖 Student Buddy AI")
st.write("Real-time emotional support and wellness tracking.")

user_input = st.text_input("How are you feeling right now?", key="user_msg")

if user_input:
    # --- NLP ANALYSIS ---
    analysis = TextBlob(user_input)
    current_score = round(analysis.sentiment.polarity, 2)
    
    # --- SAVE TO HISTORY ---
    st.session_state.mood_history.append({
        "Time": datetime.datetime.now().strftime("%H:%M:%S"), 
        "Score": current_score
    })

    # --- DISPLAY ADVICE ---
    st.subheader("Your Personalized Care Tips")
    tips = get_counselor_advice(current_score)
    for tip in tips:
        st.markdown(f"<div class='suggestion-box'>{tip}</div>", unsafe_allow_html=True)

    # Safety Alert
    if current_score < -0.4:
        st.error("🚨 It sounds like you're going through a lot. Please consider talking to a trusted friend or mentor.")

# 6. DASHBOARD (Protected from NameErrors)
if st.session_state.mood_history:
    st.divider()
    st.subheader("📈 Emotional Trend")
    
    df = pd.DataFrame(st.session_state.mood_history)
    
    col1, col2 = st.columns(2)
    latest_score = st.session_state.mood_history[-1]["Score"]
    col1.metric("Current Vibe", f"{latest_score}")
    
    avg_score = df["Score"].mean()
    status = "Positive ✨" if avg_score > 0.1 else "Neutral ⚖️" if avg_score > -0.1 else "Needs Care 💙"
    col2.metric("Overall Status", status)

    # Visualization
    st.line_chart(df.set_index("Time")["Score"])






