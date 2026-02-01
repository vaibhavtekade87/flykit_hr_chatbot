FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including gcc for llama-cpp-python
RUN apt-get update && apt-get install -y --no-install-recommends     curl     gcc     g++     make     cmake     && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.backend.txt
RUN pip install --no-cache-dir -r requirements.frontend.txt

# Expose both ports
EXPOSE 7860
EXPOSE 8000

# Make start.sh executable
RUN chmod +x /app/start.sh

# Run startup script
CMD ["/app/start.sh"]
