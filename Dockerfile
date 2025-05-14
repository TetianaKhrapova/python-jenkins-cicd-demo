FROM python:3.10-slim
WORKDIR /app
COPY app.py requirements.txt .
RUN pip install -r requirements.txt
