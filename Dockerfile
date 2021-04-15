FROM python:3.9

LABEL maintainer "Nitesh Kumar <nkcse0007@gmail.com>"

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# Installing OS Dependencies
RUN apt-get update
RUN apt-get upgrade -y



# set up django app
RUN pip install -U pip setuptools
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

COPY . /code
ADD . /code
