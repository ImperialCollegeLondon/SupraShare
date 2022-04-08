FROM python:3.8-slim-buster as python

FROM python

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
CMD gunicorn example.graph:server -b :8050

EXPOSE 8050