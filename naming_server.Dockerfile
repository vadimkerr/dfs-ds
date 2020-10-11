FROM python:3-alpine

COPY requirements.txt /tmp/
RUN python3 -m pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "naming_server.py"]
