import tweepy
import auth_tokens as cred                      # File where creds are kept


auth = tweepy.OAuth1UserHandler(
   cred.consumer_key, cred.consumer_secret, cred.access_token, cred.access_secret
)


api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


client = tweepy.StreamingClient(cred.bearer_token)

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
client.add_rules(rules)


# we list our rules
response = client.get_rules()

for rule in response.data:
    print(rule)

# we delete one or more routes by passing their id
#client.delete_rules(['1639753517446619136'])

class IDPrinter(tweepy.StreamingClient):
    # we can get a response object
    def on_response(self, response):
        # It has the structure: StreamResponse(tweet, includes, errors, matching_rules)
        # So for each tweet, we have all the matching_rules
        print("# Response #:", response)
    # or we can just read the tweet
    def on_tweet(self, tweet):
        print("# Tweet #:", tweet.id, tweet.text)
    def on_errors(self, errors):
        print("# Error #:", errors)
    def on_connection_error(self):
        # what to do in case of network error
        self.disconnect()
    def on_request_error(self, status_code):
        # what to do when the HTTP response status code is >= 400
        pass

printer = IDPrinter(cred.bearer_token)
printer.filter()
