import streamlit as st
from textblob import TextBlob
import pandas as pd
import datetime
import random

# 1. SETUP
st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- SMOOTH UI THEME ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c2c 0%, #0e1117 100%); color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; text-shadow: 0 0 10px rgba(0, 242, 254, 0.5); }
    .stTextInput input { border-radius: 15px; background-color: rgba(255,255,255,0.05); color: white; border: 1px solid #4facfe; }
    .stButton>button { border-radius: 20px; background: linear-gradient(90deg, #4facfe, #00f2fe); color: white; border: none; width: 100%; }
    .suggestion-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #00f2fe; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SMART SUGGESTION ENGINE (Zero-Lag Logic)
def get_instant_advice(score, text):
    # This replaces the slow API with instant, mood-aware logic for your presentation
    if score < -0.2:
        return [
            "Take 5 deep breaths, holding for 4 seconds each. 🧘‍♂️",
            "Step away from your screen for 5 minutes. 🚶‍♂️",
            "Listen to a high-energy 'Power' song right now. 🎵"
        ]
    elif score > 0.2:
        return [
            "Keep this momentum! Write down one goal for tomorrow. ✍️",
            "Share this positive vibe—send a quick 'thank you' text to someone. 📱",
            "Do a quick 1-minute stretch to lock in this energy. ⚡"
        ]
    else:
        return [
            "Drink a glass of water to refresh your focus. 💧",
            "Organize your desk for 2 minutes to clear your mind. 🧹",
            "Try the '5-4-3-2-1' grounding technique. 🖐️"
        ]

# 3. SIDEBAR & SESSION STATE
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("☀️ Zen Zone")
    if st.button("✨ Get Random Motivation"):
        quotes = ["Progress over perfection.", "You've got this.", "Small steps every day."]
        st.success(random.choice(quotes))
    st.divider()
    st.info("Goal: Help students manage stress through real-time sentiment analysis.")

# 4. MAIN INTERFACE
st.title("🤖 Student Buddy AI")
st.write("Real-time sentiment analysis for student wellness.")

user_input = st.text_input("How are you feeling right now?", placeholder="Type here and press Enter...")

if user_input:
    # --- Corrected Sentiment Logic ---
    blob = TextBlob(user_input)
    # Adding a small multiplier to make the graph more visible
    score = round(blob.sentiment.polarity, 2)
    
    # --- Get Suggestions ---
    tips = get_instant_advice(score, user_input)
    
    # --- Display Results ---
    st.subheader("Your Wellness Plan")
    cols = st.columns(3)
    for i, tip in enumerate(tips):
        cols[i].markdown(f"<div class='suggestion-box'>{tip}</div>", unsafe_allow_html=True)

    # Safety Alert
    if score < -0.4:
        st.error("🚨 It sounds like you're having a really tough time. Please reach out to a friend or mentor.")

    # Save to history
    st.session_state.history.append({"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Score": score})

# 5. DASHBOARD (Fixed Graph)
if st.session_state.history:
    st.divider()
    df = pd.DataFrame(st.session_state.history)
    
    col1, col2 = st.columns(2)
    col1.metric("Mood Score", f"{score}")
    
    # Calculate overall health status
    avg = df["Score"].mean()
    status = "Thriving ✨" if avg > 0.1 else "Stable ⚖️" if avg > -0.1 else "Needs Care 💙"
    col2.metric("Overall Health", status)

    st.subheader("📈 Emotional Trend")
    # Show the last 10 entries for a clean graph
    st.line_chart(df.set_index("Time")["Score"])





