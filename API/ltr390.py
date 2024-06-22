import time
from typing import Any
import board
import busio
import adafruit_ltr390
from collections import deque

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Sensor import Sensor

class ltr390(Sensor):
        
    i2c:busio.I2C
    sensor:adafruit_ltr390.LTR390

    data:deque[dict[str, Any]]

    def __init__(self) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_ltr390.LTR390(self.i2c)
        self.data = deque(maxlen=3)

    def get(self):
        return JSONResponse(content=self.data[-1])
    
    def getRaw(self):
        return self.data[-1]
    
    def get_sensore_name(self,name = "light"):
        return name
    
    def get_summary(self) -> str:
        return "Get the UV index and other light related values"
    
    def get_description(self):
        return ("This is used to get the data from the LTR390 light sensor <br><br>"+
                "<strong>UVS</strong> is a raw dimensionless value.<br>"+
                "<strong>Ambient Light</strong> is a raw dimensionless value.<br>"+
                "<strong>UI Index</strong> is measured in milliwatt's per square meter (mW/m^2). <br>"+
                "<strong>LUX</strong> is measured in lumen's per meter squared (lm/m^2).")
    
    def get_example_response(self):
        return ltr390_default
    
    def update_queue(self) -> dict[str, Any]:
        data={
            "uvs": self.sensor.uvs ,
            "ambient_light": self.sensor.light ,
            "uv_index":self.sensor.uvi,
            "lux":self.sensor.lux
            }
        return data
         
    def main_loop(self,update_time = 1):

        while(True):
            self.data.append(self.update_queue())
            time.sleep(update_time)


class ltr390_default(BaseModel):
    uvs: int = Field(..., example=1)
    ambient_light: int = Field(..., example=62)
    uv_index: float = Field(..., example=0)
    lux: float = Field(..., example=56.800000000000004)