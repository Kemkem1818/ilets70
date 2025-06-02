import streamlit as st
import openai
import random
import time
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

# --------------------
# Core Config
st.set_page_config(page_title="IELTS Reading Coach", layout="wide")
st.title("📘 IELTS Reading Coach – Improve from Band 4.0 to 7.0")

# --------------------
# Load API Key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# --------------------
# Personal Encouragement
st.markdown("""
### 👋 Hello Ha Chi!

You're about to train your brain and build the reading muscle for IELTS success. 🎯
Every passage you complete brings you closer to your goal of Band 7.0 – you’ve got this!
Take a deep breath, stay focused, and let’s begin!
""")

# --------------------
# Session Initialization
if "score" not in st.session_state:
    st.session_state.score = 0
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "generated_sets" not in st.session_state:
    st.session_state.generated_sets = []
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False

# --------------------
# Topic Pool
topics = [
    "renewable energy", "space exploration", "artificial intelligence", "climate change",
    "urban planning", "digital education", "genetic engineering", "global trade",
    "public transportation", "sustainable farming"
]

# --------------------
# Generate Reading Sets with OpenAI
if openai_api_key:
    client = openai.OpenAI(api_key=openai_api_key)
    if st.button("🔄 Generate 5 Reading Sets (1 Hour Practice)"):
        st.session_state.generated_sets.clear()
        st.session_state.current_index = 0
        st.session_state.answers.clear()
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.show_feedback = False
        with st.spinner("Generating content..."):
            for i in range(5):
                prompt = f"""
You are an IELTS reading tutor. Generate a Band 6–7 IELTS-style academic reading passage (~150 words) about: {random.choice(topics)}.
Then create 3 True/False/Not Given questions with answers.
Return the result in this format:

Passage:
<text>

Questions:
1. <text> Answer: <True/False/Not Given>
2. <text> Answer: <True/False/Not Given>
3. <text> Answer: <True/False/Not Given>
"""
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content.strip()
                parts = result.split("Questions:")
                if len(parts) < 2:
                    continue
                passage = parts[0].replace("Passage:", "").strip()
                raw_questions = parts[1].strip().split("\n")
                questions = []
                for q in raw_questions:
                    if q.strip():
                        try:
                            q_text, q_answer = q.strip().rsplit("Answer:", 1)
                            questions.append({
                                "skill": random.choice(["Skimming", "Scanning", "Main Idea", "Detail", "Inference", "Writer's View", "Vocabulary", "Paragraph Matching", "Time Management"]),
                                "question": q_text.strip(),
                                "options": ["True", "False", "Not Given"],
                                "answer": q_answer.strip()
                            })
                        except ValueError:
                            continue
                if questions:
                    st.session_state.generated_sets.append({
                        "passage": passage,
                        "questions": questions
                    })

# --------------------
# Display One Set at a Time
# (The rest of the code remains unchanged)

