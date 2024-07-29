from fastapi import Form


class OAuth2UsernamePasswordRequestForm:
    def __init__(self, username: str = Form(...), password: str = Form(...)):
        self.username = username
        self.password = password
