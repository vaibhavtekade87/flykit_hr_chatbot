#!/bin/bash

# Start FastAPI in background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on port 7860 (HuggingFace default)
streamlit run gui.py --server.port=7860 --server.headless=true --browser.gatherUsageStats=false
