FROM python:3.10-slim

WORKDIR /app

# Install gcc and build tools needed for llama-cpp-python
RUN apt-get update && apt-get install -y --no-install-recommends     curl     gcc     g++     make     cmake     && rm -rf /var/lib/apt/lists/*

# Copy all project files into container
COPY . .

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.backend.txt

# Install frontend dependencies
RUN pip install --no-cache-dir -r requirements.frontend.txt

# Expose Streamlit port (HuggingFace default) and FastAPI port
EXPOSE 7860
EXPOSE 8000

# Make startup script executable
RUN chmod +x /app/start.sh

# Run the startup script which launches both services
CMD ["/app/start.sh"]
