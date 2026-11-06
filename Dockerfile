FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    FLET_FORCE_WEB_SERVER=true \
    PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
