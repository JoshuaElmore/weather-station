from abc import abstractmethod
from typing import Any
from fastapi import Response
from pydantic import BaseModel

class Sensor:

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get(self) -> Response:
        pass

    @abstractmethod
    def getRaw(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_sensore_name(self , name:str) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_summary(self) -> str:
        pass

    @abstractmethod
    def get_example_response(self) -> BaseModel:
        pass

    @abstractmethod
    def update_queue(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def main_loop(self, update_time:float) -> None:
        pass