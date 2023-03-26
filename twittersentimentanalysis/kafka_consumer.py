# Import libraries
from kafka import KafkaConsumer
import json

topic_name = 'TW_ANALYSIS'

# Creata Kafka consumer, same default configuration frome the producer
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092'],
    api_version=(2, 0, 2),
    # Deserialize the string from the producer since it comes in hex
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Message loader from Json
for message in consumer:
    tweets = json.loads(json.dumps(message.value))
    print(tweets)

"""
Output:
{
    'data': {
        'edit_history_tweet_ids': ['1578953465573019648'], 
        'id': '1578953465573019648', 
        'text': '2022-10-09 03:40:16.270832 tweepy'
    }, 
    'matching_rules': [
        {'id': '1578934793513099266', 'tag': ''}
    ]
}
https://api.twitter.com/2/tweets/1578934793513099266
"""