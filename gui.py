
import streamlit as st
import requests
import time

# -----------------------------------------------------------
# Configuration
# -----------------------------------------------------------
API_URL = "http://localhost:8000/query"

# -----------------------------------------------------------
# Page Config
# -----------------------------------------------------------
st.set_page_config(
    page_title="Flykite Airlines — HR Assistant",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------
# Custom CSS — Production Dark Theme
# -----------------------------------------------------------
st.markdown("""
<style>
    /* ── Hide Streamlit default chrome ── */
    #MainMenu, footer, .stDeployButton { display: none !important; }
    .block-container { padding-top: 0 !important; max-width: 760px !important; }

    /* ── Full page background ── */
    .stApp {
        background: #0a0e1a;
        min-height: 100vh;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ── Header ── */
    .header-container {
        text-align: center;
        padding: 48px 20px 32px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 36px;
    }
    .header-logo {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 3.5px;
        text-transform: uppercase;
        color: #5b7cfa;
        margin-bottom: 10px;
    }
    .header-title {
        font-size: 28px;
        font-weight: 300;
        color: #e8eaf0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        font-size: 13px;
        color: #4a5068;
        margin-top: 6px;
        font-weight: 400;
    }

    /* ── Input Area ── */
    .input-wrapper {
        position: relative;
        margin-bottom: 28px;
    }
    .stTextArea textarea {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        color: #e2e8f0 !important;
        font-size: 15px !important;
        padding: 18px 20px !important;
        resize: none !important;
        min-height: 80px !important;
        transition: border-color 0.3s ease !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    .stTextArea textarea:focus {
        border-color: #5b7cfa !important;
        box-shadow: 0 0 0 3px rgba(91,124,250,0.15) !important;
        outline: none !important;
    }
    .stTextArea textarea::placeholder { color: #3d4258 !important; }
    .stTextArea label { color: #4a5068 !important; font-size: 12px !important; letter-spacing: 1px !important; text-transform: uppercase !important; margin-bottom: 8px !important; }

    /* ── Submit Button ── */
    .stButton button {
        background: linear-gradient(135deg, #5b7cfa, #6366f1) !important;
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
        box-shadow: 0 6px 20px rgba(91,124,250,0.35) !important;
    }
    .stButton button:active { transform: translateY(0px) !important; }
    .stButton button:disabled {
        background: #1e2235 !important;
        color: #3d4258 !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ── Response Card ── */
    .response-card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 28px 24px;
        margin-top: 8px;
        animation: fadeSlideUp 0.4s ease;
    }
    .response-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .response-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #5b7cfa, #6366f1);
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
        color: #5b7cfa;
    }
    .response-time {
        font-size: 11px;
        color: #3d4258;
        margin-left: auto;
    }
    .response-question {
        font-size: 13px;
        color: #4a5068;
        margin-bottom: 14px;
        font-style: italic;
    }
    .response-answer {
        font-size: 15px;
        color: #c8ced9;
        line-height: 1.75;
        white-space: pre-wrap;
    }

    /* ── Loading Spinner ── */
    .loading-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 24px;
        background: #111827;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        margin-top: 8px;
    }
    .spinner {
        width: 20px;
        height: 20px;
        border: 2px solid #1e2235;
        border-top: 2px solid #5b7cfa;
        border-radius: 50%;
        animation: spin 0.7s linear infinite;
    }
    .loading-text { color: #4a5068; font-size: 14px; }

    /* ── Error Card ── */
    .error-card {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 8px;
        color: #f87171;
        font-size: 14px;
    }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        padding: 32px 20px 20px;
        font-size: 11px;
        color: #2a2f3f;
        letter-spacing: 0.5px;
    }

    /* ── Animations ── */
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
    <div class="header-logo">✈️ &nbsp; Flykite Airlines</div>
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
# -----------------------------------------------------------
if submit and question.strip():
    # Show loading state
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
    <div class="loading-container">
        <div class="spinner"></div>
        <span class="loading-text">Searching policies and generating response...</span>
    </div>
    """, unsafe_allow_html=True)

    try:
        start = time.time()
        # Call FastAPI backend
        resp = requests.post(API_URL, json={"question": question.strip()}, timeout=120)
        elapsed = time.time() - start
        resp.raise_for_status()
        data = resp.json()

        # Clear loading, show response
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

    except requests.exceptions.ConnectionError:
        loading_placeholder.empty()
        loading_placeholder.markdown("""
        <div class="error-card">
            ⚠️ Could not connect to the backend. Make sure the API server is running on port 8000.
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        loading_placeholder.empty()
        loading_placeholder.markdown(f"""
        <div class="error-card">
            ⚠️ Something went wrong: {str(e)}
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("""
<div class="app-footer">
    Flykite Airlines HR Policy Assistant &nbsp;·&nbsp; Powered by Llama 3.1 & RAG &nbsp;·&nbsp; Internal Use Only
</div>
""", unsafe_allow_html=True)
