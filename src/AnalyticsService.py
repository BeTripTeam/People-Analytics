from src.analysis.IntAnalyzer import IntAnalyzer
from src.analysis.ProfAnalyzer import ProfAnalyzer
from src.controllers.AnalyzerController import AnalyzerController
from src.controllers.MiningController import MiningController
from src.exceptions.WrongRequestException import WrongRequestException
from src.helpers.DataManager import DataManager
from src.models.interests.Interests import Interests
from src.models.interests.Keywords import Keywords


class AnalyticsService:
    social_networks = ['vk', 'fb']
    langs = ['ru', 'en']
    
    def __init__(self):
        self.data_manager = DataManager()
        self.mining_controller = MiningController()
        self.analyzer_controller = AnalyzerController()
        
        self.prof_analyzer = ProfAnalyzer(Keywords(self.data_manager.keywords,
                                                   self.data_manager.kwd_cats,
                                                   self.data_manager.prof_names))
        self.interests_analyzer = IntAnalyzer(Interests(self.data_manager.interests))
    
    def get_user_info(self, social_network: str, user_access_token: str, user_lang: str) -> dict:
        """
        Returns information about a user
        :param social_network: Name of social network to look for user ('vk' of 'fb')
        :param user_access_token: Access token for the network
        :param user_lang: code of the language of a user to translate info (only 'en' or 'ru')
        :return: Info about user in a form:
            {
                'social_network':{
                    'name',
                    'id'
                },
                'first_name',
                'last_name',
                'employment':{
                    'company',
                    'position',
                    'description'
                },
                'occupation': #([work|school|university])#
                'prof_keywords',
                'prof_categories',
                'prof_needs'
            }
        where:
            social_network['name']: name of social network ('vk' of 'fb'),
            social_network['id']: id of user,
            --
            needs: listing of needs with weights,
            prof_keywords: dict of keywords for professional field
            prof_categories: professional categories
        """
        self._check_params(social_network, user_lang)
    
        user = self.mining_controller.get_user(social_network, user_access_token)
        prof_keywords, kwd_cats = self.prof_analyzer.get_prof_keywords(social_network, user)
        prof_needs = self.prof_analyzer.get_prof_needs(social_network, user)
        interests = self.interests_analyzer.get_interests(social_network, user)
        # To Return format
        result = {
            'social_network': {
                'name': social_network,
                'id'  : user.uid
            },
            "first_name": user.first_name, 'last_name': user.last_name, 'employment': user.employment,
            # 'skills': self._get_by_competences(competences, user.skills),
            # 'needs':  self._get_by_competences(competences, user.interests_from_skills),
            'prof_categories': kwd_cats,
            'prof_needs': prof_needs,
            'interests': interests,
            'prof_keywords'  : prof_keywords
        }
        return result

    def _check_params(self, social_network, user_lang):
        if social_network not in self.social_networks or user_lang not in self.langs:
            raise WrongRequestException('Wrong parameter value')
