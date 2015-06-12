from modules import module
# unique to module
from datetime import datetime
import math

class Picasa(module.Module):
    ''' adapted from recon-ng Picasa module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        # every module needs a way to identify it
        self.name = "Picasa"
        return

    def run(self, locname, lat, lon, rad, since):
        self.output("Collecting data from Picasa...")
        startTime = datetime.now()

        url = 'http://picasaweb.google.com/data/feed/api/all'
        count = 0
        pins = []
        stamp = None
        # TODO get results since
        # This may not ever be implemented. Not like anyone uses Picasa anayway.
        kilometers_per_degree_latitude = 111.12
        # http://www.johndcook.com/blog/2009/04/27/converting-miles-to-degrees-longitude-or-latitude
        west_boundary = float(lon) - (math.cos(math.radians(float(lat))) * float(rad) / kilometers_per_degree_latitude)
        south_boundary = float(lat) - (float(rad) / kilometers_per_degree_latitude)
        east_boundary = float(lon) + (math.cos(math.radians(float(lat))) * float(rad) / kilometers_per_degree_latitude)
        north_boundary = float(lat) + (float(rad) / kilometers_per_degree_latitude)
        payload = {'alt': 'json', 'strict': 'true', 'bbox': '%.6f,%.6f,%.6f,%.6f' % (west_boundary, south_boundary, east_boundary, north_boundary)}
        processed = 0
        while True:
            try:
                resp = self.request(url, content=payload)
            except:
                self.error("Unable to connect to Picasa API.")
                return
            jsonobj = resp.json()
            if not jsonobj:
                self.error(resp.text)
                break
            if not 'entry' in jsonobj['feed']: break
            for photo in jsonobj['feed']['entry']:
                if not 'georss$where' in photo:
                    continue
                source = 'Picasa'
                screen_name = photo['author'][0]['name']['$t']
                profile_name = photo['author'][0]['name']['$t']
                profile_url = photo['author'][0]['uri']['$t']
                media_url = photo['content']['src']
                thumb_url = '/s72/'.join(media_url.rsplit('/', 1))
                message = photo['title']['$t']
                latitude = photo['georss$where']['gml$Point']['gml$pos']['$t'].split()[0]
                longitude = photo['georss$where']['gml$Point']['gml$pos']['$t'].split()[1]
                time = datetime.strptime(photo['published']['$t'], '%Y-%m-%dT%H:%M:%S.%fZ')
                pins.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
                count += 1
            processed += len(jsonobj['feed']['entry'])
            #self.verbose('%s photos processed.' % (processed))
            qty = jsonobj['feed']['openSearch$itemsPerPage']['$t']
            start = jsonobj['feed']['openSearch$startIndex']['$t']
            next = qty + start
            if next > 1000: break
            payload['start-index'] = next
        self.addPins(locname, pins)
        self.registerPull(locname, self.name, startTime)
        timeDelta = datetime.now() - startTime
        self.output("Picasa pull gathered {} photos.".format(count))
        self.output("Picasa pull took {} seconds.".format(timeDelta.total_seconds()))
        #self.summarize(new, count)
