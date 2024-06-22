import time
from typing import Any
import board
import busio
from adafruit_pm25.i2c import PM25_I2C
from collections import deque

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Sensor import Sensor

class pmsa003i(Sensor):
        
    i2c:busio.I2C
    sensor:PM25_I2C

    data:deque[dict[str, Any]]

    key_map = {
        "pm10 standard": "pm10_standard",
        "pm25 standard": "pm25_standard",
        "pm100 standard": "pm100_standard",
        "pm10 env": "pm10_env",
        "pm25 env": "pm25_env",
        "pm100 env": "pm100_env",
        "particles 03um": "particles_0_3um",
        "particles 05um": "particles_0_5um",
        "particles 10um": "particles_1um",
        "particles 25um": "particles_2_5um",
        "particles 50um": "particles_5um",
        "particles 100um": "particles_10um",
    }

    @staticmethod
    def replace_keys(dict1, key_map):
        return {key_map.get(key, key): value for key, value in dict1.items()}

    def __init__(self) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = PM25_I2C(self.i2c , None)
        self.data = deque(maxlen=3)

    def get(self):
        return JSONResponse(content=self.data[-1])
    
    def getRaw(self):
        return self.data[-1]
    
    def get_sensore_name(self,name = "air_quality"):
        return name
    
    def get_summary(self) -> str:
        return "Get air quality data from the PMSA003I sensor."
    
    def get_description(self):
        return ("This is used to get the data from the LTR390 light sensor <br><br>"+
                "<strong>pmXX_standard</strong> is the particulate matter concentration in standard units. For a give size partical.<br>"+
                "<strong>pmXX_env</strong> is the particulate matter concentration in environmental units. For a give size partical.<br>"+
                "<strong>particles_XXum</strong> is the Particulate matter per 0.1L in. <br>")
    
    def get_example_response(self):
        return pmsa003i_default
    
    def update_queue(self) -> dict[str, Any]:
        try:
            aqdata = self.sensor.read()
            # print(aqdata)
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            return None
        
        data = self.replace_keys(aqdata, self.key_map)

        return data
         
    def main_loop(self,update_time = 1.1):

        while(True):
            self.data.append(self.update_queue())
            time.sleep(update_time)

class pmsa003i_default(BaseModel):
    pm10_standard: int = Field(..., example=8)
    pm25_standard: int = Field(..., example=10)
    pm100_standard: int = Field(..., example=10)
    pm10_env: int = Field(..., example=8)
    pm25_env: int = Field(..., example=10)
    pm100_env: int = Field(..., example=10)
    particles_0_3um: int = Field(..., example=1245)
    particles_0_5um: int = Field(..., example=365)
    particles_1um: int = Field(..., example=44)
    particles_2_5um: int = Field(..., example=0)
    particles_5um: int = Field(..., example=0)
    particles_10um: int = Field(..., example=0)