# ============================================================
# MediBot — Simple Medical Assistant (One Page)
# Use: python -m streamlit run medibot.py
# Setup:
#   pip install streamlit requests duckduckgo-search Pillow
#   export GROQ_API_KEY=your_key   (get free at console.groq.com)
# ============================================================

import streamlit as st
import requests, json, os, base64
from duckduckgo_search import DDGS

# ── Config ────────────────────────────────────────────────
st.set_page_config(page_title="MediBot", page_icon="🩺", layout="centered")

API_KEY = "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"
URL     = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {"Content-Type":"application/json","Authorization":f"Bearer {API_KEY}"}

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');
* { font-family: 'Nunito', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem !important; max-width: 720px !important; }
.title  { text-align:center; font-size:2rem; font-weight:800; color:#1e293b; margin-bottom:4px; }
.sub    { text-align:center; color:#64748b; font-size:0.9rem; margin-bottom:28px; }
.card   { background:white; border-radius:16px; padding:20px; margin:12px 0;
          box-shadow:0 2px 16px rgba(0,0,0,0.07); border-left:4px solid #2563eb; }
.warn   { background:#fff7ed; border-left:4px solid #f59e0b; border-radius:10px;
          padding:10px 14px; font-size:0.82rem; color:#92400e; margin:10px 0; }
.stButton>button { background:linear-gradient(135deg,#2563eb,#0891b2) !important;
    color:white !important; border:none !important; border-radius:10px !important;
    font-weight:700 !important; padding:10px 20px !important; width:100% !important; }
</style>
""", unsafe_allow_html=True)

# ── MCP Web Search Tool ───────────────────────────────────
# This is the actual function that runs when LLM calls web_search
def web_search(query):
    with DDGS() as d:
        results = list(d.text(query, max_results=4))
    return "\n".join(f"{r['title']}: {r['body']}" for r in results)

# MCP Tool Schema — tells LLM what tools it can use
TOOLS = [{
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search web for medical info, symptoms, medicines",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

# ── Agentic Loop ──────────────────────────────────────────
# LLM decides to search → we search → send results back → LLM answers
def ask_medibot(messages):
    while True:
        res  = requests.post(URL, headers=HEADERS,
                 data=json.dumps({"model":"llama-3.3-70b-versatile",
                                  "max_tokens":800, "tools":TOOLS,
                                  "tool_choice":"auto", "messages":messages}))
        data   = res.json()["choices"][0]
        msg    = data["message"]
        reason = data["finish_reason"]

        if reason == "stop":                    # LLM finished → return answer
            return msg["content"]

        if reason == "tool_calls":              # LLM wants to search
            messages.append({"role":"assistant","content":msg.get("content"),
                              "tool_calls":msg["tool_calls"]})
            for tc in msg["tool_calls"]:        # Execute each search
                result = web_search(json.loads(tc["function"]["arguments"])["query"])
                messages.append({"role":"tool","tool_call_id":tc["id"],"content":result})

# ── Vision: Analyze Medicine Photo ───────────────────────
def analyze_photo(image_bytes):
    b64 = base64.b64encode(image_bytes).decode()   # image → base64 text
    res = requests.post(URL, headers=HEADERS, data=json.dumps({
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "max_tokens": 600,
        "messages": [{"role":"user","content":[
            {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
            {"type":"text","text":"Analyze this medicine. Give: name, uses, when to use, when NOT to use, side effects. Be brief and clear."}
        ]}]
    }))
    return res.json()["choices"][0]["message"]["content"]

# ── UI ────────────────────────────────────────────────────
st.markdown("<div class='title'>🩺 MediBot AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Describe symptoms OR upload a medicine photo</div>", unsafe_allow_html=True)

if not API_KEY:
    st.error("Set GROQ_API_KEY first → console.groq.com (free)")
    st.stop()

# Two tabs
tab1, tab2 = st.tabs(["💬 Symptom Checker", "💊 Medicine Photo"])

# ── Tab 1: Symptom Checker ────────────────────────────────
with tab1:
    st.markdown("<div class='warn'>⚠️ For informational use only. Always consult a doctor.</div>",
                unsafe_allow_html=True)

    symptoms = st.text_area("What symptoms do you have?",
                placeholder="e.g. headache, fever 101°F, sore throat since 2 days...",
                height=100)

    if st.button("🔍 Analyze Symptoms"):
        if symptoms.strip():
            with st.spinner("Searching medical database..."):
                answer = ask_medibot([
                    {"role":"system","content":"You are a medical assistant. Search for accurate info. Give: possible conditions, home remedies, medicines to consider. Keep it brief. End with: consult a doctor."},
                    {"role":"user","content":f"Symptoms: {symptoms}"}
                ])
            st.markdown(f"<div class='card'>{answer.replace(chr(10),'<br>')}</div>",
                        unsafe_allow_html=True)
        else:
            st.warning("Please describe your symptoms first.")

# ── Tab 2: Medicine Photo ─────────────────────────────────
with tab2:
    st.markdown("<div class='warn'>⚠️ Verify all medicine info with a pharmacist.</div>",
                unsafe_allow_html=True)

    photo = st.file_uploader("Upload medicine photo", type=["jpg","jpeg","png"])

    if photo:
        st.image(photo, width=280)
        if st.button("🔬 Analyze Medicine"):
            with st.spinner("Analyzing with Vision AI..."):
                result = analyze_photo(photo.read())
            st.markdown(f"<div class='card'>{result.replace(chr(10),'<br>')}</div>",
                        unsafe_allow_html=True)
