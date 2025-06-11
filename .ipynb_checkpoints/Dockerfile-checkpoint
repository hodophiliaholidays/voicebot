# Use official slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# System dependencies: ffmpeg for audio, git for pip installs
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports (not required for LiveKit Cloud agent, but kept for completeness)
EXPOSE 5000

# Set environment to production
ENV PYTHONUNBUFFERED=1

# Command to start the LiveKit agent
CMD ["python", "main.py", "start"]
