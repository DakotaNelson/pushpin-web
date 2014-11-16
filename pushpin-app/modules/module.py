from map.models import Keys
from django.core.exceptions import ValidationError
import requests
import json
import re

class ModuleException(Exception):
    pass

class Colors(object):
    N = '\033[m' # native
    R = '\033[31m' # red
    G = '\033[32m' # green
    O = '\033[33m' # orange
    B = '\033[34m' # blue

class Module:
    def __init__(self):
        return

    #======================================================
    # Key Management Methods
    #======================================================

    # retrieves keys from the database
    def getKey(self, name):
        # TODO one day add user control to keys/multiple users to app
        keys = Keys.objects.values(name)
        # potentially take list of values and return them all?

        if keys[0][name]:
            return keys[0][name]
        else:
            raise ModuleException("Key: " + name + " is not in database.")

    def addKey(self, name, key):
        # TODO: return only a user's keys (for multi-user use)
        keys = Keys.objects.get(user__username='test')
        setattr(keys, name, key)
        try: keys.clean()
        except ValidationError:
            raise ModuleException("Attempted to insert invalid key: " + name)
        keys.save()
        return

    #======================================================
    # Display Methods
    #======================================================

    def error(self, line):
        ''' formats and presents errors '''
        if not re.search('[.,;!?]$', line):
            line += '.'
        line = line[:1].upper() + line[1:]
        print('%s[!] %s%s' % (Colors.R, line, Colors.N))

    def output(self, line):
        '''Formats and presents normal output.'''
        print('%s[*]%s %s' % (Colors.B, Colors.N, line))

    #======================================================
    # Request Methods
    #======================================================

    def request(self, url, method="GET", timeout=None, payload=None, headers=None, cookiejar=None, auth=None, content='', redirect=True):
        if(method.lower() == "get"):
            r = requests.get(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
        elif(method.lower() == "post"):
            r = requests.post(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
        else:
            raise ModuleException("Only GET and POST requests are currently supported.")
            return None

        # TODO: Other things that would be nice to support:
        #request.user_agent = self.global_options['user-agent']
        #request.debug = self.global_options['debug']
        #request.proxy = self.global_options['proxy']

        if r.status_code == requests.codes.ok:
            return r
        else:
            raise ModuleException("Request to " + url + " returned with error " + str(r.status_code) + ".\n Response body: " + r.text)
            return None

    #======================================================
    # Request Methods
    #======================================================

    def get_twitter_oauth_token(self):
        try:
            return self.getKey('twitter_token')
        except:
            pass
        twitter_key = self.getKey('twitter_api')
        twitter_secret = self.getKey('twitter_secret')
        url = 'https://api.twitter.com/oauth2/token'
        auth = (twitter_key, twitter_secret)
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        payload = {'grant_type': 'client_credentials'}
        resp = self.request(url, method='POST', auth=auth, headers=headers, payload=payload)
        if 'errors' in resp.json():
            raise ModuleException('%s, %s' % (resp.json()['errors'][0]['message'], resp.json()['errors'][0]['label']))
        access_token = resp.json()['access_token']
        self.addKey('twitter_token', access_token)
        return access_token

    def search_twitter_api(self, payload):
        headers = {'Authorization': 'Bearer %s' % (self.get_twitter_oauth_token())}
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        results = []
        while True:
            resp = self.request(url, content=payload, headers=headers)
            jsonobj = resp.json()
            for item in ['error', 'errors']:
                if item in jsonobj:
                    self.error(jsonobj[item])
                    raise ModuleException(jsonobj[item])
            results += jsonobj['statuses']
            if 'next_results' in jsonobj['search_metadata']:
                max_id = urlparse.parse_qs(jsonobj['search_metadata']['next_results'][1:])['max_id'][0]
                payload['max_id'] = max_id
                continue
            break
        return results
