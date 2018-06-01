from .AUser import AUser
from src.helpers.TextProcessor import split_text_to_words


class FbUser(AUser):
    def __init__(self, user, events, games, movies, music, television, books, groups):
        super().__init__()
        
        # Personal
        self.uid        = user.get('id')
        self.first_name = user.get('first_name', '')
        self.last_name  = user.get('last_name', '')
        
        # Skills
        self.languages = [lang.get('name', '') for lang in user.get('languages', [])]
        self.education = [school.get('school', {}).get('name', '') for school in user.get('education', [])]
        self.concentrations = []
        for school in user.get('education', []):
            self.concentrations.extend(c.get('name', '') for c in school.get('concentration', []))
        
        self.jobs = [job.get('position', {}).get('name', '') for job in user.get('work', [])]
        
        # Interests
        self.about  = split_text_to_words(user.get('about', ''))
        self.events = events
        self.books  = books
        self.groups = groups
        
        self.inspirational_people = [p.get('name', '') for p in user.get('inspirational_people', [])]
        self.favorite_athletes    = [a.get('name', '') for a in user.get('favorite_athletes', [])]
        self.favorite_teams       = [t.get('name', '') for t in user.get('favorite_teams', [])]
        self.sports               = [s.get('name', '') for s in user.get('sports', [])]
        
        self.games  = games
        self.movies = movies
        self.music  = music
        self.tv     = television
        
        if len(self.jobs) > 0:
            self.employment = {
                'company': user.get('work', {})[0].get('employer', {}).get('name', ''),
                'position': user.get('work', {})[0].get('position', {}).get('name', '')
            }
        self.occupation = ''