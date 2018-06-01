from src.helpers.DataManager import DataManager


class AUser(object):
    how_interested = 0
    user_lang = 'en'
    user_langs = []
    
    def __init__(self):
        self.uid = None
        self.last_name = None
        self.first_name = None
        self.user_langs = DataManager.user_lnags
        
        self.skills = []
        self.interests = []
        self.interests_from_skills = []
        self.child_skills_nums = []

        self.skills_weights = []
        self.interests_from_skills_weights = []
        
        self.employment = {
            'company': '',
            'position': ''
        }
        
    def __repr__(self):
        return "User: %s %s" % (self.first_name, self.last_name)

    def set_user_lang(self, lang: str):
        """
        Changes language of the user so that all the info about
        the user would be translated to that language if possible
        :param lang: language code
        """
        if lang in self.user_langs:
            self.user_lang = lang
    