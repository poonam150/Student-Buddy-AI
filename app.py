import streamlit as st
from textblob import TextBlob
import pandas as pd
import datetime
import google.generativeai as genai
import os
import time

# 1. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. PAGE CONFIG
st.set_page_config(page_title="BuddyAI Pro", page_icon="🧘‍♂️", layout="wide")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #30363d; }
    [data-testid="stMetricValue"] { color: #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALIZE STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mood_data" not in st.session_state:
    st.session_state.mood_data = []

# --- SIDEBAR: WELLNESS TOOLS ---
with st.sidebar:
    st.title("🌿 Zen Tools")
    
    # Feature 1: Breathwork Timer
    st.subheader("Box Breathing")
    if st.button("Start 1-Min Reset"):
        progress_bar = st.progress(0)
        status = st.empty()
        for i in range(1, 16): # 4 cycles of 4-sec box breathing
            status.text("💨 Breathe In (4s)")
            time.sleep(1); progress_bar.progress(i*6)
    
    st.divider()
    
    # Feature 2: Crisis Support
    with st.expander("🚨 Need Immediate Help?"):
        st.write("You're not alone. Text HOME to 741741 (US/Canada) or 85258 (UK).")

# --- MAIN INTERFACE ---
st.title("🤖 Student Buddy AI Pro")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT INPUT LOGIC
if prompt := st.chat_input("How are you feeling, friend?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Perform Sentiment Analysis
    sentiment = TextBlob(prompt).sentiment.polarity
    st.session_state.mood_data.append({
        "Time": datetime.datetime.now().strftime("%H:%M"),
        "Score": sentiment
    })

    # Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Writing..."):
            try:
                full_prompt = f"You are an empathetic student buddy. Reply to: '{prompt}'. Keep it warm and human."
                response = model.generate_content(full_prompt)
                bot_reply = response.text
                st.markdown(bot_reply)
            except:
                bot_reply = "I'm right here. Take a breath, I'm listening."
                st.write(bot_reply)
                
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# 5. DASHBOARD SECTION (Below Chat)
if st.session_state.mood_data:
    st.divider()
    st.subheader("📊 Your Weekly Vibe Check")
    df = pd.DataFrame(st.session_state.mood_data)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        avg_vibe = sum(d['Score'] for d in st.session_state.mood_data) / len(st.session_state.mood_data)
        st.metric("Overall Sentiment", f"{avg_vibe:.2f}")
        if avg_vibe < -0.2: st.warning("Sending extra hugs today! 🫂")
    
    with col2:
        st.line_chart(df.set_index("Time")["Score"])













