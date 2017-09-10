from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth
import requests
import os
import sys

SECRET_KEY = 'development key'
DEBUG = False
FACEBOOK_APP_ID = '159985207843693'
FACEBOOK_APP_SECRET = '7b111fdeb43cf6889725a849013d387c'

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


@app.route('/')
def index():
    return 'Welcome to FindMePitch' 


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    #print (resp['access_token'], '')
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me?fields=id,name,email')
    return 'Logged in as id=%s name=%s email=%s redirect=%s' % \
        (me.data['id'], me.data['name'], me.data['email'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run('0.0.0.0', port=port)