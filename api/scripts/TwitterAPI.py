import requests
import pickle
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
import nltk
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from requests_oauthlib import OAuth1
from BasicAPI import BasicAPI


def lambda_handler(event, context):
    twitter = TwitterAPI(event['lat'], event['lon'])
    return twitter.get_latest_twitter()


class TwitterAPI(BasicAPI):

    type_name = 'twitter'
    # Dependency Issue in AWS
    twitter_classifier = pickle.load(open('data/CLASSIFIER.obj', 'rb'))

    def __init__(self, user_lat, user_lon, search_distance=BasicAPI.proximity_threshold):
        super(TwitterAPI, self).__init__(user_lat, user_lon, search_distance)
        self.latest_twitter = []

    def get_latest_twitter(self):  # Revise without tweepy
        ACCESS_TOKEN = BasicAPI.api_key['Twitter']['ACCESS_TOKEN']
        ACCESS_SECRET = BasicAPI.api_key['Twitter']['ACCESS_SECRET']
        CONSUMER_KEY = BasicAPI.api_key['Twitter']['CONSUMER_KEY']
        CONSUMER_SECRET = BasicAPI.api_key['Twitter']['CONSUMER_SECRET']
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        para = {'user_id': '307781209',
                'tweet_mode': 'extended'}
        result = requests.get(url, auth=auth, params=para)
        data = []
        for r in result.json():
            dct = {}
            dct['created_at'] = r['created_at']
            dct['full_text'] = r['full_text']
            data.append(dct)
        self.latest_twitter = data
        self.get_twitter_tag()
        return {'tweets': {'search_distance': self.search_distance,
                           'results': self.latest_twitter
                           }
                }

    def get_twitter_tag(self):
        for t in self.latest_twitter:
            t['tag'] = 'neg'
            if '[' in t['full_text']:
                t['tag'] = 'pos'
        for t in self.latest_twitter:
            if '[' not in t['full_text']:
                t['tag'] = TwitterAPI.twitter_classifier.classify(t['full_text'])
