import pandas as pd
# import pickle
import os

from src.exceptions.UnableToLoadDataException import UnableToLoadDataException
from src.helpers.Paths import Paths
from json import load
from codecs import open as open_okved


class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataManager(metaclass=Singleton):
    """
    Singleton class which contains pre-loaded data for analytics
    """
    paths = ''
    work_skills = {}
    user_lnags = ['en', 'ru']
    jobs = {}
    
    def __init__(self):
        self._basepath = os.path.dirname(__file__)
        if len(self.work_skills.keys()) == 0:
            try:
                self.paths = Paths()
                self._import_tags_tables()
            except Exception as e:
                raise UnableToLoadDataException(e)

    # ------------- PUBLIC -------------

    def skills_weights_to_skills(self, skills_weights, lang):
        """
        Translates list of weights of skills to names of skills on specified language
        :param skills_weights: list of weights of skills
        :param lang: language code ('en' or 'ru')
        :return: list of names of skills (or professional categories)
        """
        try:
            return [self.work_skills.get('skill_names').get(lang)[i]
                    for i, w in enumerate(skills_weights) if w > 0]
        except Exception as e:
            raise UnableToLoadDataException(e)
    
    def skills_weights_to_skills_weights(self, skills_weights, lang):
        """
        Translates list of weights of skills to names of skills on specified language and returnes them with their
        weights in dict
        :param skills_weights: list of weights of skills
        :param lang: language code ('en' or 'ru')
        :return: list of names of skills (or professional categories) with corresponding weights in a form:
        {
            'name': skill name on specified language,
            'weight': skill weight
        }
        """
        try:
            return [{'name': self.work_skills.get('skill_names').get(lang)[i], 'weight': w}
                    for i, w in enumerate(skills_weights) if w > 0]
        except Exception as e:
            raise UnableToLoadDataException(e)

    # ------------- PRIVATE -------------

    def _import_tags_tables(self):
        """Loads lists of tags of different categories.
        """
        # WORK SKILLS
        work_skills_en = self._get_dict(self.paths.work_skills_en)
        work_skills_ru = self._get_dict(self.paths.work_skills_ru)
        self.work_skills = {
            "skill_names": {
                "en": list(work_skills_en.keys()),
                "ru": list(work_skills_ru.keys())
            },
            "jobs": {
                "en": list(work_skills_en.values()),
                "ru": list(work_skills_ru.values())
            }
        }
        # JOBS
        jobs_en = self._get_dict(self.paths.jobs_en)
        jobs_ru = self._get_dict(self.paths.jobs_ru)
        self.jobs = {
            'en': jobs_en['Jobs'],
            'ru': jobs_ru['Jobs']
        }
        # KEYWORDS
        keywords = self._get_df(self.paths.keywords)
        self.keywords = [keywords[col] for col in keywords.columns]
        self.kwd_cats = list(keywords.columns)
        # PROF NAMES
        profs = self._get_df(self.paths.prof_names)
        self.prof_names = [profs[col] for col in profs.columns]
        #STOPWORDS
        with open_okved(self._get_path(self.paths.stopwords), 'r', 'utf-8') as sw:
            self.stopwords = sw.read()
        #OKVED
        with open_okved(self._get_path(self.paths.okved), 'r', 'utf-8') as parsed_okved:
            self.okved = load(parsed_okved)
        #INTERESTS
        self.interests = self._get_df(self.paths.interests)
        
    def _get_df(self, path) -> pd.DataFrame:
        table = pd.read_csv(
            self._get_path(path), skip_blank_lines=True, keep_default_na=False, dtype=str, error_bad_lines=False)
        return table
    
    def _get_dict(self, path):
        table = self._get_df(path)
        res_dict = {}
        for col in table.columns:
            s = set(table[col])
            if '' in s:
                s.remove('')
            res_dict[col] = s
        return res_dict
    
    def _get_path(self, path):
        return os.path.abspath(os.path.join(self._basepath, "..", "..", path))