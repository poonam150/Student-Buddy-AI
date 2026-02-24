# 🤖 Student Buddy AI Pro
> **Your 24/7 Intelligent Companion for Academic Success and Emotional Well-being.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://student-buddy-ai-ryicjbgyzyfsauws5mhj26.streamlit.app/)
[![Model: Gemini-2.5-Flash](https://img.shields.io/badge/Model-Gemini--2.5--Flash-blueviolet)](https://deepmind.google/technologies/gemini/)

## 🌟 Overview
**Student Buddy AI Pro** is a specialized mental health and productivity assistant designed to combat student burnout. Built using **Streamlit** and powered by the **Google Gemini 2.5 Flash** large language model, it provides empathetic support while tracking emotional trends through advanced sentiment analysis.

## ✨ Key Features
* **🧠 Empathetic AI Chat:** Real-time, human-like conversations tailored to student life (stress, exams, and project pressure).
* **📊 Mood Dashboard:** Automatically visualizes your emotional journey with a live line chart and sentiment metrics.
* **🧘‍♂️ Zen Tools:** Integrated "Quick Stress Reset" with a guided breathing timer in the sidebar.
* **🚀 Auto-Discovery Engine:** Advanced error handling that ensures a stable connection to the latest Google Gemini models.
* **🛡️ Crisis Support:** Quick-access information for immediate mental health resources.

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Python) |
| **AI Engine** | Google Gemini 2.5 Flash API |
| **Data Logic** | Pandas & TextBlob |
| **Deployment** | GitHub + Streamlit Community Cloud |

## 🚀 Setup & Installation

### 1. Prerequisites
* Python 3.9+
* A Google AI Studio API Key ([Get it here](https://aistudio.google.com/))

### 2. Local Installation
```bash
# Clone the repository
git clone [https://github.com/poonam150/student-buddy-ai.git](https://github.com/poonam150/student-buddy-ai.git)
cd student-buddy-ai

# Install dependencies
pip install -r requirements.txt

3. Configuration
Add your API key to your Streamlit secrets or create a .streamlit/secrets.toml file:
GOOGLE_API_KEY = "your_actual_api_key_here"

4. Run the App
streamlit run app.py


