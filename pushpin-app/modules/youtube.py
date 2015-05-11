from modules import module
from datetime import datetime

class Youtube(module.Module):
    ''' adapted from recon-ng Twitter module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        return

    def run(self, locname, lat, lon, rad):
        self.output("Collecting data from Youtube...")
        url = 'http://gdata.youtube.com/feeds/api/videos'
        count = 0
        pins = []
        point = str(lat) + ',' + str(lon)
        payload = {'alt': 'json', 'location': '%s!' % (point), 'location-radius': '%dkm' % (rad)}
        processed = 0
        while True:
            try:
                resp = self.request(url, content=payload)
            except:
                self.error("Unable to connect to Youtube API.")
            jsonobj = resp.json()
            if not jsonobj:
                self.error(resp.text)
                return
            if not 'entry' in jsonobj['feed']: break
            for video in jsonobj['feed']['entry']:
                if not video['georss$where']:
                    continue
                source = 'YouTube'
                screen_name = video['author'][0]['name']['$t']
                profile_name = video['author'][0]['name']['$t']
                profile_url = 'http://www.youtube.com/user/%s' % video['author'][0]['uri']['$t'].split('/')[-1]
                media_url = video['link'][0]['href']
                thumb_url = video['media$group']['media$thumbnail'][0]['url']
                message = video['title']['$t']
                latitude = video['georss$where']['gml$Point']['gml$pos']['$t'].split()[0]
                longitude = video['georss$where']['gml$Point']['gml$pos']['$t'].split()[1]
                time = datetime.strptime(video['published']['$t'], '%Y-%m-%dT%H:%M:%S.%fZ')
                pins.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
                count += 1
            processed += len(jsonobj['feed']['entry'])
            #self.verbose('%s photos processed.' % (processed))
            qty = jsonobj['feed']['openSearch$itemsPerPage']['$t']
            start = jsonobj['feed']['openSearch$startIndex']['$t']
            next = qty + start
            if next > 500: break
            payload['start-index'] = next
        self.addPins(locname, pins)
        #self.summarize(new, count)
