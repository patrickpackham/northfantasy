# pull official base image
FROM python:3.9-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install system dependencies
RUN apt-get update && apt-get install -y libpq-dev python3-dev gcc libffi-dev git

# copy project
COPY ../ .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
