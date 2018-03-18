# -*- coding: utf-8 -*-

'''
Courtesy of http://flask.pocoo.org/snippets/64/
'''

from flask_wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
import requests

from pytwisHandler import PytwisConst # Should come from pytwis
from pytwisHandler import PytwisHandler

pytwisHandler = PytwisHandler('http://127.0.0.1:4000/pytwis')

class SignInForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def check_login_credentials(self):
        '''
        Check the login credentials (username, password).
        '''
        # TODO: Check the login credentials (username, password) match 
        # the record in the backend database.

        # url = 'http://127.0.0.1:4000/pytwis?cmd=login&username=' + self.username.data + '&password=' + self.password.data
        status, response = pytwisHandler.sendRequest({PytwisConst.CMD:PytwisConst.CMD_LOGIN,
                                                      PytwisConst.USER_NAME: self.username.data,
                                                      PytwisConst.PASSWORD: self.password.data})

        if status == 200:
            return True
        else:
            return False

class PostTweetForm(Form):
    tweet = StringField('Tweet', validators=[DataRequired()])