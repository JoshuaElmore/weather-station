from __future__ import print_function

from DFRobot_RainfallSensor import *
import sys
import time
import time
from typing import Any
from collections import deque
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from Sensor import Sensor

sys.path.append("../")

class raini2c(Sensor):

    sensor:DFRobot_RainfallSensor_I2C

    data:deque[dict[str, Any]]

    runingCount:float

    def __init__(self) -> None:
        self.sensor = DFRobot_RainfallSensor_I2C()
        self.data = deque(maxlen=3)
        self.runingCount = self.sensor.get_rainfall()

    def get(self):
        return JSONResponse(content=self.data[-1])
    
    def getRaw(self):
        return self.data[-1]
    
    def get_sensore_name(self,name = "rain"):
        return name

    def get_summary(self) -> str:
        return "Get the ammount of rainfall in the last minute"
    
    def get_description(self):
        return ("This is used to get the data from tip bucket rain sensor <br><br>"+
                "<strong>rainfall</strong> the amount of rain that fell in the last minute in mm.<br>")
    
    def get_example_response(self):
        return raini2c_default
    
    def update_queue(self) -> dict[str, Any]:
        value = self.sensor.get_rainfall()-self.runingCount

        if value < 0:
            value = 0

        data={
            "rainfall": value
            }
        return data
         
    def main_loop(self,update_time = 60):

        while(True):

            self.data.append(self.update_queue())
            self.runingCount = self.sensor.get_rainfall()
            time.sleep(update_time)
    

class raini2c_default(BaseModel):
    rainfall: float = Field(..., example=3.0734)
