FROM python:3-slim

ENV APP_PATH=/var/app
ENV FLASK_ENV=development
ENV FLASK_APP=./main.py

RUN apt update
RUN apt install -y build-essential

RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH
COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

CMD flask run


