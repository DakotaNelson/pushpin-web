from map.models import Keys
import requests
import json
import re

class Colors(object):
    N = '\033[m' # native
    R = '\033[31m' # red
    G = '\033[32m' # green
    O = '\033[33m' # orange
    B = '\033[34m' # blue

class Module:
    def __init__(self):
        return

    # retrieves keys from the database
    def getKey(self, name):
        # TODO one day add user control to keys/multiple users to app
        keys = Keys.objects.values(name)
        # potentially take list of values and return them all?

        return keys[0][name]

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
        # TODO: don't ignore method
        if(method != "GET"):
            self.error("Only GET requests are currently supported.")
            return None

        # Other things that would be nice to support:
        #request.user_agent = self.global_options['user-agent']
        #request.debug = self.global_options['debug']
        #request.proxy = self.global_options['proxy']

        r = requests.get(url, params=payload, headers=headers, cookies=cookiejar, auth=auth, data=content, timeout=timeout)

        if r.status_code == requests.codes.ok:
            return r
        else:
            self.error("Request to " + url + " returned with error " + r.status_code)
            return None
