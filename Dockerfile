FROM python:3-slim

ENV ARANGO_URL=http://arango:8529
ENV APP_PATH=/var/app
ENV FLASK_ENV=development
ENV FLASK_APP=$APP_PATH/main.py

RUN apt update
RUN apt install -y build-essential

RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH
COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

CMD flask run


