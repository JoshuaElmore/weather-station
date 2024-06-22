FROM python:3.12-slim

ADD main.py .

RUN pip install influxdb-client requests

CMD [ "python", "./main.py" ]
