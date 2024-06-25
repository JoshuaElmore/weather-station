import time
from typing import Any
import board
import busio
import adafruit_bmp3xx
from collections import deque

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Sensor import Sensor

class bmp390(Sensor):
        
    i2c:busio.I2C
    sensor:adafruit_bmp3xx.BMP3XX_I2C

    data:deque[dict[str, Any]]

    def __init__(self) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bmp3xx.BMP3XX_I2C(self.i2c)
        self.data = deque(maxlen=3)

    def get(self):
        return JSONResponse(content=self.data[-1])
    
    def getRaw(self):
        return self.data[-1]
    
    def get_sensore_name(self,name = "pressure"):
        return name
    
    def get_summary(self) -> str:
        return "Get Pressure and Tempature"
    
    def get_description(self):
        return ("This is used to get the data from the LTR390 barometric pressure sensor <br><br>"+ 
        "<strong>Temperature</strong> is measured in C° with an accuracy of ±0.5°C.<br>"+
        "<strong>Pressure</strong> is measured in hectoPascals (hPa) with an accuracy of ±3 Pascals.<br>"+
        "<strong>Altitude</strong> is measured in meters with an accuracy of ±0.25 meters.")
    
    def get_example_response(self):
        return bmp390_default
    
    def update_queue(self) -> dict[str, Any]:
        data={
            "pressure": self.sensor.pressure ,
            "internal_temperature": self.sensor.temperature ,
            "altitude":self.sensor.altitude,
            }
        return data
         
    def main_loop(self,update_time = 1):

        while(True):
            self.data.append(self.update_queue())
            time.sleep(update_time)


class bmp390_default(BaseModel):
    pressure: float = Field(..., example=1002.8542979288461)
    internal_temperature: float = Field(..., example=24.224413672694936)
    altitude: float = Field(..., example=86.58501032365115)