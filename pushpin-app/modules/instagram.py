from modules import module
# unique to module
from datetime import datetime
import json
import re

class Instagram(module.Module):
    ''' adapted from recon-ng Instagram module
        written by Nathan Malcolm (@SintheticLabs)
        and Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        return

    def get_instagram_access_token(self):
        return self.get_explicit_oauth_token(
            'instagram',
            'basic',
            'https://instagram.com/oauth/authorize/',
            'https://api.instagram.com/oauth/access_token'
        )

    def run(self, locname, lat, lon, rad):
        self.output("Collecting data from Instagram...")
        access_token = self.get_instagram_access_token()
        url = 'https://api.instagram.com/v1/media/search'
        count = 0
        pins = []
        payload = {'lat': lat, 'lng': lon, 'distance': rad, 'access_token': access_token}
        processed = 0
        while True:
            resp = self.request(url, content=payload)
            jsonobj = json.loads(resp.text)
            # check for an erroneous request
            if jsonobj['meta']['code'] != 200:
                # check for an expired access token
                if jsonobj['meta']['code'] == 400:
                    # renew token
                    self.delete_key('instagram_token')
                    payload['access_token'] = self.get_instagram_access_token()
                    continue
                self.error(jsonobj['meta']['error_message'])
                break
            if not count: self.output('Collecting data for an unknown number of photos...')
            for item in jsonobj['data']:
                latitude = item['location']['latitude']
                longitude = item['location']['longitude']
                if not all((latitude, longitude)): continue
                source = 'Instagram'
                screen_name = item['user']['username']
                profile_name = item['user']['full_name']
                profile_url = 'http://instagram.com/%s' % screen_name
                media_url = item['images']['standard_resolution']['url']
                thumb_url = item['images']['thumbnail']['url']
                try: message = item['caption']['text']
                except: message = ''
                try: time = datetime.fromtimestamp(float(item['created_time']))
                except ValueError: time = datetime(1970, 1, 1)
                new.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
                count += 1
            processed += len(jsonobj['data'])
            #self.verbose('%s photos processed.' % (processed))
            if len(jsonobj['data']) < 20:
                #print len(jsonobj['data'])
                break
            payload['max_timestamp'] = jsonobj['data'][19]['created_time']
        self.addPins(locname, pins)
        #self.summarize(new, count)
