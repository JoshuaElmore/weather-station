import time
from typing import Any
import board
import busio
import adafruit_sht31d
from collections import deque

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Sensor import Sensor

class sht31(Sensor):
        
    i2c:busio.I2C
    sensor:adafruit_sht31d.SHT31D

    data:deque[dict[str, Any]]

    def __init__(self) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_sht31d.SHT31D(self.i2c)
        self.data = deque(maxlen=3)

    def get(self):
        return JSONResponse(content=self.data[-1])
    
    def getRaw(self):
        return self.data[-1]
    
    def get_sensore_name(self,name = "temp"):
        return name
    
    def get_summary(self) -> str:
        return "Get Tempature and Humidity"
    
    def get_description(self):
        return ("This is used to get the data from the SHT-30 tempature and humidity sensor <br><br>"+ 
        "<strong>Tempature</strong> is measured in C° with an accuracy of ±0.5°C.<br>"+
        "<strong>Relative Humidity</strong> is measured as a percentage with an accuracy of ±2%.")
    def get_example_response(self):
        return sht31_default
    
    def update_queue(self) -> dict[str, Any]:
        data={
            "temperature": self.sensor.temperature ,
            "relative_humidity": self.sensor.relative_humidity 
            }
        return data
         
    def main_loop(self,update_time = 1):

        while(True):
            self.data.append(self.update_queue())
            time.sleep(update_time)


class sht31_default(BaseModel):
    tempature: float = Field(..., example=26.409933623254744)
    relative_humidity: float = Field(..., example=40.404364080262454)