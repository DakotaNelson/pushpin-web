from modules import module
from datetime import datetime, timedelta

class Twitter(module.Module):
    ''' adapted from recon-ng Twitter module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        # every module needs a way to identify it
        self.name = "Twitter"
        return

    def run(self, locname, lat, lon, rad, since):
        self.output('Collecting data from Twitter for {}...'.format(locname))
        startTime = datetime.now()

        url = 'https://api.twitter.com/1.1/search/tweets.json'
        count = 0
        pins = []
        threshold = 1000 # used to decide when to output status reports
        stamp = (since - timedelta(days=1)).strftime("%Y-%m-%d")
        # take a day off the "since" to make sure we don't lose anything - day granularity is a pain
        point = str(lat) + "," + str(lon)
        results = self.search_twitter_api({'q':'', 'geocode': '%s,%dkm' % (point, rad), 'count': '100', 'since':stamp}) # NOTE: this gets ALL the tweets before processing

        for tweet in results:
            if not tweet['geo']:
                continue
            tweet_id = tweet['id_str']
            source = 'Twitter'
            screen_name = tweet['user']['screen_name']
            profile_name = tweet['user']['name']
            profile_url = 'https://twitter.com/%s' % screen_name
            media_url = 'https://twitter.com/%s/statuses/%s' % (screen_name, tweet_id)
            thumb_url = tweet['user']['profile_image_url_https']
            message = tweet['text']
            latitude = tweet['geo']['coordinates'][0]
            longitude = tweet['geo']['coordinates'][1]
            time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            pins.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
            count += 1
            if count == threshold:
                threshold += 1000
                self.output('Twitter module processed {} tweets so far...'.format(count))
                self.addPins(locname, pins)
                pins = []
        self.addPins(locname, pins)
        self.registerPull(locname, self.name, startTime)
        timeDelta = datetime.now() - startTime
        self.output("Twitter pull gathered {} tweets.".format(count))
        self.output("Twitter pull took {} seconds.".format(timeDelta.total_seconds()))
        #self.verbose('%s tweets processed.' % (len(results)))
        #self.summarize(new, count)
