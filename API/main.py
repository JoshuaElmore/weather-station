from WeatherAPI import weatherAPI
from ltr390 import ltr390
from sht30 import sht31
from bmp390 import bmp390
from pmsa003i import pmsa003i
from raini2c import raini2c
from threading import Thread
from fastapi import FastAPI

api = weatherAPI()

# get the FastAPI object into main for the runtime to find.
app: FastAPI = api.app

temp = sht31()
Thread(target=temp.main_loop).start()

light = ltr390()
Thread(target=light.main_loop).start()

pressure = bmp390()
Thread(target=pressure.main_loop).start()

rain = raini2c()
Thread(target=rain.main_loop).start()

air = pmsa003i()
Thread(target=air.main_loop).start()


api.add_sensor(light)
api.add_sensor(temp)
api.add_sensor(pressure)
api.add_sensor(rain)
api.add_sensor(air)

api.add_router()