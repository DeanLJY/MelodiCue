FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y g++ cmake libssl-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

CMD ["python", "app.py", "--host=0.0.0.0"]
