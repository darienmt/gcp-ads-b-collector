FROM python:3.7-alpine
WORKDIR /app
ADD main.py /app
ADD requirements.txt /app
ADD key.json /app

ENV GOOGLE_APPLICATION_CREDENTIALS=key.json

RUN pip install -r requirements.txt

CMD ["python", "main.py"]