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

# --- FAST API FUNCTION ---
def query_hf_api(prompt_text):
    # This calls Hugging Face's high-speed servers directly
    API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    headers = {"Authorization": f"Bearer {my_token}"}
    payload = {
        "inputs": prompt_text,
        "parameters": {
            "max_new_tokens": 150, 
            "temperature": 0.7, 
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- SMOOTH UI THEME (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #1a1c2c 0%, #0e1117 100%);
        color: #e0e0e0;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(10px);
    }
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
    }
    .stButton>button {
        border-radius: 20px;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-weight: bold;
        border: none;
    }
    [data-testid="stMetricValue"] {
        color: #00f2fe !important;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
    }
    .dot {
        height: 80px; width: 80px;
        background: radial-gradient(circle, #00f2fe, #4facfe);
        border-radius: 50%;
        margin: 20px auto;
        animation: pulse 4s ease-in-out infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.7); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(0.7); opacity: 0.5; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.title("☀️ Zen Zone")
    
    st.subheader("🧘 Breathing Guide")
    if st.checkbox("Start Breathing Exercise"):
        st.write("Inhale... Exhale...")
        st.markdown('<div class="dot"></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🎯 Daily Mission")
    if st.button("Get My Mission"):
        # Logic based on mood history
        current_score = st.session_state.mood_history[-1]['Score'] if 'mood_history' in st.session_state and st.session_state.mood_history else 0
        if current_score < -0.1:
            mission = "Listen to one song that makes you feel powerful. 🎵"
        elif current_score > 0.3:
            mission = "You're doing great! Share that energy—send a nice text to a friend. 📱"
        else:
            mission = "Take a 2-minute 'tech break' and look out a window. 🪟"
        st.session_state.current_mission = mission
        st.balloons()

    if 'current_mission' in st.session_state:
        st.info(st.session_state.current_mission)
    
    st.divider()
    st.subheader("📝 Daily Journal")
    journal_note = st.text_area("Write freely...", placeholder="How's your mental energy today?")
    if st.button("Save Entry"):
        st.success("Entry locked in.")
        st.balloons()
    
    st.divider()
    st.subheader("🆘 Quick Help")
    st.link_button("View Support Resources", "https://en.wikipedia.org/wiki/Mental_health")

# 3. MAIN INTERFACE
st.title("🤖 Student Buddy AI")
st.write("Your safe space for thoughts and self-care tips.")

if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

user_input = st.text_input("Type how you're feeling...")

if user_input:
    # --- Analysis ---
    blob = TextBlob(user_input)
    score = blob.sentiment.polarity
    
    # --- AI Suggestions (Fast API Call) ---
    prompt = f"<|system|>\nYou are a supportive counselor. Give 3 short, actionable self-care tips in bullets.\n<|user|>\n{user_input}\n<|assistant|>\n"
    
    with st.spinner("Reflecting on your words..."):
        try:
            output = query_hf_api(prompt)
            # The API returns generated text inside a list
            if isinstance(output, list) and len(output) > 0:
                bot_text = output[0].get('generated_text', "I'm thinking... please try again.")
            else:
                # If API is "warming up", it might return a message instead of a list
                bot_text = "The AI is warming up its brain. Please try typing your message again in 10 seconds!"
        except Exception as e:
            bot_text = "Connection is a bit slow. Please try again."

    # --- Results & Safety ---
    if score < -0.4:
        st.error("🚨 **Important:** You sound like you're going through a lot. Please reach out to a professional.")
    
    st.chat_message("assistant").write(bot_text)
    
    # --- Save History ---
    st.session_state.mood_history.append({"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Score": score})

# 4. DASHBOARD
if st.session_state.mood_history:
    st.divider()
    st.subheader("📈 Emotional Insights")
    df = pd.DataFrame(st.session_state.mood_history)
    
    col1, col2 = st.columns(2)
    col1.metric("Current Vibe", f"{st.session_state.mood_history[-1]['Score']:.2f}")
    
    avg_score = df["Score"].mean()
    status = "Thriving ✨" if avg_score > 0 else "Needs Care 💙"
    col2.metric("Overall Health", status)
    
    st.line_chart(df.set_index("Time"))

    if len(st.session_state.mood_history) > 3:
        with st.expander("📊 View Session Analysis"):
            highest_mood = df["Score"].max()
            st.write(f"Your peak mood score today: **{highest_mood:.2f}**")
            st.write("Keep using the buddy to see your long-term trends!")

