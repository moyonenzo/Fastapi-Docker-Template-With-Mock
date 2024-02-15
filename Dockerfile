FROM python:3.10-bullseye

WORKDIR /app/
ADD requirements.txt /app/
ADD src/ /app/src/

RUN pip install -r requirements.txt
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes -subj "/C=XX/ST=France/L=Paris/O=ETNA/OU=ETNA/CN=ETNA"

EXPOSE 5000
CMD ["uvicorn", "src:app", "--reload", "--host", "0.0.0.0", "--port", "5000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]