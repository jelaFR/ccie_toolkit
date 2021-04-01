import requests
import json

class APIRequest():
    """
    Create API request
    """

    def __init__(self, url, data=dict(), cookie="", secure=False):
        """
        An API request

        Args:
            url (str): The url of the server without the http/https part (example : "apirequest.com")
            data (dict, optional): Data to include inside post/put requests
            cookie (str): Cookie for authentication
            secure (bool, optional): Uses HTTPs instead of HTTP. Defaults to False.
        """
        self.url = url
        self.cookie = cookie
        self.data = data
        self.secure = secure
        self.connected = False
        
    def get(self):
        """
        API GET request
        """
        try:
            api_result = requests.get(self.url, data=json.dumps(self.data), cookies=self.cookie)
            self.connected = True
            return api_result
        except:
            print(f"[KO] Unable to connect to URL {self.url}")
            return False


    def post(self):
        """
        API POST request
        """
        try:
            api_result = requests.post(self.url, data=json.dumps(self.data), cookies=self.cookie)
            if api_result.status_code == 200:
                self.connected = True
                return api_result.cookies
            else:
                self.connected = False
                return False
        except:
            print(f"[KO] Unable to connect to URL {self.url}")
            return False


    def put(self):
        """
        API PUT request
        """
        try:
            api_result = requests.put(self.url, data=json.dumps(self.data), cookies=self.cookie)
            self.connected = True
            return api_result
        except:
            print(f"[KO] Unable to connect to URL {self.url}")
            return False