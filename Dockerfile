FROM python:2.7.12

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /