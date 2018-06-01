from src.helpers.TextProcessor import get_keywords, split_text_to_words, split_texts
from src.models.interests.Interests import Interests
from src.models.user.FbUser import FbUser
from src.models.user.VKUser import VKUser


class IntAnalyzer:
    def __init__(self, interests: Interests):
        self.interests = interests
    
    def get_interests(self, social_network, user):
        ints = []
        if social_network == 'vk':
            ints = self.get_interests_vk(user)
        if social_network == 'fb':
            ints = self.get_interests_fb(user)
        return ints
    
    def get_interests_vk(self, user: VKUser):
        descr = [
            user.activities,
            user.interests,
            user.about,
            user.reposts_from,
            user.reposts_from_descr,
            user.posts,
            user.groups_names,
            user.groups_descr
        ]
        desc_kwds = []
        for d in descr:
            desc_kwds.extend(split_texts(d, []))
        return self.interests.get_interests(desc_kwds)
    
    def get_interests_fb(self, user: FbUser):
        interests = []
        if len(user.books) >= 10:
            interests.append('книги')
        if (len(user.favorite_athletes) +
            len(user.favorite_teams) +
            len(user.sports)
        ) >= 10:
            interests.append('спорт')
        if len(user.games) >= 10:
            interests.append('игры')
        if (len(user.movies) +
            len(user.tv)
        ) >= 10:
            interests.append('кино и телевидение')
        if len(user.music) >= 10:
            interests.append('музыка')
        if len(user.education) > 5:
            interests.append('образование')
        keywords = get_keywords(user.about)
        interests.extend(self.interests.get_interests(keywords))
        return interests
