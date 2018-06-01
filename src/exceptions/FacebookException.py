class FacebookException(Exception):
    def __init__(self, m=''):
        super().__init__(m)
        self.message = m