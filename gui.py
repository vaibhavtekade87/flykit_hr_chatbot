
import streamlit as st
import requests
import time

# -----------------------------------------------------------
# Configuration
# -----------------------------------------------------------
API_URL = "http://localhost:8000/query"
MAX_RETRIES = 3
RETRY_DELAY = 5

# -----------------------------------------------------------
# Page Config
# -----------------------------------------------------------
st.set_page_config(
    page_title="Flykite Airlines - HR Assistant",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------
# Custom CSS - Light Theme
# -----------------------------------------------------------
st.markdown("""
<style>
    #MainMenu, footer, .stDeployButton { display: none !important; }
    .block-container { padding-top: 0 !important; max-width: 760px !important; }

    .stApp {
        background: #f4f6f9;
        min-height: 100vh;
        font-family: 'Segoe UI', sans-serif;
    }

    .header-container {
        text-align: center;
        padding: 48px 20px 32px;
        border-bottom: 1px solid #dfe3ec;
        margin-bottom: 36px;
        background: #ffffff;
        border-radius: 0 0 16px 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .header-logo {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 3.5px;
        text-transform: uppercase;
        color: #3b5bdb;
        margin-bottom: 10px;
    }
    .header-title {
        font-size: 28px;
        font-weight: 300;
        color: #1a1f2e;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        font-size: 13px;
        color: #6b7280;
        margin-top: 6px;
    }

    .stTextArea textarea {
        background: #ffffff !important;
        border: 1px solid #dfe3ec !important;
        border-radius: 14px !important;
        color: #1a1f2e !important;
        font-size: 15px !important;
        padding: 18px 20px !important;
        resize: none !important;
        min-height: 80px !important;
        transition: border-color 0.3s ease !important;
        font-family: 'Segoe UI', sans-serif !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }
    .stTextArea textarea:focus {
        border-color: #3b5bdb !important;
        box-shadow: 0 0 0 3px rgba(59,91,219,0.12) !important;
        outline: none !important;
    }
    .stTextArea textarea::placeholder { color: #9ca3af !important; }
    .stTextArea label {
        color: #6b7280 !important;
        font-size: 12px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        margin-bottom: 8px !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #3b5bdb, #4c6ef5) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 32px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        cursor: pointer !important;
        width: 100% !important;
        transition: transform 0.15s ease, box-shadow 0.2s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(59,91,219,0.3) !important;
    }
    .stButton button:active { transform: translateY(0px) !important; }
    .stButton button:disabled {
        background: #e5e7eb !important;
        color: #9ca3af !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
        transform: none !important;
    }

    .response-card {
        background: #ffffff;
        border: 1px solid #dfe3ec;
        border-radius: 16px;
        padding: 28px 24px;
        margin-top: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        animation: fadeSlideUp 0.4s ease;
    }
    .response-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        padding-bottom: 14px;
        border-bottom: 1px solid #eef1f7;
    }
    .response-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #3b5bdb, #4c6ef5);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
    }
    .response-label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #3b5bdb;
    }
    .response-time {
        font-size: 11px;
        color: #9ca3af;
        margin-left: auto;
    }
    .response-question {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 14px;
        font-style: italic;
    }
    .response-answer {
        font-size: 15px;
        color: #374151;
        line-height: 1.75;
        white-space: pre-wrap;
    }

    .loading-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 24px;
        background: #ffffff;
        border: 1px solid #dfe3ec;
        border-radius: 16px;
        margin-top: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .spinner {
        width: 20px;
        height: 20px;
        border: 2px solid #e5e7eb;
        border-top: 2px solid #3b5bdb;
        border-radius: 50%;
        animation: spin 0.7s linear infinite;
    }
    .loading-text { color: #6b7280; font-size: 14px; }

    .error-card {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 8px;
        color: #dc2626;
        font-size: 14px;
    }

    .app-footer {
        text-align: center;
        padding: 32px 20px 20px;
        font-size: 11px;
        color: #9ca3af;
        letter-spacing: 0.5px;
    }

    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Header
# -----------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="header-logo">Flykite Airlines</div>
    <div class="header-title">HR Policy Assistant</div>
    <div class="header-subtitle">Ask anything about our company policies</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Input Section
# -----------------------------------------------------------
question = st.text_area(
    "Your Question",
    placeholder="e.g. What happens if my probation period is extended?",
    height=100,
    key="question_input"
)

submit = st.button("Ask", disabled=not question.strip())

# -----------------------------------------------------------
# Handle Submission
# Retry logic handles slow backend startup (model download)
# Retries 3 times with 5 second delay between attempts
# -----------------------------------------------------------
if submit and question.strip():
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
    <div class="loading-container">
        <div class="spinner"></div>
        <span class="loading-text">Searching policies and generating response...</span>
    </div>
    """, unsafe_allow_html=True)

    answer_received = False

    for attempt in range(MAX_RETRIES):
        try:
            start = time.time()
            # Call FastAPI backend with 300s timeout for model inference
            resp = requests.post(API_URL, json={"question": question.strip()}, timeout=300)
            elapsed = time.time() - start
            resp.raise_for_status()
            data = resp.json()

            # Show response card
            loading_placeholder.empty()
            loading_placeholder.markdown(f"""
            <div class="response-card">
                <div class="response-header">
                    <div class="response-icon">🤖</div>
                    <span class="response-label">Response</span>
                    <span class="response-time">{elapsed:.1f}s</span>
                </div>
                <div class="response-question">"{data['question']}"</div>
                <div class="response-answer">{data['answer']}</div>
            </div>
            """, unsafe_allow_html=True)
            answer_received = True
            break

        except requests.exceptions.ConnectionError:
            # Backend not ready yet, wait and retry
            if attempt < MAX_RETRIES - 1:
                loading_placeholder.markdown(f"""
                <div class="loading-container">
                    <div class="spinner"></div>
                    <span class="loading-text">Backend is starting up... retrying ({attempt + 1}/{MAX_RETRIES})</span>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(RETRY_DELAY)
            else:
                # All retries failed
                loading_placeholder.empty()
                loading_placeholder.markdown("""
                <div class="error-card">
                    Backend is not available. It may still be loading the model. Please wait a few minutes and try again.
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            # Any other error
            loading_placeholder.empty()
            loading_placeholder.markdown(f"""
            <div class="error-card">
                Something went wrong: {str(e)}
            </div>
            """, unsafe_allow_html=True)
            break

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("""
<div class="app-footer">
    Flykite Airlines HR Policy Assistant  |  Powered by Llama 3.1 and RAG  |  Internal Use Only
</div>
""", unsafe_allow_html=True)
