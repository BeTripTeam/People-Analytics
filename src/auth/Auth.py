from abc import ABC, abstractmethod

from src.models.API.API import API


class Auth(ABC):
    @abstractmethod
    def get_api(self) -> API:
        pass
