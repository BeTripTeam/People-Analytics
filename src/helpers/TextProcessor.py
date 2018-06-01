import re
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer


def split_text_to_words(mystr):
    if mystr is not None:
        return re.sub("[^\w]", " ", mystr).split()
    return []


def split_texts(sents, stopwords):
    e = []
    for s in sents:
        e.extend(split_text_to_words(s.lower()))
    for sw in stopwords:
        if sw in e:
            e.remove(sw)
    e.extend(sents)
    return e


def find_s(arr):
    return [wt[0] for wt in arr if wt[1] == 'S']


def pos_tags_str(s):
    res = pos_tag(re.sub("[^\w]", " ", s).split(), lang='rus')
    return res


def pos_tags(arr):
    res = pos_tag(arr, lang='rus')
    return res


def get_keywords(s):
    return find_s(pos_tags(s))


def get_keywords_s(s):
    return find_s(pos_tags_str(del_rep_spaces(s)))


def del_rep_spaces(s):
    return re.sub(' +', ' ', s)


class TextProcessor:
    def __init__(self, stopwords):
        self.stopwords = stopwords
        
    def find_features(self, text):
        vec = TfidfVectorizer(ngram_range=(1, 2), stop_words=self.stopwords, norm='l2')
        vec.fit(text)
        return vec.get_feature_names()
