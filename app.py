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

# --- FAST API FUNCTION (MISTRAL MODEL) ---
def query_hf_api(prompt_text):
    # Mistral-7B is more reliable and stays "awake" longer than TinyLlama
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {
        "Authorization": f"Bearer {my_token}",
        "X-Wait-For-Model": "true" 
    }
    payload = {
        "inputs": prompt_text,
        "parameters": {
            "max_new_tokens": 150, 
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        return response.json()
    except:
        return None

st.set_page_config(page_title="Student Buddy AI", page_icon="🤖")

# --- UI THEME (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c2c 0%, #0e1117 100%); color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: rgba(22, 27, 34, 0.8); backdrop-filter: blur(10px); }
    .stTextInput input { background-color: rgba(255, 255, 255, 0.05); color: white; border-radius: 15px; }
    .stButton>button { border-radius: 20px; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: white; font-weight: bold; border: none; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; text-shadow: 0 0 10px rgba(0, 242, 254, 0.5); }
    .dot { height: 60px; width: 60px; background: radial-gradient(circle, #00f2fe, #4facfe); border-radius: 50%; margin: 20px auto; animation: pulse 4s infinite; }
    @keyframes pulse { 0% {transform: scale(0.7); opacity: 0.5;} 50% {transform: scale(1.1); opacity: 1;} 100% {transform: scale(0.7); opacity: 0.5;} }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.title("☀️ Zen Zone")
    st.subheader("🧘 Breathing Guide")
    if st.checkbox("Start Breathing"):
        st.markdown('<div class="dot"></div>', unsafe_allow_html=True)

    st.divider()
    if st.button("Get My Daily Mission"):
        st.info("Your mission: Write down 3 things you are grateful for today! 📝")
        st.balloons()
    
    st.divider()
    st.subheader("🆘 Quick Help")
    st.link_button("View Support Resources", "https://en.wikipedia.org/wiki/Mental_health")

# 3. MAIN INTERFACE
st.title("🤖 Student Buddy AI")
st.write("Your safe space for thoughts and self-care tips.")

if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

user_input = st.text_input("How are you feeling right now?")

if user_input:
    # --- Sentiment Analysis ---
    blob = TextBlob(user_input)
    score = blob.sentiment.polarity
    
    # --- AI Request ---
    # Mistral format: [INST] prompt [/INST]
    prompt = f"<s>[INST] You are a supportive counselor. A student says: '{user_input}'. Give 3 very short, bulleted self-care tips. [/INST]"
    
    with st.spinner("AI is thinking..."):
        output = query_hf_api(prompt)
        
        if output and isinstance(output, list) and 'generated_text' in output[0]:
            bot_text = output[0]['generated_text'].strip()
        else:
            bot_text = "I'm here for you! It sounds like you're going through a lot. Take a deep breath—I'm ready when you're ready to talk more."

    # --- Safety Check ---
    if score < -0.4:
        st.error("🚨 **Important:** You sound like you're going through a lot. Please reach out to a professional or a support hotline.")
    
    st.chat_message("assistant").write(bot_text)
    st.session_state.mood_history.append({"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Score": score})

# 4. DASHBOARD
if st.session_state.mood_history:
    st.divider()
    st.subheader("📈 Emotional Insights")
    df = pd.DataFrame(st.session_state.mood_history)
    
    c1, c2 = st.columns(2)
    c1.metric("Current Vibe", f"{score:.2f}")
    c2.metric("Overall Health", "Thriving ✨" if df["Score"].mean() > 0 else "Needs Care 💙")
    
    st.line_chart(df.set_index("Time"))




