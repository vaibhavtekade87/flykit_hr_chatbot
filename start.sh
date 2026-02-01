#!/bin/bash

# Start FastAPI backend in background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Wait for FastAPI to be ready before starting Streamlit
# Checks health endpoint every 10 seconds, max 30 attempts (5 minutes)
echo "Waiting for backend to be ready..."
for i in $(seq 1 30); do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "Backend is ready."
        break
    fi
    echo "Waiting... attempt $i/30"
    sleep 10
done

# Start Streamlit on port 7860 (HuggingFace default port)
streamlit run gui.py --server.port=7860 --server.headless=true --browser.gatherUsageStats=false
