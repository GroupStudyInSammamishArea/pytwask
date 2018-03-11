import json
import requests
import urllib

## Copy PytwisConst from pytwis
## Need to make this a package
class PytwisConst:
    # Commands
    CMD_REGISTER = 'register'
    CMD_LOGIN = 'login'
    CMD_LOGOUT = 'logout'
    CMD_CHANGE_PASSWORD = 'changepassword'
    CMD_POST = 'post'
    CMD_FOLLOW = 'follow'
    CMD_UNFOLLOW = 'unfollow'
    CMD_FOLLOWERS = 'followers'
    CMD_FOLLOWINGS = 'followings'
    CMD_TIMELINE = 'timeline'

    # others
    AUTH = 'auth'
    CONFIRM_PASSWORD = 'new_confirmed_password'
    CMD = 'cmd'
    ERROR = 'error'
    FOLLOWEE = 'followee'
    MAX_TWEET_CNT = 'max_tweet_cnt'
    NEW_PASSWORD = 'new_password'
    OLD_PASSWORD = 'old_password'
    PASSWORD = 'password'
    TWEET = 'tweet'
    TWEETS = 'tweets'
    USERNAME = 'username'

class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class PytwisHandler(metaclass=Singleton):
    baseUrl = ''
    secreteKey = ''
    userName = ''

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl # 'http://127.0.0.1:4000/

    def sendRequest(self, params):
        if not self.secreteKey:
            url = self.baseUrl + '?' + urllib.parse.urlencode(params)
        else:
            url = self.baseUrl + '?' + urllib.parse.urlencode(params) + \
                  '&' + urllib.parse.urlencode({PytwisConst.AUTH : self.secreteKey})

        response = requests.get(url)

        if(response.status_code == 200): # need to change it macro
            dicResponse = json.loads(response.text)

            if(PytwisConst.AUTH in dicResponse):
                self.secreteKey = dicResponse[PytwisConst.AUTH] # Update auth secret key

            if (PytwisConst.USERNAME in dicResponse):
                self.userName = dicResponse[PytwisConst.USERNAME] # update a user name

            return response.status_code, dicResponse
        else:
            return response.status_code, ""

    def getUsername(self):
        return self.userName
