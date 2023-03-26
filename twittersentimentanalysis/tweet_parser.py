######################################################################################################################################################
# Code Info                                                                                                                                          #
#                                                                                                                                                    #
# tweet_parser.py                                                                                                                                    #
# Author(s): Varun Pius Rodrigues                                                                                                                    #
# About: Reads tweets and adds/writes them to Kafka topic                                                                                            #
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                                                    #
# Change Log:                                                                                                                                        #
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Issue ID | Changed By                 | Resolution Date | Resolution                                                                               #
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# ARCH-001   Varun Pius Rodrigues         2023-03-25        Added new method `on_response` to fix tweet structure error                              #
# -------------------------------------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Library Imports goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# System Libraries
import json
import logging

# External librabries
from ruamel.yaml import YAML
import tweepy
from kafka import KafkaProducer     # //TODO: Check if needed

# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Configurations goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# Twitter filter rules 
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Search name for twitter
search_term = '("TikTok")'

# Alternate way to declare rules
rules = [
    # we add our rules here
    tweepy.StreamRule(
        '("black panther" OR #wakandaforever) (magnificent OR amazing OR excellent OR awesome OR great) -is:retweet',
        tag='black panther tribute'
    ),
    tweepy.StreamRule(
        '("tiktok")'
    )
]


# Logging configurations
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
logging.basicConfig(filename='../logs/TW_DEBUG.log', filemode='w', encoding='UTF-8', level=logging.DEBUG, format='%(levelname)s: %(message)s')
logging.debug('This is a debug message')

# These are the various other logging levels available
#logging.info('This is an info message')
#logging.warning('This is a warning message')
#logging.error('This is an error message')
#logging.critical('This is a critical message')


######################################################################################################################################################
# Code starts here
######################################################################################################################################################


# Acess tokens and keys
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
def twitterAuth():
    yaml=YAML(typ='safe')                           # default, if not specfied, is 'rt' (round-trip)
    with open('config.yml', 'r') as file:
        config = yaml.load(file)
    consumer_key = config['DeveloperKeys']['consumer_key']
    consumer_secret = config['DeveloperKeys']['consumer_secret']
    access_token = config['DeveloperKeys']['access_token']
    access_secret = config['DeveloperKeys']['access_secret']
    bearer_token = config['DeveloperKeys']['bearer_token']

    return bearer_token


"""
def twitterAuth_old():
    # Create Twitter API authentication object
    authenticate = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
    # Access information for Twitter API
    authenticate.set_access_token(auth.access_token, auth.access_secret)
    # Api object creation
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    return api
"""


# Logging configurations
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
class TweetListener(tweepy.StreamingClient):

    def on_response(self, response):
        # It has the structure: StreamResponse(tweet, includes, errors, matching_rules)
        # So for each tweet, we have all the matching_rules
        #print("# Response #:", response)
        logging.debug("Response: " + str(response.data))


    # or we can just read the tweet
    def on_tweet(self, tweet):
        #print("Tweet:", tweet.id, tweet.text)
        #logging.debug("Tweet ID: " + str(tweet.id) + " | Tweet:  " + tweet.text)
        #producer.send(topic_name, value=tweet.text)
        return tweet.text


    def on_status(self, raw_data):
        logging.info(raw_data)          # Doesnt't write to log as logging level is info 
                                        # while we have set logging level at initialization to debug
        return True


    def on_error(self, status_code):
        # Error if disconnect
        if status_code == 420:
            return False


    def on_errors(self, errors):
        print("# Error #:", errors)


    def on_connection_error(self):
        # what to do in case of network error
        self.disconnect()


    def on_request_error(self, status_code):
        # what to do when the HTTP response status code is >= 400
        pass


    def start_streaming_tweets(self, search_term):
        # Start catching tweets from twitter, delete '[' and ']' for general search
        # If  using `rules` from configuration, uncomment the following line to add list of rules:
        #self.add_rules(rules)
        self.add_rules(tweepy.StreamRule(search_term))
        
        # List of current rules for the API:
        #print(self.get_rules())
        # Delete rules from list of current rules for API
        #self.delete_rules([1584762707890573312])

        # Filter tweets as per the rules
        self.filter()
        #self.filter(track=[search_term], languages=["en"])
        #self.filter(tweet_fields=["referenced_tweets"])
        #self.delete_rules([1578934793513099266])


# Kafka 
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
def kafka_initializer():
    # Generate Kafka producer/ localhost and 9092 default ports
    global producer
    global topic_name
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                            value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    # Topic name for Kafka tracing
    topic_name = 'TW_ANALYSIS'
    return


if __name__ == '__main__':
#def parse_tweet():
    # Twitter API usage
    kafka_initializer()
    bearer_token = twitterAuth()
    twitter_stream = TweetListener(bearer_token)
    twitter_stream.start_streaming_tweets(search_term)


######################################################################################################################################################
# Notes
######################################################################################################################################################
