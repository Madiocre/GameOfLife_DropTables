FROM node:18 AS build

WORKDIR /app/Client

COPY Client/package*.json ./

RUN npm install

COPY Client/ .

# RUN npm run lint -- --fix
RUN npm run build

FROM python:3.10-slim

WORKDIR /app

COPY Server/ .

RUN apt update && apt upgrade -y

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build /app/Client/dist ./static

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]