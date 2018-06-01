from typing import List

from abc import ABC, abstractmethod

from src.models.API.API import API
from src.models.user.AUser import AUser


class AProvider(ABC):
    
    @abstractmethod
    def get_user(self, access_token, uid) -> AUser:
        
        pass

    @abstractmethod
    def get_user_friends(self, access_token, uid) -> List[dict]:
        pass

    @abstractmethod
    def get_user_friends_extended(self, access_token, uid) -> List[AUser]:
        pass
