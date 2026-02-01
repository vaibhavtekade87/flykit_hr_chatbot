FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.backend.txt
RUN pip install --no-cache-dir -r requirements.frontend.txt

# Expose both ports
EXPOSE 7860
EXPOSE 8000

# Startup script — runs both FastAPI and Streamlit
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
