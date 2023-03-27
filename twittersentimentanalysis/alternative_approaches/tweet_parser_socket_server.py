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
#                                                                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Library Imports goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# System Libraries
import json
import logging
import socket


# External librabries
from ruamel.yaml import YAML
import tweepy

# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Configurations goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# Twitter filter rules 
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Search name for twitter
search_term = '("TikTok")'


# Logging configurations
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logging.debug('This is a debug message')


######################################################################################################################################################
# Code starts here
######################################################################################################################################################


# Acess tokens and keys
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
def twitterAuth(env):
    yaml=YAML(typ='safe')                           # default, if not specfied, is 'rt' (round-trip)
    with open('../resources/config.yml', 'r') as file:
        config = yaml.load(file)
    consumer_key = config[env]['DeveloperKeys']['consumer_key']
    consumer_secret = config[env]['DeveloperKeys']['consumer_secret']
    access_token = config[env]['DeveloperKeys']['access_token']
    access_secret = config[env]['DeveloperKeys']['access_secret']
    bearer_token = config[env]['DeveloperKeys']['bearer_token']

    return bearer_token


# Tweet Listener
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
class TweetListener(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        logging.debug('On_Tweet method Called here')

        tweet_text = tweet.text.encode('utf-8')

        logging.debug('Tweet ID being processed:' + str(tweet.id))
        logging.debug('Before Socket Send')
        conn.send(tweet_text)
        logging.debug('After Socket Send')

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_errors(self, errors):
        print("Error:", errors)

    def on_connection_error(self):
        self.disconnect()

    def on_request_error(self, status_code):
        pass


def start_streaming_tweets(search_term):
    logging.debug('Inside start_streamingTweets')
    
    twitter_stream = TweetListener(bearer_token)
    twitter_stream.add_rules(tweepy.StreamRule(search_term))
    twitter_stream.filter()
    
    logging.debug('After filtering tweets')


if __name__ == '__main__':
    env = 'Dev'
    bearer_token = twitterAuth(env)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # initiate a socket object
    host = "127.0.0.1"                                               # local machine address
    port = 5555                                                      # specific port for your service.
    sock.bind((host, port))                                          # Binding host and port
    print("Now listening on port: %s" % str(port))
    sock.listen(5)                                                   #  waiting for client connection.
    
    try:
        global conn
        conn, addr = sock.accept()                                   # Establish connection with client.
                                                                     # it returns first a socket object conn, and the address bound to the socket
        print("Received request from: " + str(addr))
        data = conn.recv(1024)
        start_streaming_tweets(search_term)

    finally:
        sock.close()
        logging.debug('After socket close')

######################################################################################################################################################
# Notes
######################################################################################################################################################
