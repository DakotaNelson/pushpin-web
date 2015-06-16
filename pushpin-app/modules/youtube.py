from modules import module
from datetime import datetime, timedelta, timezone

class Youtube(module.Module):
    ''' adapted from recon-ng Twitter module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        # every module needs a way to identify it
        self.name = "Youtube"
        return

    # returns a list of video IDs that are within the specified area since the specified date
    def search(self, key, lat, lon, rad, since):
        pageToken = None
        point = str(lat) + ',' + str(lon)
        stamp = since.isoformat('T')
        videoIds = []
        url = 'https://www.googleapis.com/youtube/v3/search' #?locationRadius={}km&order=date&publishedAfter={}&part=snippet&location={}&type=video&maxResults=50&key={}'
        while True:
            payload = {'locationRadius': str(rad) + 'km',
                       'order': 'date',
                       'publishedAfter': stamp,
                       'part': 'snippet',
                       'location': point,
                       'type': 'video',
                       'maxResults': '50',
                       'pageToken': pageToken,
                       'key': key}
            try:
                resp = self.request(url, content=payload)
            except:
                self.error("Unable to connect to Youtube API.")
                return []
            jsonobj = resp.json()
            if not jsonobj:
                self.error(resp.text)
                return []
            for video in jsonobj['items']:
                videoIds.append(video['id']['videoId'])
            # we've now processed a whole page
            if not 'nextPageToken' in jsonobj: return videoIds # no next page, we're done
            pageToken = jsonobj['nextPageToken']

    def run(self, locname, lat, lon, rad, since):
        self.output('Collecting data from Youtube for {}...'.format(locname))
        startTime = datetime.now(timezone.utc).astimezone()

        pins = []
        count = 0

        apiKey = self.getKey('google_api')

        videoIds = self.search(apiKey, lat, lon, rad, since)

        self.output('YouTube module collecting data for ~{} total videos...'.format(len(videoIds)))

        if len(videoIds) == 0: return

        for videoId in videoIds:
            geoPayload = {'part': 'snippet, recordingDetails',
                          'id': videoId,
                          'key': apiKey
                         }
            resp = self.request('https://www.googleapis.com/youtube/v3/videos', content=geoPayload)
            geoInfo = resp.json()
            if not geoInfo:
                self.error(resp.text)
                return

            video = geoInfo['items'][0]
            if len(geoInfo['items']) != 1: self.error("Got more than one video for query. Huh?")

            if not 'latitude' in video['recordingDetails']['location']:
                continue # if location isn't there, we don't even want it

            source = 'YouTube'
            screen_name = video['snippet']['channelTitle']
            profile_name = video['snippet']['channelTitle']
            profile_url = 'https://www.youtube.com/channel/{}'.format(video['snippet']['channelId'])
            media_url = 'https://www.youtube.com/watch?v={}'.format(video['id'])
            thumb_url = video['snippet']['thumbnails']['default']['url']
            message = video['snippet']['title']
            latitude = video['recordingDetails']['location']['latitude']
            longitude = video['recordingDetails']['location']['longitude']
            time = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # also potentially useful: video description
            # video['snippet']['description']

            pins.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
            count += 1
            if len(pins) == 200:
                # every 200, do a db dump
                self.output('YouTube module processed {} videos so far...'.format(count))
                self.addPins(locname, pins)
                pins = []

        # now that they're all processed
        self.addPins(locname, pins) # dump any left
        self.output("YouTube module has processed {} videos...".format(count))
        self.registerPull(locname, self.name, startTime)
        timeDelta = datetime.now(timezone.utc).astimezone() - startTime
        self.output("YouTube pull took {} seconds.".format(timeDelta.total_seconds()))
