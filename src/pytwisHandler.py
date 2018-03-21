import json
import requests
import urllib
from flask import session

## Copy PytwisConst from pytwis
## Need to make this a package
class PytwisConst:
    AUTH = 'auth'
    CHANGE_PASSWORD = 'changepassword'
    CONFIRM_PASSWORD = 'new_confirmed_password'
    CMD = 'cmd'
    ERROR = 'error'
    FOLLOW = 'follow'
    FOLLOWEE = 'followee'
    FOLLOWERS = 'followers'
    FOLLOWER_LIST = 'follower_list'
    FOLLOWINGS = 'followings'
    FOLLOWING_LIST = 'following_list'
    LOGIN = 'login'
    LOGOUT = 'logout'
    MAX_TWEET_CNT = 'max_tweet_cnt'
    NEW_PASSWORD = 'new_password'
    OLD_PASSWORD = 'old_password'
    PASSWORD = 'password'
    POST = 'post'
    REGISTER = 'register'
    TIMELINE = 'timeline'
    TWEET = 'tweet'
    TWEETS = 'tweets'
    UNFOLLOW = 'unfollow'
    USER_NAME = 'username'

    # Commands
    CMD_REGISTER = REGISTER
    CMD_LOGIN = LOGIN
    CMD_LOGOUT = LOGOUT
    CMD_CHANGE_PASSWORD = CHANGE_PASSWORD
    CMD_POST = POST
    CMD_FOLLOW = FOLLOW
    CMD_UNFOLLOW = UNFOLLOW
    CMD_FOLLOWERS = FOLLOWERS
    CMD_FOLLOWINGS = FOLLOWINGS
    CMD_TIMELINE = TIMELINE

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
    middleLayerBaseUrl = ''

    def __init__(self, middleLayerBaseUrl):
        self.middleLayerBaseUrl = middleLayerBaseUrl

    def sendRequest(self, params):
        if PytwisConst.AUTH in session:
            url = self.middleLayerBaseUrl + '?' + urllib.parse.urlencode(params) + \
                  '&' + urllib.parse.urlencode({PytwisConst.AUTH : session[PytwisConst.AUTH]})
        else:
            url = self.middleLayerBaseUrl + '?' + urllib.parse.urlencode(params)

        response = requests.get(url)

        if(response.status_code == 200): # need to change it macro
            dicResponse = json.loads(response.text)

            if(PytwisConst.AUTH in dicResponse):
                session[PytwisConst.AUTH] = dicResponse[PytwisConst.AUTH] # Update auth secret key

            if (PytwisConst.USER_NAME in dicResponse):
                session[PytwisConst.USER_NAME] = dicResponse[PytwisConst.USER_NAME] # update a user name

            return response.status_code, dicResponse
        else:
            return response.status_code, ""

    def getUsername(self):
        if PytwisConst.USER_NAME in session:
            return session[PytwisConst.USER_NAME]
        else:
            return "Not logged in yet."
