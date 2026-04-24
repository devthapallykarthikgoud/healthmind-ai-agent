# 🩺 HealthMind AI Agent

### AI-Powered Healthcare Assistant using Streamlit + Groq + MCP + Multimodal LLM Reasoning

🔗 **Live Demo:** https://healthmind-ai-agent.streamlit.app/

---

## 📌 Project Overview

HealthMind AI Agent is a production-oriented AI healthcare assistant designed to provide early-stage medical guidance using Large Language Models (LLMs), Multimodal AI, and MCP (Model Context Protocol) principles.

The system helps users understand symptoms, analyze medicine images, identify possible health conditions, assess severity levels, and provide safe general healthcare guidance — while maintaining strict medical safety boundaries.

This project is built to simulate how real-world AI healthcare triage systems work by combining intelligent reasoning with tool-based execution instead of relying only on direct LLM responses.

Rather than acting as a simple chatbot, HealthMind AI behaves like an AI agent that can:

* Understand symptoms conversationally
* Identify medications from uploaded images
* Assess health severity levels
* Suggest safe OTC medicine categories
* Recommend when medical consultation is necessary
* Maintain healthcare safety guardrails

This makes it a strong real-world project for GenAI, Agentic AI, MCP, and LLM-based interview use cases.

---

## 🚀 Core Features

### 💬 Symptom Checker

Users can describe symptoms in natural language such as:

> “I have fever, headache, and sore throat for 2 days”

The system analyzes:

* Possible health conditions (non-diagnostic)
* Severity assessment (Mild / Moderate / Severe)
* Home remedies
* Safe OTC medicine suggestions
* Doctor consultation recommendations

---

### 💊 Medicine Photo Analyzer

Users can upload medicine images such as tablets, syrups, strips, or packaging.

The system provides:

* Medicine identification
* What the medicine is used for
* When to use it
* When NOT to use it
* Common precautions
* Common side effects

This uses multimodal LLM reasoning with image understanding.

---

### ⚠️ Healthcare Safety Layer

Because this is a healthcare project, strict safety rules are enforced:

* No direct diagnosis
* No dosage recommendations
* No prescription advice
* Emergency escalation for severe symptoms
* Strong disclaimer system

This makes the project safer and more realistic.

---

### 🧠 MCP-Based Agent Design

The system follows MCP (Model Context Protocol) architecture where:

```text
User Input
   ↓
MCP Controller
   ↓
Tool Selection
   ↓
LLM + Tool Reasoning
   ↓
Structured Safe Response
```

Instead of a normal chatbot flow:

```text
Prompt → Response
```

this project behaves like a true AI agent with decision-making and controlled tool execution.

---

## 🧠 Tech Stack

### Backend / Core AI

* Python
* Groq API
* Llama 3.3 70B Versatile
* Multimodal LLM Reasoning
* MCP (Model Context Protocol)
* Vision AI
* JSON Tool Calling Logic

---

### Frontend / UI

* Streamlit
* Custom CSS Styling
* Professional Medical UI Design
* Responsive Layout

---

### Deployment

* Streamlit Community Cloud
* GitHub Integration
* Secure API Secret Management

---

## 🔥 Why This Project is Strong

Most student healthcare chatbots simply call an API and print the answer.

This project is different because it focuses on:

### ✅ Real AI Agent Behavior

Instead of simple prompt-response flow

### ✅ Multimodal Understanding

Text + Image input support

### ✅ Healthcare Safety Design

Safe boundaries for medical assistance

### ✅ MCP Architecture Thinking

Tool orchestration + reasoning

### ✅ Production Deployment

Live deployed interview-ready system

This makes the project significantly stronger for:

* GenAI roles
* LLM Engineer roles
* AI/ML Engineer roles
* Applied Scientist interviews
* Product AI demonstrations

---

## ▶️ Run Locally

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 2 — Add API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ Never upload `.env` to GitHub.

---

### Step 3 — Run the Application

```bash
streamlit run medibot.py
```

---

## 🌐 Deployment

Recommended deployment platform:

### Streamlit Community Cloud

The application is fully deployment-ready and supports secure API key management using Streamlit Secrets.

---

## ⚠️ Disclaimer

This application is designed for informational and educational purposes only.

It does NOT replace professional medical advice, diagnosis, or treatment.

Always consult a qualified healthcare professional before taking medical action.

---

## 👨‍💻 Author

Built as an advanced AI Healthcare Assistant project focused on:

* Agentic AI
* MCP Systems
* LLM Engineering
* Multimodal AI
* Real-world Healthcare Use Cases

