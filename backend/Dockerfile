FROM python:3.14-slim

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade "setuptools>=78.1.1" "msgpack>=1.2.3" "urllib3>=2.8.0" \
 && pip install --no-cache-dir -r requirements.txt
COPY app.py .

RUN useradd --create-home appuser && mkdir /data && chown appuser /data
USER appuser

ENV DB_PATH=/data/shortlink.db
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "app:app"]
