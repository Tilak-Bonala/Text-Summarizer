FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends awscli && \
    #rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

CMD ["python3", "app.py"]
