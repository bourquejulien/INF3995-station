FROM node:16-alpine as build
ARG configuration=production

RUN apk add --no-cache chromium
ENV CHROME_BIN='/usr/bin/chromium-browser'

WORKDIR /usr/local/app

COPY package*.json ./
RUN yarn install

COPY . .

RUN yarn run build --output-path=./dist/out

FROM nginx:stable-alpine as final
EXPOSE 5001

WORKDIR /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/
COPY --from=build /usr/local/app/dist/out/ ./

FROM build as lint
ENTRYPOINT ["yarn", "run", "lint"]

FROM build as test
ENTRYPOINT ["yarn", "run", "test", "--browsers=ChromeHeadlessNoSandbox", "--watch=false"]
