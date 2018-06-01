from typing import List

from src.exceptions.WrongRequestException import WrongRequestException
from src.models.user.AUser import AUser
from src.provider.FacebookProvider import FacebookProvider
from src.provider.VKProvider import VKProvider


class MiningController:
    def __init__(self):
        self.networks = {
            'fb': FacebookProvider(),
            'vk': VKProvider()
        }
        
    def get_user(self, network_name, access_token, uid="me") -> AUser:
        provider = self._get_provider(network_name)
        return provider.get_user(access_token, uid)
    
    def get_user_friends(self, network_name, access_token, uid) -> List[dict]:
        provider = self._get_provider(network_name)
        return provider.get_user_friends(access_token, uid)
    
    def get_user_friends_extended(self, network_name, access_token, uid='me') -> List[AUser]:
        provider = self._get_provider(network_name)
        return provider.get_user_friends_extended(access_token, uid)

    def _get_provider(self, network_name):
        return self.networks.get(network_name)