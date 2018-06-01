

class WrongRequestException(Exception):
    def __init__(self, m=''):
        self.message = m