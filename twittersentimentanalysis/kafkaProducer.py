######################################################################################################################################################
# Library Imports
######################################################################################################################################################

# System Libraries
import json
import logging

# User libraries
import auth_tokens as auth                      # File where creds are kept

# External librabries
import tweepy
from kafka import KafkaProducer


######################################################################################################################################################
# Config
######################################################################################################################################################

# Generate Kafka producer/ localhost and 9092 default ports
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(2, 0, 2))

# Search name for twitter
search_term = 'Trump'

# Topic name for Kafka tracing
topic_name = 'TW_ANALYSIS'


######################################################################################################################################################
# Code starts here
######################################################################################################################################################

"""
def twitterAuth():
    # Create Twitter API authentication object
    authenticate = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
    # Access information for Twitter API
    authenticate.set_access_token(auth.access_token, auth.access_secret)
    # Api object creation
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    return api
"""

class TweetListener(tweepy.StreamingClient):

    #def on_data(self, raw_data):
    #def on_tweet(self, raw_data):
    def on_status(self, raw_data):
        # Log data to TW_DEBUG.log
        logging.info(raw_data)

        # Printing tweets
        print(raw_data.text)

        """
        msg = json.loads( raw_data )
        if "extended_tweet" in msg:
            print("Full text: ", msg['extended_tweet']['full_text'])
        else:
            print("Text: ", msg['text'])
        """
        
        # Send to our producer
        #producer.send(topic_name, value=raw_data)

        return True

    def on_error(self, status_code):
        # Error if disconnect
        if status_code == 420:
            return False

    def start_streaming_tweets(self, search_term):
        # Start catching tweets from twitter, delete '[' and ']' for general search
        self.add_rules(tweepy.StreamRule(search_term))
        #print(self.get_rules())
        self.filter()
        #self.filter(track=[search_term], languages=["en"])
        #self.filter(tweet_fields=["referenced_tweets"])
        #self.delete_rules([1584762707890573312])
        #self.delete_rules([1578934793513099266])


if __name__ == '__main__':
    # Creat loggong instance
    logging.basicConfig(filename='TW_DEBUG.log', encoding='UTF-8', level=logging.DEBUG)

    # TWitter API usage
    #twitter_stream = TweetListener(auth.consumer_key, auth.consumer_secret, auth.access_token, auth.access_secret)
    twitter_stream = TweetListener(auth.bearer_token)
    twitter_stream.start_streaming_tweets(search_term)


######################################################################################################################################################
# Notes
######################################################################################################################################################

"""
API used: 
    tweepy.StreamingClient

add_rules parameters

Figure which is the correct method:
    on_data
    on_tweet
    on_status
"""