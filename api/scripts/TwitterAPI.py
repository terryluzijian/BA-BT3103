import pickle
import tweepy

from BasicAPI import BasicAPI


def lambda_handler(event, context):
    twitter = TwitterAPI(event['lat'], event['lon'])
    return twitter.get_latest_twitter()


class TwitterAPI(BasicAPI):

    type_name = 'twitter'
    twitter_classifier = pickle.load(open('data/CLASSIFIER.obj', 'rb'))

    def __init__(self, user_lat, user_lon, search_distance=BasicAPI.proximity_threshold):
        super(TwitterAPI, self).__init__(user_lat, user_lon, search_distance)
        self.latest_twitter = []

    def get_latest_twitter(self):
        ACCESS_TOKEN = BasicAPI.api_key['Twitter']['ACCESS_TOKEN']
        ACCESS_SECRET = BasicAPI.api_key['Twitter']['ACCESS_SECRET']
        CONSUMER_KEY = BasicAPI.api_key['Twitter']['CONSUMER_KEY']
        CONSUMER_SECRET = BasicAPI.api_key['Twitter']['CONSUMER_SECRET']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
        tweet = []
        for i in range(1):  # Only get nearest 200 * 20 per page
            rst = api.user_timeline('307781209', tweet_mode='extended', page=i)
            tweet += rst
        result = []
        for t in tweet:
            dct = {}
            dct['text'] = t.full_text
            dct['time'] = t.created_at
            result.append(dct)
        self.latest_twitter = result
        self.get_twitter_tag(self.latest_twitter)
        return {'tweets': {'search_distance': self.search_distance,
                           'results': self.latest_twitter
                           }
                }

    def get_twitter_tag(self):
        for t in self.latest_twitter:
            t['tag'] = 'neg'
            if '[' in t['text']:
                t['tag'] = ['pos']
        for t in self.latest_twitter:
            if '[' not in t['text']:
                t['tag'] = TwitterAPI.twitter_classifier.classify(t['text'])
