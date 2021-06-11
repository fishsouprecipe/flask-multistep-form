FROM python:3.8-slim-buster as builder
WORKDIR /flask-multistep-form
COPY requirements.txt ./requirements.txt

FROM builder AS prod
RUN : \
    && pip install --upgrade pip \
    && pip install -r requirements.txt
COPY app ./app

FROM builder AS tests
COPY requirements-tests.txt ./requirements-tests.txt
RUN : \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -r requirements-tests.txt
COPY app ./app
COPY tests ./tests
