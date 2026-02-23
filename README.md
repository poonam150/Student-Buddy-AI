# 🤖 Student Buddy AI: Mental Health Companion

A professional Streamlit web application designed to support student well-being using **Natural Language Processing (NLP)** and **Large Language Models (LLMs)**. This tool analyzes student sentiment in real-time to provide personalized self-care advice and emotional tracking.

## 🚀 Live Demo
**Access the app here:** [Student Buddy AI Live](https://student-buddy-ai-hr7jw9v6j5dzsvbb4estxq.streamlit.app/)

---

## 🌟 Key Features
- **AI-Powered Counseling:** Utilizes the `TinyLlama-1.1B` model to generate 3 short, actionable self-care tips tailored to user input.
- **Real-time Sentiment Analysis:** Leverages `TextBlob` to calculate emotional polarity scores, helping students visualize their mood.
- **Interactive Mood Dashboard:** Generates dynamic line charts and metrics using `Pandas` to track emotional health over time.
- **Smart Daily Missions:** An interactive feature that suggests mental health "missions" (like tech breaks or social connection) based on the user's current mood score.
- **High-End UI/UX:** A "Smooth UI" featuring a dark-mode radial gradient, glassmorphism input fields, and CSS-animated breathing guides.
- **Safety & Resources:** Built-in logic to detect high-distress scores and provide immediate links to global support resources (WHO/Wikipedia).

## 🛠️ Tech Stack
- **Frontend/Backend:** [Streamlit](https://streamlit.io/)
- **Sentiment Engine:** [TextBlob](https://textblob.readthedocs.io/)
- **LLM Integration:** [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- **Data Visualization:** [Pandas](https://pandas.pydata.org/)
- **Security:** Streamlit Secrets Management (TOML) for secure API handling.

## 📦 Local Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Student-Buddy-AI.git](https://github.com/YOUR_USERNAME/Student-Buddy-AI.git)
