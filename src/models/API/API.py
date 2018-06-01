from abc import ABC, abstractmethod


class API:
    def __init__(self, api):
        self._api = api
    
    def get_api(self):
        return self._api
