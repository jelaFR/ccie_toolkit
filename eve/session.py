from eve.request import APIRequest

class LoginSession():

    """
    This class create a login session to the EVE-NG server
    """
    def __init__(self, url, username="admin", password="eve", timeout=90):
        """
        Args:
            url (str): EVE-NG server url "http://eve-ng.example.com"
            user (str, optional): Username to log into GUI. Defaults to "admin".
            password (str, optional): Password to log into GUI. Defaults to "eve".
            timeout (int, optional): Maximum time to wait in order to connect. Defaults to 90.
        """
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.logged = False

    def username(self):
        """
        Returns username
        """
        return self.username

    def password(self):
        """
        Returns password
        """
        return self.password

    def login_state(self):
        """
        Check if user is logged
        """
        return self.logged

    def login(self):
        """
        Login into EVE NG through API and requests
        """
        loginUrl = self.url + "/api/auth/login"
        credentials = {'username':f'{self.username}', 'password':f'{self.password}'}
        session = APIRequest(loginUrl, credentials)
        cookie = session.post()
        return cookie