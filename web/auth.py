#coding:utf8
import tornado.web
import requests
import db

GITHUB_CLIENT_ID = '218ea45c40986a65f61f'
GITHUB_CLIENT_SECRRET = '95ad8b3df244277c1a744c55ba15d1a4550a657b'
GITHUB_SCOPE = 'user'
GITHUB_STATE = 'YOU NEVER GUESS'
GITHUB_BASE = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN = 'https://github.com/login/oauth/access_token'
GITHUB_API = "https://api.github.com/user?access_token="

class login(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        pass

class logout(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie('username', '')
        self.render('login.html')
        
class authmiddler(tornado.web.RequestHandler):
    def require_login(self):
        if not self.get_cookie('username'):
            self.redirect('/login')

class oauth(tornado.web.RequestHandler):
    def get(self):
        re_url = GITHUB_BASE + '?client_id=' + GITHUB_CLIENT_ID + '&scope=' + GITHUB_SCOPE + '&state=' + GITHUB_STATE
        self.redirect(re_url)

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
            self.set_cookie("token", token['access_token'])

            users = db.mdb('topdf', 'user').perform()
            print token['access_token']
            if users.find_one({'username': user['login']}) == None:
                users.insert({'username': user['login'], 'token': token['access_token']})
            else:
                users.update({'username': user['login']},{'$set': {
                    'token': token['access_token']}    
                    })
            self.redirect('/people')
        else:
            self.redirect('/login')
            
class test(tornado.web.RequestHandler):
    def get(self):
        users = db.mdb('topdf', 'user').perform()
        print users.find_one({'username': "as"})
        self.write(users.find_one({'username': "as"}))
