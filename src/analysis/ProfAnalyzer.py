from src.helpers.TextProcessor import get_keywords_s, split_texts
from src.models.interests.Keywords import Keywords


class ProfAnalyzer:
    def __init__(self, keywords: Keywords):
        self.keywords = keywords
    
    def get_prof_keywords_vk(self, user):
        job, company, other_jobs, educations \
            = user.employment.get('position', ''), user.employment, user.jobs, user.educations
        
        job = [job.lower()] if job else []
        other_jobs = [j.lower() for j in other_jobs]
        educations = split_texts(educations, ['университет', 'институт'])

        desc_kwds = self._prepare_descriptive_keywords(user)

        wk, cats = self.keywords.get_weighted_keywords_counts(
            [
                job,
                other_jobs,
                educations,
                desc_kwds
            ],
            [
                1,
                0.5,
                0.6,
                0.3
            ]
        )
        return wk, cats

    def _prepare_descriptive_keywords(self, user):
        description = [
            user.interests,
            user.about,
            user.reposts_from,
            user.reposts_from_descr,
            user.posts,
            user.groups_names,
            user.groups_descr
        ]
        desc_kwds = []
        for desc in description:
            s = (' '.join(desc)).lower()
            if s:
                desc_kwds.extend(get_keywords_s(s))
        return desc_kwds

    def get_prof_keywords_fb(self, jobs, concentrations):
        jobs            = [j.lower() for j in jobs]
        concentrations  = [j.lower() for j in concentrations]
        
        wk, cats = self.keywords.get_weighted_keywords_counts(
            [
                jobs,
                concentrations
            ],
            [
                1,
                0.5
            ]
        )
        return wk, cats
    
    def get_prof_keywords(self, social_network, user):
        if social_network == 'vk':
            return self.get_prof_keywords_vk(user)
        if social_network == 'fb':
            return self.get_prof_keywords_fb(user.jobs, user.concentrations)
    
    def get_prof_cats(self, words):
        _, cats = self.keywords.get_weighted_keywords_counts([words], [1 for _ in words])
        return cats
        
    def is_head(self, job):
        for j in ['ceo', 'cto', 'head ', "manager", 'директор', 'менедж', 'глава'
                  'руководител', 'управляющий', 'основатель', 'founder', 'chief', 'executive']:
            if j in job:
                return True
        return False
    
    def get_prof_needs(self, sn, user):
        job = user.employment.get('position', '')
        needs = self.get_prof_needs_(job)
        if user.occupation == 'student':
            needs.append('стажировка')
        return needs
        
    def get_prof_needs_(self, job):
        if self.is_head(job):
            return ['поиск сотрудников', 'знакомства/связи', 'поиск работы', 'саморазвитие']
        return ['знакомства/связи', 'поиск работы', 'саморазвитие']

#
# from src.analysis.ProfAnalyzer import ProfAnalyzer
# kwds = Keywords([['meals', 'cook'], ['programming', 'pc']])
# pa = ProfAnalyzer(kwds)
# kw = pa.get_prof_keywords_vk('programmer', {'name': 'BeTrip', 'desc': ''}, ['waiter'], ['compute science'], ['programming', 'vk'])
# print(kw)
