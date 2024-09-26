FROM node:20

WORKDIR /api-test-automation
COPY package.json package.json
COPY config.js config.js
COPY tests tests

RUN npm install

ENTRYPOINT ["npm"]