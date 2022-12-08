FROM node:16
WORKDIR /code
COPY ./package.json .
COPY ./package-lock.json .
RUN npm install
COPY . .
EXPOSE 5173