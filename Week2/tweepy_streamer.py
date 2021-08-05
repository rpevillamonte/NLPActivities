from time import time_ns
from typing import Text
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API, Cursor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from textblob import TextBlob

import twitter_credentials as tc

class TwitterClient():
    
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_tweet_by_keywords(self, keyword):
        tweets = []
        for tweet in Cursor(api.search, q=keyword, lang='tl').items(100):
            tweets.append(tweet)
        return tweets    

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        # return tweets to user
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets        
    
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
        auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    
    def __init__(self):
        self.ta = TwitterAuthenticator()
    
    """"Class for streaming and processing live Tweets."""
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        """This handles Twitter authentication and connection to the Twitter streaming API."""
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.ta.authenticate_twitter_app()
        
        stream = Stream(auth, listener)
        
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    """Basic listener class that prints received tweets to stdout."""
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, raw_data):
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
        #return super().on_data(raw_data)
        
    def on_error(self, status_code):
        if status_code == 420:
            # Return False on_data method in case rate limit occurs.
            return False
        print(status_code)
        #return super().on_error(status_code)
        
class TweetAnalyzer():
    """Functionality for analyzing and categorizing content from tweets."""
    
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        pl = analysis.sentiment.polarity
        
        if pl > 0:
            return 1
        elif pl == 0:
            return 0
        else:
            return -1
    
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['length'] = np.array([len(tweet.text) for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['created_at'] = np.array([tweet.created_at for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['language'] = np.array([tweet.lang for tweet in tweets])
        
        return df
                
if __name__ == "__main__":
    
    twitter_client = TwitterClient()
        
    ta = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    
    #tweets = api.user_timeline(screen_name='DOHgovph', count=200)
    tweets = twitter_client.get_tweet_by_keywords("#vaccine")
    df = ta.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([ta.analyze_sentiment(tweet) for tweet in df['Tweets']])
    
    sentiments = df['sentiment']
    for s in sentiments:
        print(s)
    
    #print(df.head(100))
    
    