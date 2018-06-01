from .AUser import AUser
from src.helpers.TextProcessor import split_text_to_words
# import re
from datetime import datetime


class VKUser(AUser):
    
    def __init__(self, user, wall, groups, job_group):
        super().__init__()
        user = user[0]
        
        self.uid = 0
        self.last_name = self.first_name = ''
        
        self.activities = []
        self.occupation = {}
        self.interests  = []
        self.about      = []
        self.other_accounts = {
            'facebook' : '',
            'instagram': ''
        }
        self.jobs       = []
        self.educations = []
        self.job_groups = []
        self.groups     = {}
        self.posts      = []
        self.reposts_from       = []
        self.reposts_from_descr = []
        self.employment = {
            'company' : '',
            'position': '',
            'description': ''
        }
        try:
            # Personal
            self.uid = user.get('id')
            self.activities = split_text_to_words(user.get('activities', ''))
            self.interests  = split_text_to_words(user.get('interests' , ''))
            self.about      = split_text_to_words(user.get('about'     , ''))
    
            self.first_name = user.get('first_name')
            self.last_name  = user.get('last_name')
            self.other_accounts = {'facebook' : user.get('facebook',  ''),
                                   'instagram': user.get('instagram', '')}
            # Skills
            self.jobs       = [job.get('position', '')     for job in user.get('career', [])]
            self.educations = [uni.get('faculty_name', '') for uni in user.get('universities', [])]
            self.educations.extend([uni.get('chair_name', '') for uni in user.get('universities', [])])
            self.educations.extend([s.get('name', '') for s in user.get('schools', [])])
            self.educations.extend([s.get('speciality', '') for s in user.get('schools', [])])
            self.job_groups = [g.get('description', '') for g in job_group]
            self.occupation = user.get("occupation", {}).get('type', '')
            
            # Interests
            self.groups = [{'name': group.get('name', ''), 'description': group.get('description', '')} for group in
                           groups.get('items', [])]
            self.groups_names = [group.get('name', '') for group in groups.get('items', [])]
            self.groups_descr = [group.get('description', '') for group in groups.get('items', [])]
            self.posts  = [post.get('text', '') for post in wall.get('items', [])]
            self.reposts_from       = [r.get('name', '') for r in wall.get('groups', [])]
            self.reposts_from_descr = [r.get('description', '') for r in wall.get('groups', [])]
            # Employment
            if job_group:
                employer = job_group[0].get('name', '')
                description = job_group[0].get('description', '')
            else:
                employer = user.get('occupation', {}).get('name', '')
                description = ''
            if self.jobs:
                position = self.jobs[- 1]
            else:
                position = ''
            self.employment = {
                'company'    : employer,
                'position'   : position,
                'description': description
            }
            self.jobs.append(user.get('occupation', {}).get('name', ''))
            # Occupation
            if not self.occupation:
                if self.jobs:
                    self.occupation = 'work'
                else:
                    year = datetime.today().year
                    for uni in user.get('universities', []):
                        if uni.get('graduation') <= year:
                            self.occupation = 'student'
        except Exception as e:
            pass