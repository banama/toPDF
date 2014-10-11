#coding:utf8
import tornado.web
import requests
import db
import hashlib

GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRRET
GITHUB_SCOPE = 'user'
GITHUB_STATE = 
GITHUB_BASE = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN = 'https://github.com/login/oauth/access_token'
GITHUB_API = "https://api.github.com/user?access_token="

DOUBAN_CLIENT_ID =
DOUBAN_CLIENT_SECRECT = 
DOUBAN_REDIRECT_URI = 'http://127.0.0.1:8888/jump/douban'
DOUBAN_SCOPE= 'douban_basic_common'
DOUBAN_BASE = 'https://www.douban.com/service/auth2/auth'
DOUBAN_TOKEN = 'https://www.douban.com/service/auth2/token'

class login(tornado.web.RequestHandler):
    def get(self):

        if not self.get_cookie('username') and not self.get_cookie('account'):
            self.render('login.html')
        else:
            self.redirect('/people')

    def post(self):
        account = str(self.get_arguments('account'))
        password = hashlib.sha1(''.join(self.get_arguments('password'))).hexdigest()
        users = db.mdb('topdf', 'user').perform()
        print type('account')
        _user = users.find_one({'account': account})
        if  _user == None:
            self.redirect('/login')
        elif _user['password'] != password:
            self.redirect('/login')
        else:
            self.set_cookie('account', account)
            self.redirect('/people')

class join(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie('username') and not self.get_cookie('account'):
            self.render('join.html')
        else:
            self.redirect('/people')

    def post(self):
        account = ''.join(self.get_arguments('account'))
        password = hashlib.sha1(''.join(self.get_arguments('password'))).hexdigest()
        users = db.mdb('topdf', 'user').perform()
        _user = users.find_one({'account': account})

        if  _user == None:
            users.insert({
                'account': account,
                'password': password
                })
            self.set_cookie('account', account)
            self.redirect('/people')
        else:
            self.redirect('/join')

class logout(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie('username', '')
        self.set_cookie('account', '')
        self.redirect('/')
    

class oauth(tornado.web.RequestHandler):
    def get(self, input):
        if input == 'github':
            re_url = GITHUB_BASE + '?client_id=' + GITHUB_CLIENT_ID + '&scope=' + GITHUB_SCOPE + '&state=' + GITHUB_STATE
            self.redirect(re_url)
        elif input == 'douban':
            re_url = DOUBAN_BASE + '?client_id=' + DOUBAN_CLIENT_ID + '&redirect_uri=' + DOUBAN_REDIRECT_URI + '&response_type=code&scope=' + DOUBAN_SCOPE
            self.redirect(re_url)
        else:
            self.redirect('/login')

class jump(tornado.web.RequestHandler):
    def get(self, input):
        if input == 'github':
            data = {
                'client_id': GITHUB_CLIENT_ID,
                'client_secret' : GITHUB_CLIENT_SECRRET
            }
            data['code'] = ''.join(self.get_arguments('code'))
            headers = {'Accept': 'application/json'}
            token = requests.post(GITHUB_TOKEN, data=data, headers = headers).json()
            user = requests.get(GITHUB_API + token['access_token'], headers = headers).json()

            self.set_cookie("username", user['login'])

            users = db.mdb('topdf', 'user').perform()
            if users.find_one({'username': user['login']}) == None:
                users.insert({'username': user['login'], 'token': token['access_token'], 'oauth':'github'})
            else:
                users.update({'username': user['login'], 'oauth': 'github'},{'$set': {
                    'token': token['access_token']}    
                    })
            self.redirect('/people')

        elif input == 'douban':
            data = {
                'client_id': DOUBAN_CLIENT_ID,
                'client_secret' : DOUBAN_CLIENT_SECRECT,
                'redirect_uri': DOUBAN_REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            data['code'] = ''.join(self.get_arguments('code')).encode('utf8')
            headers = {'Accept': 'application/json'}
            token = requests.post(DOUBAN_TOKEN, data=data, headers = headers).json()

            self.set_cookie("username", token['douban_user_name'].encode('utf8'))
            users = db.mdb('topdf', 'user').perform()
            if users.find_one({'username': token['douban_user_name']}) == None:
                users.insert({'username': token['douban_user_name'], 'token': token['access_token'], 'oauth':'github'})
            else:
                users.update({'username': token['douban_user_name'], 'oauth': 'github'},{'$set': {
                    'token': token['access_token']}    
                    })
            self.redirect('/people')
        else:
            self.redirect('/login')

class test(tornado.web.RequestHandler):
    def get(self):
        users = db.mdb('topdf', 'user').perform()
        print list(users.find())
        self.write('1')
