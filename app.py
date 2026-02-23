import streamlit as st
from textblob import TextBlob
import os
from dotenv import load_dotenv
from transformers import pipeline
import pandas as pd
import datetime

# 1. SETUP & THEME
# Secure token loading for Streamlit Cloud and Local
if "HF_TOKEN" in st.secrets:
    my_token = st.secrets["HF_TOKEN"]
else:
    load_dotenv()
    my_token = os.getenv("HF_TOKEN")

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- SMOOTH GRADIENT THEME (CSS) ---
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
        padding: 10px;
    }
    .stButton>button {
        border-radius: 20px;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(0, 242, 254, 0.4);
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
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
    }
    @keyframes pulse {
        0% { transform: scale(0.7); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(0.7); opacity: 0.5; }
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_chatbot():
    return pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", token=my_token)

chat_engine = load_chatbot()

# 2. SIDEBAR
with st.sidebar:
    st.title("☀️ Zen Zone")
    
    st.subheader("🧘 Breathing Guide")
    if st.checkbox("Start Breathing Exercise"):
        st.write("Focus on the light... Inhale... Exhale...")
        st.markdown('<div class="dot"></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🎯 Daily Mission")
    
    if st.button("Get My Mission"):
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
    st.caption("Link not working? Try: https://www.who.int/health-topics/mental-health")

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
    
    # --- AI Suggestions ---
    prompt = f"<|system|>\nYou are a supportive counselor. Give 3 short, actionable self-care tips in bullets.\n<|user|>\n{user_input}\n<|assistant|>\n"
    
    with st.spinner("Reflecting on your words..."):
        response = chat_engine(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)
        bot_text = response[0]['generated_text'].split("<|assistant|>\n")[-1]

    # --- Safety Check ---
    if score < -0.4:
        st.error("🚨 **Important:** You sound like you're going through a lot. Please reach out to a professional or a support hotline. You aren't alone.")
    
    st.chat_message("assistant").write(bot_text)
    
    st.download_button(label="📥 Save Wellness Plan", data=bot_text, file_name="wellness_plan.txt")

    # --- Save History ---
    st.session_state.mood_history.append({"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Score": score})

# 4. DASHBOARD & ANALYSIS
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

    # 5. FINAL SESSION SUMMARY (Corrected Indentation)
    if len(st.session_state.mood_history) > 3:
        with st.expander("📊 View Session Analysis"):
            st.write(f"Total messages analyzed: {len(st.session_state.mood_history)}")
            highest_mood = df["Score"].max()
            st.write(f"Your peak mood score today: **{highest_mood:.2f}**")
            st.write("Keep using the buddy to see your long-term trends!")
