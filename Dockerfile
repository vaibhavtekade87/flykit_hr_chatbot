FROM python:3.10-slim

WORKDIR /app

# Install curl only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.backend.txt

# Install frontend dependencies
RUN pip install --no-cache-dir -r requirements.frontend.txt

# Expose ports
EXPOSE 7860
EXPOSE 8000

# Make startup script executable
RUN chmod +x /app/start.sh

# Run startup script
CMD ["/app/start.sh"]
