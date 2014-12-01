from modules import module

from datetime import datetime
import json
from map.models import Pushpin, Location

class Flickr(module.Module):
    ''' adapted from recon-ng Flickr module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        return

    def run(self, locname, lat, lon, rad):
        self.output("Collecting data from Flickr...")

        api_key = self.getKey('flickr_api')

        url = 'https://api.flickr.com/services/rest/'
        count = 0
        pins = []
        #self.heading(point, level=0)
        payload = {'method': 'flickr.photos.search', 'format': 'json', 'api_key': api_key, 'lat': lat, 'lon': lon, 'has_geo': 1, 'min_taken_date': '1990-01-01 00:00:00', 'extras': 'date_upload,date_taken,owner_name,geo,url_t,url_m', 'radius': rad, 'radius_units':'km', 'per_page': 500}
        processed = 0
        while True:
            try:
                resp = self.request(url, content=payload)
            except:
                # there was an error in the request
                self.error("Unable to connect to Flickr API.")
                break
            jsonobj = json.loads(resp.text[14:-1])
            # or a failure in the API
            if jsonobj['stat'] == 'fail':
                self.error(jsonobj['message'])
                break
            if not count: self.output('Collecting data for ~%s total photos...' % (jsonobj['photos']['total']))
            for photo in jsonobj['photos']['photo']:
                latitude = photo['latitude']
                longitude = photo['longitude']
                if not all((latitude, longitude)): continue
                source = 'Flickr'
                screen_name = photo['owner']
                profile_name = photo['ownername']
                profile_url = 'http://flickr.com/photos/%s' % screen_name
                try: media_url = photo['url_m']
                except KeyError: media_url = photo['url_t'].replace('_t.', '.')
                thumb_url = photo['url_t']
                message = photo['title']
                try: time = datetime.strptime(photo['datetaken'], '%Y-%m-%d %H:%M:%S')
                except ValueError: time = datetime(1970, 1, 1)
                pins.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
                count += 1
            processed += len(jsonobj['photos']['photo'])
            #self.verbose('%s photos processed.' % (processed))
            if jsonobj['photos']['page'] >= jsonobj['photos']['pages']:
                break
            payload['page'] = jsonobj['photos']['page'] + 1
        self.addPins(locname, pins)
        #self.summarize(new, count)
