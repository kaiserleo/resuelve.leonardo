FROM python:3.6

LABEL author_name="Leonardo de la Cerda"
LABEL author_email="leobiwakenobi@gmail.com"

RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
