FROM python:3.7.5

RUN ["mkdir", "-p", "/usr/src/app"]

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN ["pip3", "install", "--upgrade", "pip"]

RUN ["pip3", "install", "-r", "requirements.txt"]

COPY . .
