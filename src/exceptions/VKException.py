

class VKException(Exception):
    def __init__(self, m=''):
        self.message = m