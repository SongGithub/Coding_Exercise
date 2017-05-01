FROM python:2.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
Add . /code
WORKDIR /code
CMD ["python", "./src/main.py"]
