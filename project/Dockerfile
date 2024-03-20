FROM python:3.12.0




WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
COPY ./requirements.txt /backend
RUN pip install -r requirements.txt

COPY . /backend

