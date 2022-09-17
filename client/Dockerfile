FROM node:16-alpine as build
ARG configuration=production

WORKDIR /usr/local/app

COPY package*.json .
COPY yarn.lock .
RUN yarn install --immutable

COPY . .

RUN yarn run build --output-path=./dist/out

FROM nginx:stable-alpine as final
EXPOSE 5001

COPY ./nginx.conf /etc/nginx/
COPY --from=build /usr/local/app/dist/out/ /usr/share/nginx/html
