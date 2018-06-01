import pandas as pd


def _intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


class Interests:
    def __init__(self, ints):
        self.interests = ints
        
    def get_interests(self, keywords):
        interests = []
        for col in self.interests.columns:
            if _intersection(keywords, self.interests[col]):
                interests.append(col)
        return interests
