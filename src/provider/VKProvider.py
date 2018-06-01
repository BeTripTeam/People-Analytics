from typing import List

import time

from src.auth.VKAuth import VKAuth
from src.exceptions.VKException import VKException
from src.models.user.VKUser import VKUser
from .AProvider import AProvider


class VKProvider(AProvider):
    def __init__(self):
        pass
        
    def get_api(self, access_token):
        try:
            return VKAuth(access_token).get_api().get_api()
        except Exception as e:
            raise VKException()
    
    # ------------- PUBLIC -------------
    
    def get_user(self, access_token, uid='me') -> VKUser:
        
        api = self.get_api(access_token)
        
        u_fields = ['photo_id', 'career', 'occupation', 'activities', 'interests',
                    'music', 'movies', 'tv', 'books', 'games',
                    'about', 'education', 'universities', 'connections', 'schools']
        g_fields = ['description']
        
        try:
            if uid is 'me':
                user = api.users.get(fields=u_fields)
                time.sleep(1)
                groups = api.groups.get(extended=1, fields=g_fields)
                if not groups:
                    groups = {}
                time.sleep(1)
                wall = api.wall.get(extended=1, fields=g_fields)
                time.sleep(1)
                if 'id' in user[0].get('occupation', {}):
                    job_group = api.groups.getById(group_id=user[0].get('occupation').get('id'), fields=['description'])
                else:
                    job_group = {}
            else:
                user = api.users.get(user_ids=uid, fields=u_fields)
                if len(user) == 0:
                    raise VKException("User is empty")
                
                # For other person it still returns token owner's groups
                groups = {} #self._api.get_api().groups.get(user_ids=uid, extended=1, fields=['description'])
                time.sleep(1)
                wall = api.wall.get(owner_id=uid, extended=1)
                time.sleep(1)
                # Get group of company
                if 'id' in user[0].get('occupation', {}):
                    job_group = api.groups.getById(owner_id=uid, group_id=user[0].get('occupation').get('id'), fields=['description'])
                else:
                    job_group = {}
                    
            return VKUser(user, wall, groups, job_group)
        except VKException as e:
            raise e
        except Exception as e:
            raise VKException(e)
    
    def get_user_friends(self, access_token, uid='me'):
        api = self.get_api(access_token)
        try:
            return [{
                'id': user.get('id'),
                'first_name': user.get('first_name', ''),
                'last_name': user.get('last_name', '')
            } for user in self._get_user_friends(uid, api)]
        except Exception as e:
            raise VKException(e)
    
    def get_user_friends_extended(self, access_token, uid) -> List[VKUser]:
        api = self.get_api(access_token)
        try:
            u_fields = ['photo_id', 'career', 'occupation', 'activities', 'interests',
                        'music', 'movies', 'tv', 'books', 'games',
                        'about', 'education', 'universities', 'connections']
            friends = api.friends.get(fields=u_fields)
            if not friends: return []
            return [VKUser([friend], {}, {}, []) for friend in friends.get('items', [])]
        except Exception as e:
            raise VKException(e)

    # ------------- PRIVATE -------------
    
    def _get_user_friends(self, uid, api):
        u_fields = ['first_name', 'last_name']
        if uid is 'me':
            friends = api.friends.get(fields=u_fields)
        else:
            friends = api.friends.get(user_id=uid, fields=u_fields)
        if friends:
            return friends.get('items', [])
        else:
            return []
