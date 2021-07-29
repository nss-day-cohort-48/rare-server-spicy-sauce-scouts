class Login():
    """log in to the site"""
    def __init__(self, email, token, active):
        self.email = email
        self.token = token
        self.active = active