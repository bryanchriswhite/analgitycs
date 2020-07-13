FROM node:12-slim

ENV APP_PATH=/var/app

RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH
COPY ./package.json ./
COPY ./yarn.lock ./

#RUN apt update
#RUN apt install git node-gyp ...

#RUN npm -g i yarn

RUN yarn install

CMD yarn serve
