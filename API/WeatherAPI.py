from typing import Any, List
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from Sensor import Sensor


class weatherAPI:

    app: FastAPI
    router: APIRouter
    sensors: List[Sensor] = []

    def __init__(self) -> None:
        self.app = FastAPI(
            title="WeatherAPI",
            version="1.0.0",
            description="A simple API made by Joshua Elmore for geting data off a weather stasion runing on a Raspberry Pi",
        )

        self.router = APIRouter() 

    def add_sensor(self, sensor: Sensor):
        self.router.add_api_route(
            "/" + sensor.get_sensore_name() + "/",
            description=sensor.get_description(),
            endpoint=sensor.get,
            methods=["GET"],
            summary=sensor.get_summary(),
            response_model=sensor.get_example_response(),
        )

        self.sensors.append(sensor)

    def add_router(self) -> None:
        self.router.add_api_route(
            "/all/",
            endpoint=self.get_all_raw,
            description="This is method to get all of the values of the sensors atached if sensors have duplacket vlaues they are averaged",
            methods=["GET"],
        )

        self.router.add_api_route(
            "/",
            include_in_schema=False,
            endpoint=lambda: RedirectResponse(url='/docs')
        )        

        self.app.include_router(self.router)

    @staticmethod
    def combine_dicts(dict_list):
        combined_dict = {}
        for d in dict_list:
            for key, value in d.items():
                if key in combined_dict:
                    combined_dict[key].append(value)
                else:
                    combined_dict[key] = [value]
        for key, values in combined_dict.items():
            combined_dict[key] = sum(values) / len(values)
        return combined_dict

    def get_all_raw(self) -> dict[str, Any]:
        dict_list = []

        for s in self.sensors:
            dict_list.append(s.getRaw())

        combind_dict = weatherAPI.combine_dicts(dict_list)

        return JSONResponse(combind_dict)
