FROM python:3.11-slim-bullseye


RUN apt update -y && apt install awscli -y


WORKDIR /app
COPY . /app


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

CMD ["python3", "app.py"]
