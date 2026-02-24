import streamlit as st
from textblob import TextBlob
import pandas as pd
import datetime
import requests
import os
from dotenv import load_dotenv

# 1. SETUP
if "HF_TOKEN" in st.secrets:
    my_token = st.secrets["HF_TOKEN"]
else:
    load_dotenv()
    my_token = os.getenv("HF_TOKEN")

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c2c 0%, #0e1117 100%); color: #e0e0e0; }
    .stTextInput input { border-radius: 15px; background-color: rgba(255,255,255,0.05); color: white; border: 1px solid #4facfe; }
    .stButton>button { border-radius: 20px; background: linear-gradient(90deg, #4facfe, #00f2fe); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI BRAIN FUNCTION
def get_ai_response(user_text):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {my_token}", "X-Wait-For-Model": "true"}
    
    # We ask the AI to be a friend, not a robot
    prompt = f"<s>[INST] You are a kind student buddy. Someone says: '{user_text}'. Reply with one comforting sentence and then give 2 short self-care tips. [/INST]"
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 100}}, timeout=10)
        result = response.json()
        raw_output = result[0]['generated_text']
        return raw_output.split("[/INST]")[-1].strip()
    except:
        # Emergency backup if AI is slow
        return "I'm listening. That sounds tough, but you aren't alone. Try drinking some water and taking a 5-minute walk."

# 3. APP LOGIC
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

st.title("🤖 Student Buddy AI")
st.write("Talk to me. I'm here to listen and help you track your vibes.")

user_input = st.text_input("What's on your mind?", key="input")

if user_input:
    # --- SENTIMENT ---
    analysis = TextBlob(user_input)
    # We "smooth" the score so the chart doesn't jump too drastically
    new_score = analysis.sentiment.polarity
    
    # --- AI TALK ---
    with st.spinner("Buddy is thinking..."):
        reply = get_ai_response(user_input)
    
    st.chat_message("assistant").write(reply)
    
    # --- SAVE TO HISTORY ---
    st.session_state.mood_history.append({
        "Time": datetime.datetime.now().strftime("%H:%M:%S"), 
        "Score": new_score
    })

# 4. SMOOTH CHART DASHBOARD
if st.session_state.mood_history:
    st.divider()
    df = pd.DataFrame(st.session_state.mood_history)
    
    col1, col2 = st.columns(2)
    col1.metric("Current Vibe", f"{st.session_state.mood_history[-1]['Score']:.2f}")
    
    # Overall Status logic
    avg_score = df["Score"].mean()
    status = "Thriving ✨" if avg_score > 0.2 else "Doing Okay ⚖️" if avg_score > -0.2 else "Needs Support 💙"
    col2.metric("Overall Health", status)

    st.subheader("📈 Your Mood Journey")
    # We show the line chart with a fixed scale so it doesn't look "crazy"
    st.line_chart(df.set_index("Time")["Score"])







