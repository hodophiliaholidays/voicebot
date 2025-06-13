# Use official slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Cloud Run's required port
EXPOSE 8080

# Start FastAPI server (and this triggers LiveKit in startup event)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
