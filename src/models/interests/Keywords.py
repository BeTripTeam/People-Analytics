from typing import Tuple, List

import numpy as np
import operator


def _intersection(lst1, lst2):
    s = set(lst1) & set(lst2)
    if '' in s:
        s.remove('')
    return list(s)


def _count(word_list):
    distinct_words = set(word_list)
    counts = np.array([word_list.count(word) for word in distinct_words])
    return dict([(w, c) for w, c in zip(distinct_words, counts)])


def _norm(arr: List[Tuple]):
    if not arr:
        return []
    weights = np.array([i[1] for i in arr])
    wm = weights.max()
    weights = weights / weights.max()
    return [(s, w) for w, s in zip(weights, [i[0] for i in arr])]


def _get_keywords(kw):
    kw = set(kw)
    kw.remove('')
    return list(kw)


class Keywords:
    def __init__(self, kwds, kwd_cats, prof_names):
        self.keywords = kwds
        self.kwd_cats = kwd_cats
        self.prof_names = prof_names
    
    def _get_count_by_cat(self, words):
        counts = [0] * len(self.kwd_cats)
        if words:
            for i, kwds in enumerate(self.keywords):
                i1 = _intersection(kwds, words)
                i2 = _intersection(self.prof_names[i], words)
                if i1 or i2:
                   counts[i] += len(i1) + len(i2)
        return np.array(counts)
    
    def get_weighted_keywords_counts(self, lists, weights):
        res_counts = np.array([0.0] * len(self.kwd_cats))
        for words, weight in zip(lists, weights):
            counts = self._get_count_by_cat(words)
            res_counts += counts * weight
        keywords = [(_get_keywords(self.keywords[i]), res_counts[i]) for i, c in enumerate(res_counts) if res_counts[i] > 0]
        kwd_cats = [(self.kwd_cats[i], res_counts[i]) for i, c in enumerate(res_counts) if res_counts[i] > 0]
        return sorted(_norm(keywords), key=operator.itemgetter(1), reverse=True), \
               sorted(_norm(kwd_cats), key=operator.itemgetter(1), reverse=True)
    
    