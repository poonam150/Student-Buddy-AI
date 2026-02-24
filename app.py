import streamlit as st
from textblob import TextBlob
import os
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv

# 1. SETUP & SECURE TOKEN LOADING
if "HF_TOKEN" in st.secrets:
    my_token = st.secrets["HF_TOKEN"]
else:
    load_dotenv()
    my_token = os.getenv("HF_TOKEN")

# --- IMPROVED API FUNCTION ---
def query_hf_api(prompt_text):
    # Using TinyLlama - a reliable, fast model
    API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    headers = {
        "Authorization": f"Bearer {my_token}",
        "X-Wait-For-Model": "true"  # Force the API to wait until the model is loaded
    }
    payload = {
        "inputs": prompt_text,
        "parameters": {"max_new_tokens": 100, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# --- NEW: AUTO-WARMUP ON STARTUP ---
# This runs once when the app is first opened
if 'warmed_up' not in st.session_state:
    with st.spinner("🚀 Waking up the AI Buddy... please wait a few seconds."):
        query_hf_api("Hello") # Send a tiny "wake up" signal
        st.session_state.warmed_up = True
        st.toast("AI is now awake and ready!", icon="✅")

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- UI THEME (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c2c 0%, #0e1117 100%); color: #e0e0e0; }
    .stTextInput input { border-radius: 15px; background-color: rgba(255,255,255,0.05); color: white; }
    .stButton>button { border-radius: 20px; background: linear-gradient(90deg, #4facfe, #00f2fe); color: white; font-weight: bold; border: none; }
    .dot { height: 60px; width: 60px; background: #00f2fe; border-radius: 50%; margin: auto; animation: pulse 3s infinite; }
    @keyframes pulse { 0% {transform: scale(0.8); opacity: 0.4;} 50% {transform: scale(1.1); opacity: 1;} 100% {transform: scale(0.8); opacity: 0.4;} }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.title("☀️ Zen Zone")
    st.subheader("🧘 Breathing Guide")
    if st.checkbox("Show Guide"):
        st.markdown('<div class="dot"></div>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("Get My Daily Mission"):
        st.info("Your mission: Spend 5 minutes without your phone today. 📵")
        st.balloons()

# 3. MAIN INTERFACE
st.title("🤖 Student Buddy AI")
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

user_input = st.text_input("How are you feeling right now?", placeholder="e.g. I am feeling a bit stressed about exams.")

if user_input:
    # 1. Analyze Sentiment
    score = TextBlob(user_input).sentiment.polarity
    
    # 2. Get AI Advice
    prompt = f"<|system|>\nYou are a kind student counselor. Give 2 short tips.\n<|user|>\n{user_input}\n<|assistant|>\n"
    
    with st.spinner("AI is thinking..."):
        try:
            output = query_hf_api(prompt)
            # Handle list response
            if isinstance(output, list) and len(output) > 0:
                bot_response = output[0].get('generated_text', "I'm here for you!")
            else:
                bot_response = "I'm processing that. Can you try saying it one more time?"
        except:
            bot_response = "Connection is busy. Let's try again in a second!"

    # 3. Display Result
    st.chat_message("assistant").write(bot_response)
    st.session_state.mood_history.append({"Time": datetime.datetime.now().strftime("%H:%M"), "Score": score})

# 4. DASHBOARD
if st.session_state.mood_history:
    st.divider()
    st.subheader("📈 Your Mood Journey")
    df = pd.DataFrame(st.session_state.mood_history)
    st.line_chart(df.set_index("Time"))
    
    avg_mood = df["Score"].mean()
    if avg_mood > 0:
        st.success(f"Overall vibe: Positive (Score: {avg_mood:.2f})")
    else:
        st.warning(f"Overall vibe: Needs a boost (Score: {avg_mood:.2f})")



