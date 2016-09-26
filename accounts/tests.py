from django.test import TestCase

# Create your tests here.

client_id = '9890f2416a5ee83e8da8'
client_secret = '9ad5f139646112dd848a295b1b708730fe4152f2'

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

from requests_oauthlib import OAuth2Session

github = OAuth2Session(client_id)

authorization_url, state = github.authorization_url(authorization_base_url)
print(authorization_url)

redirect_response = "https://127.0.0.1:8000"

github.fetch_token(token_url, client_secret=client_secret, 
                   authorization_response=redirect_response)

r = github.get('https://api.github.com/user')
print(r.content)