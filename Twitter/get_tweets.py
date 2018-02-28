import tweepy
import configparser
import json


class BtcStreamListener(tweepy.StreamListener):

    tweets = []

    def on_status(self, status):
        self.tweets.append(status._json['text'])
        print(status._json['text'])
        if len(self.tweets) > 10:
            with open('test.txt', 'a', encoding='utf-8') as myfile:
                string = '\n\n\n\n\n\n'.join(self.tweets)
                myfile.write(string)
            self.tweets = []
            print("tweets appended")


def auth():
    try:
        config = configparser.ConfigParser()
        config.read("twitter_api_config.ini")

        consumer_key = config['twitter']['consumer_key']
        consumer_secret = config['twitter']['consumer_secret']
        access_token = config['twitter']['access_token']
        access_token_secret = config['twitter']['access_token_secret']
    except:
        print('Failed to get configs')
        return None

    try:

        auth_keys = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth_keys.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth_keys)
        return api
    except:
        print('Failed to authorize')
        return None


def get_tweets():

    api = auth()
    stream_listener = BtcStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=['bitcoin', 'btc', 'satoshi'], languages=['en'], async=True)


get_tweets()
