# MediBot - Simple Medical Assistant
# pip install streamlit requests
# streamlit run medibot.py

import streamlit as st
import requests
import json
import base64

# ── Setup ──────────────────────────────────────────────────
st.set_page_config(page_title="MediBot", page_icon="🩺")

API_KEY = "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"
URL     = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# ── Simple CSS ─────────────────────────────────────────────
st.markdown("""
<style>

/* Full app background */
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/free-vector/clean-medical-background_53876-97927.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Main content container */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
    right: 2rem;
}

/* White glass card effect */
.block-container {
    background: rgba(255, 255, 255, 0.92);
    padding: 2rem;
    border-radius: 20px;
    margin-top: 2rem;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.08);
}

/* Hide Streamlit default UI */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Result box */
.result {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #2563eb;
    margin-top: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    color: black;
}

/* Buttons */
.stButton > button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-weight: bold !important;
    width: 100% !important;
}

/* Text area */
textarea {
    background: white !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Force all text inside main container to dark */
h1, h2, h3, h4, h5, h6,
p, label, div, span {
    color: #0f172a !important;
}

/* Streamlit text input labels */
label {
    font-weight: 600 !important;
}

/* Warning box text */
[data-testid="stAlertContainer"] {
    color: #111827 !important;
}

/* Tabs text */
button[data-baseweb="tab"] {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* Placeholder text */
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* Caption text */
.css-10trblm {
    color: #334155 !important;
}

</style>
""", unsafe_allow_html=True)
# ── Call LLM ───────────────────────────────────────────────
def ask_llm(prompt):
    """Send prompt to Groq LLM and return the answer."""
    body = {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 700,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(URL, headers=HEADERS, data=json.dumps(body))
    return response.json()["choices"][0]["message"]["content"]

# ── Analyze Medicine Photo (Vision) ───────────────────────
def analyze_photo(image_bytes):
    """Send image to vision LLM and get medicine details."""
    b64 = base64.b64encode(image_bytes).decode()  # convert image to base64 text
    body = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "max_tokens": 700,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text",      "text": "Analyze this medicine. Give: name, what it treats, when to use, when NOT to use, side effects. Keep it simple and clear."}
            ]
        }]
    }
    response = requests.post(URL, headers=HEADERS, data=json.dumps(body))
    return response.json()["choices"][0]["message"]["content"]

# ── UI ─────────────────────────────────────────────────────
st.title("🩺 MediBot")
st.caption("AI Medical Assistant — Symptom Checker & Medicine Analyzer")
st.divider()

tab1, tab2 = st.tabs(["💬 Symptom Checker", "💊 Medicine Photo"])

# Tab 1 — Symptom Checker
with tab1:
    st.warning("⚠️ This is not medical advice. Always consult a doctor.")

    symptoms = st.text_area("Describe your symptoms:", height=100,
                            placeholder="e.g. headache, fever 101°F, sore throat for 2 days...")

    if st.button("Analyze Symptoms"):
        if symptoms.strip():
            with st.spinner("Analyzing..."):
                prompt = f"""You are a medical assistant.
Patient says: {symptoms}

Give:
1. Possible conditions
2. Severity (Mild/Moderate/Severe)
3. Home remedies
4. OTC medicine suggestions (no dosage)
5. When to see a doctor

End with: This is not medical advice. Consult a doctor."""

                result = ask_llm(prompt)

            st.markdown(f"<div class='result'>{result.replace(chr(10),'<br>')}</div>",
                        unsafe_allow_html=True)
        else:
            st.error("Please enter your symptoms.")

# Tab 2 — Medicine Photo
with tab2:
    st.warning("⚠️ Always verify medicine info with a pharmacist.")

    photo = st.file_uploader("Upload a medicine photo:", type=["jpg", "jpeg", "png"])

    if photo:
        st.image(photo, width=260)

        if st.button("Analyze Medicine"):
            with st.spinner("Reading medicine with Vision AI..."):
                result = analyze_photo(photo.read())

            st.markdown(f"<div class='result'>{result.replace(chr(10),'<br>')}</div>",
                        unsafe_allow_html=True)
