FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (git + build essentials)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip & install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

CMD ["python", "app.py"]
