import influxdb_client, os, time,json,requests
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

import signal
import sys

#Graceful shutdown the script
def handle_sigterm(*args):
    print("SIGTERM received, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_URL")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket=os.environ.get("INFLUXDB_BUCKET")
location = os.environ.get("LOCATION_NAME")
weather_uri = os.environ.get("WEATHER_API_URI")

write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    time.sleep(60) # separate points by 60 second

    point = Point("weather").tag("location", location)

    try:
        request = requests.get(weather_uri, timeout=5)
        request.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        continue

    var = json.loads(request.text)

    for key, value in var.items():
        point.field(key, value)

    try:
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print(e)
        continue