FROM python:3.10-bullseye

WORKDIR /app/
ADD requirements.txt /app/
ADD src/ /app/src/

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["uvicorn", "src:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]