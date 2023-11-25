FROM node:21-alpine as build-stage
WORKDIR /application
COPY ./src/package.json ./
RUN npm install
COPY ./src/ ./
RUN npm run build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /application/dist /application
