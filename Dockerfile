# Base Image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    chromium \
    chromium-driver \
    xvfb \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome binary path
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set display (important for headless)
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Default command
CMD ["pytest"]
