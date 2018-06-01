import vk

from src.exceptions.VKException import VKException
from src.models.API.API import API
from .Auth import Auth


class VKAuth(Auth):
    
    #access_token = '87cc1a32e7af1bb84adefc1e0f01570f6d08930c538a486b9d888cd0ff1910302c827e20284647e18cc61'
    _api = None
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.get_api()
    
    def get_api(self) -> API:
        if self._api is None:
            try:
                session = vk.Session(access_token=self.access_token)
                vk_api = vk.API(session, v='5.73')
                self._api = API(vk_api)
            except Exception as e:
                raise VKException(e)
        return self._api
