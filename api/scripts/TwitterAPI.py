import pickle
import tweepy

from BasicAPI import BasicAPI


def lambda_handler(event, context):
    pass


class TwitterAPI(BasicAPI):

    type_name = 'twitter'
    twitter_classifier = pickle.load(open('data/CLASSIFIER.obj', 'rb'))

    def __init__(self, arg):
        super(TwitterAPI, self).__init__()
        self.latest_twitter = []

    def get_latest_twitter(self):
        ACCESS_TOKEN = BasicAPI.api_key['Twitter']['ACCESS_TOKEN']
        ACCESS_SECRET = BasicAPI.api_key['Twitter']['ACCESS_SECRET']
        CONSUMER_KEY = BasicAPI.api_key['Twitter']['CONSUMER_KEY']
        CONSUMER_SECRET = BasicAPI.api_key['Twitter']['CONSUMER_SECRET']
        api = tweepy.API(tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET).set_access_token(ACCESS_TOKEN, ACCESS_SECRET))
        tweet = []
        for i in range(1):  # Only get nearest 200 * 20 per page
            rst = api.user_timeline('307781209', tweet_mode='extended', page=i)
            tweet += rst
        print(len(tweet))
