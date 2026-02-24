import streamlit as st
import pandas as pd
import datetime
from google import genai
import os
import time

# 1. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

# 2. CONFIG & UI
st.set_page_config(page_title="BuddyAI Pro", page_icon="🧘‍♂️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    [data-testid="stMetricValue"] { color: #00f2fe; }
    .sidebar-content { padding: 20px; border-radius: 15px; background: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# --- SIDEBAR TOOLS ---
with st.sidebar:
    st.title("🌿 Wellness Tools")
    st.subheader("Quick Stress Reset")
    if st.button("Start 1-Min Breathing"):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.1)
            progress_bar.progress(i + 1)
        st.success("Great job. Take one more deep breath.")
    
    st.divider()
    st.info("Tip: If the project feels like a nightmare, break it into 3 tiny tasks for today.")

# --- MAIN INTERFACE ---
st.title("🤖 Student Buddy AI Pro")
st.caption("Connected to: Gemini 2.5 Flash")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. CHAT LOGIC
if prompt := st.chat_input("Talk to your buddy..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Response
    with st.chat_message("assistant"):
        with st.spinner("Buddy is thinking..."):
            try:
                # We ask the AI to also give a "Mood Score" between -1 and 1
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=f"You are a kind student buddy. A student says: '{prompt}'. Reply in 2 warm sentences. Then, on a new line, provide a sentiment score only as 'Score: X' where X is between -1.0 and 1.0."
                )
                full_text = response.text
                
                # Split the text from the score
                if "Score:" in full_text:
                    bot_reply, score_part = full_text.split("Score:")
                    score_val = float(score_part.strip())
                else:
                    bot_reply = full_text
                    score_val = 0.0
                
                st.markdown(bot_reply)
                
                # Save Data
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                st.session_state.mood_history.append({
                    "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "Score": score_val
                })
            except Exception as e:
                st.error("I'm here, but the connection flickered. Let's keep talking!")

# 4. LIVE DASHBOARD
if st.session_state.mood_history:
    st.divider()
    st.subheader("📈 Emotional Trend Dashboard")
    df = pd.DataFrame(st.session_state.mood_history)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        current_score = st.session_state.mood_history[-1]["Score"]
        st.metric("Current Mood Score", f"{current_score}")
        if current_score < -0.3:
            st.warning("You seem stressed. Remember to take a break! ☕")
    
    with col2:
        st.line_chart(df.set_index("Time")["Score"])
















