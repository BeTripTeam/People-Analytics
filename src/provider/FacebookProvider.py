from typing import List

import requests

from src.exceptions.FacebookException import FacebookException
from src.models.API.API import API
from src.models.user.FbUser import FbUser
from src.provider.AProvider import AProvider


class FacebookProvider(AProvider):
    _request_base = 'https://graph.facebook.com/v2.11/'
    
    _fields = 'first_name,last_name,about,education,favorite_athletes,' \
              'favorite_teams,inspirational_people,languages, sports,work'
    
    _edges_names = ['events', 'games', 'movies', 'music', 'television', 'books', 'groups']
    
    # ------------- PUBLIC -------------
    
    def get_user(self, access_token, uid='me') -> FbUser:
        try:
            request = f'{self._request_base}{uid}?fields={self._fields}&access_token={access_token}'
            user = requests.get(request).json()
            
            if 'error' in user:
                message = user.get('error').get("type", 'FacebookError') + ': '
                message = message + user.get('error').get("message", '')
                raise FacebookException(message)
            
            edges = [self._search_edge(edge, access_token, uid) for edge in self._edges_names]
            # feed = self._search_feed(uid)
            return FbUser(user, *edges)
        except FacebookException as e:
            raise e
        except Exception as e:
            raise FacebookException(e)
    
    def get_user_friends(self, access_token, uid='me'):
        """
        Returns friends in list of a form:
        [{
            "first_name": "João",
            "last_name": "Fernandes",
            "uid": "10153880234320990"
        }, ...]
        :param access_token: --
        :param uid: user id
        :return: list of dicts
        """
        try:
            return [{
                "uid": friend.get("id"),
                "first_name": friend.get("name", '').split(' ')[0],
                "last_name": friend.get("name", '').split(' ')[-1] if len(list(friend.get("name", ''))) > 1 else ''
            } for friend in self._get_user_friends(access_token, uid)]
        except FacebookException as e:
            raise e
        except Exception as e:
            raise FacebookException(e)
    
    def get_user_friends_extended(self, access_token, uid) -> List[FbUser]:
        try:
            return [self.get_user(access_token, friend.get('id')) for friend in self._get_user_friends(access_token, uid)]
        except FacebookException as e:
            raise e
        except Exception as e:
            raise FacebookException(e)
    
    # ------------- PRIVATE -------------
    
    # def _search_feed(self, uid):
    #     result = self._search_edge_raw('feed', uid=uid)
    #     feed = []
    #     for res in result:
    #         if 'message' in res:
    #             feed.append(res.get('message'))
    #     return feed
    
    def _search_edge(self, edge, access_token, uid='me'):
        result = self._search_edge_raw(edge, access_token, uid=uid)
        return [r.get('name') for r in result]
    
    def _search_edge_raw(self, edge, access_token, uid='me'):
        request = f'{self._request_base}{uid}/{edge}?access_token={access_token}'
        res = requests.get(request).json()
        
        if 'error' in res:
            raise FacebookException(res.get('error', {}).get('message', ''))
        
        result = (res.get('data', {}))
        if 'paging' in res:
            while 'next' in res.get('paging', {}):
                res = requests.get(res.get('paging').get('next')).json()
                result.extend(res.get('data', {}))
        return result
    
    def _get_user_friends(self, access_token, uid='me'):
        """
        Returns friends in list of a form:
        [{
            "name": "João Fernandes",
            "uid": "10153880234320990"
        },
        ...]
        :param uid: user id
        :return: list of dicts
        """
        friends = self._search_edge_raw('friends', access_token, uid)
        return friends
