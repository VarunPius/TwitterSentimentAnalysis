# Project:
https://github.com/Silvertongue26/zookeeper_kafka_pyspark_polarity-analysis/blob/main/main.py

# ToDo:
Encrypt and decrypt access keys

# Technology used
- **Twitter API v2**: If you got your credentials (consumer_key, consumer_secret, access_token, access_secret) way to go champ!
- **Python 3.9**
- **Java JRE**: Java Runtime Environment (JRE) is a piece of software that is designed to run other software. As the runtime environment for Java, the JRE contains the Java class libraries, the Java class loader, and the Java Virtual Machine
- **Spark 3.2.1 with Hadoop 3.2.1**: Apache Spark is basically a computational engine that works with huge sets of data by processing them in parallel and batch systems. Spark is written in Scala, and PySpark was released to support the collaboration of Spark and Python.
- **Apache Kafka 3.1.0**: Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.
- **Apache Zookeeper 3.7.0 (stable version)**: ZooKeeper is a high-performance coordination service for distributed applications. It exposes common services — such as naming, configuration management, synchronization, and group services — in a simple interface so you don’t have to write them from scratch. You can use it off-the-shelf to implement consensus, group management, leader election, and presence protocols. And you can build on it for your own, specific needs.

# How it works? Producer.py, Consumer.py and Main.py files

1. To start with the streaming we must first run our servers(Zookeeper, Kafka, Spark), as we did before, we need to open three new terminals and in each, we start a different process.
    - Terminal 1: Type `zkserver`
    - Terminal 2: Move to `C:\KAFKA` and type `.\bin\windows\kafka-server-start.bat .\config\server.properties`
    - Terminal 3: Type `pyspark`

2. Create four files in your project folder:
    File 1: `auth_tokens.py`: Here we will store our Twitter API keys to be granted access to the twitter hell.
    File 2: `kafkaProducer.py`: This will be our Twitter data extractor, that will send the data to our consumer file
    File 3: `kafkaConsumer.py`: Here we will receive the information sent by our producer and prepare it for processing in our main.py file
    File 4: `main.py`: In this file we will make all our processing functions, data cleaning, sentiment analysis and parquet storage.

# Authentication 
We start with the `auth_tokens.py` file. In this file, we’ll declare our twitter keys (Not much to say in this file)

```
consumer_key = "YOUR KEY HERE"
consumer_secret = "YOUR KEY HERE"
access_token = "YOUR KEY HERE"
access_secret = "YOUR KEY HERE"
```

# Producer
Next, we use the `kafkaProducer.py`. 

1. We begin by importing the libraries:
```python
import auth_tokens as auth
import tweepy
import logging

from kafka import KafkaProducer
```

2. We generate the instance of our Kafka producer, our search term, and topic name, which we established up in our tutorial. Since we are using our computer as our host we will configure the Kafka producer with its default port 9092 -> `localhost:9092`.
```python
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],  api_version=(2, 0, 2))

search_term = 'elon musk'

topic_name = 'TW_ANALYSIS'
```

3. We define our tweeter authentication function
```python
def twitterAuth():
    # Create Twitter API authentication object
    authenticate = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
    # Access information for Twitter API
    authenticate.set_access_token(auth.access_token, auth.access_secret)
    # Api object creation
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    return api
```

4. We overwrite our tweet listener function in order to send information to our Kafka consumer
```python
#class TweetListener(tweepy.Stream):    #Older version code
class TweetListener(tweepy.StreamingClient):
    def on_data(self, raw_data):
        # Log data to TW_DEBUG.log
        logging.info(raw_data)

        # Send to our producer
        producer.send(topic_name, value=raw_data)

        return True

    def on_error(self, status_code):
        # Error if disconnect
        if status_code == 420:
            return False

    def start_streaming_tweets(self, search_term):
        # Start catching tweets from twitter, delete '[' and ']' for general search
        # self.filter(track=[search_term], languages=["en"]) #older version code
        self.add_rules(tweepy.StreamRule("Tweepy"))
        self.filter()
```

5. Now we write our main function where we call all the other functions we just wrote
```python
if __name__ == '__main__':
    # Creat loggong instance
    logging.basicConfig(filename='TW_DEBUG.log', encoding='UTF-8', level=logging.DEBUG)

    # TWitter API usage
    #twitter_stream = TweetListener(auth.consumer_key, auth.consumer_secret, auth.access_token, auth.access_secret)     #Older version code
    twitter_stream = TweetListener(auth.bearer_token)
    twitter_stream.start_streaming_tweets(search_term)
```

## Final Producer file:
```python
# Import libraries
import auth_tokens as auth
import tweepy
import logging

from kafka import KafkaProducer

# Generate Kafka producer/ localhost and 9092 default ports
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],  api_version=(2, 0, 2))

# Search name for twitter
search_term = 'elon musk'

# Topic name for Kafka tracing
topic_name = 'TW_ANALYSIS'

def twitterAuth():
    # Create Twitter API authentication object
    authenticate = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
    # Access information for Twitter API
    authenticate.set_access_token(auth.access_token, auth.access_secret)
    # Api object creation
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    return api

#class TweetListener(tweepy.Stream):    # Older API version code
class TweetListener(tweepy.StreamingClient):
    def on_data(self, raw_data):
        # Log data to TW_DEBUG.log
        logging.info(raw_data)

        # Send to our producer
        producer.send(topic_name, value=raw_data)

        return True

    def on_error(self, status_code):
        # Error if disconnect
        if status_code == 420:
            return False

    def start_streaming_tweets(self, search_term):
        # Start catching tweets from twitter, delete '[' and ']' for general search
        #self.filter(track=[search_term], languages=["en"])     # Older API version code
        self.add_rules(tweepy.StreamRule("Tweepy"))
        self.filter()


if __name__ == '__main__':
    # Creat loggong instance
    logging.basicConfig(filename='TW_DEBUG.log', encoding='UTF-8', level=logging.DEBUG)

    # TWitter API usage
    #twitter_stream = TweetListener(auth.consumer_key, auth.consumer_secret, auth.access_token, auth.access_secret)     # Older API version code
    twitter_stream = TweetListener(auth.bearer_token)
    twitter_stream.start_streaming_tweets(search_term)
```

# Consumer
Next, we start with the `kafkaConsumer.py`
With this script, we’ll catch the information that the Producer is sending us, and we’ll make it available to our main.py script

1. Import libraries and define our topic variable previously defined:
```python
from kafka import KafkaConsumer
import json

topic_name = 'TW_ANALYSIS'
```

2. We create or Kafka consumer instance and configure it so that the information received in hex is transformed to a readable string in JSON:
```python
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
```

## Final consumer code:
```python
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
```

# Main Spark code
This is the main code where Spark processing takes place. We write it in `main.py`. (The big one… not really)

In this file, we will start working with the information received from our Kafka consumer. We’ll go through a process of Data reading → Data preparation → Data cleaning → Subjectivity and polarity calculation (using the TextBlob) → Sentiment classification → Data storage. 
All in a day's work!

Let's start by importing libraries need for our tasks.
```Python
# Import libraries
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType, StructField, FloatType
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
import re
import logging
from textblob import TextBlob

import findspark
findspark.init()
```

## Data Reading
On our main function, we create our SparkSession instance and Kafka stream reader:
```python
if __name__ == "__main__":
    # Create logging file
    logging.basicConfig(filename='spark_tw.log', encoding='UTF-8', level=logging.INFO)

    # Spark object creation
    spark = SparkSession\
            .builder \
            .appName("Sentiment_Analysis_TW") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
            .getOrCreate()

    # Main spark reader in kafka format
    df = spark \
        .readStream \
        .format("kafka") \
        .option("subscribe", "TW_ANALYSIS")\
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .load()
```

## Data preparation
In here, we will convert the stream into a readable string and create the schema for the dataframe that will store it.
```python
    df.selectExpr("CAST(value AS STRING)")

    # Schema creation for new df values
    valSchema = StructType([StructField("text", StringType(), True)])

    # Creation and asignation of tweets text to new df
    values = df.select(from_json(df.value.cast("string"), valSchema).alias("tweets"))
    df1 = values.select("tweets.*")
```

## Functions definition
1. Once we have a data frame with which we can work, it's time to create the function that will clean all the link, emojis, usernames, etc. from the tweets we captured.
```python
def cleanTweet(tweet: str) -> str:
    tweet = re.sub(r'http\S+', '', str(tweet))
    tweet = re.sub(r'bit.ly/\S+', '', str(tweet))
    tweet = tweet.strip('[link]')

    # Remove users
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))

    # Remove punctuation
    my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@â'
    tweet = re.sub('[' + my_punctuation + ']+', ' ', str(tweet))

    # Remove numbers
    tweet = re.sub('([0-9]+)', '', str(tweet))

    # Remove hashtags
    tweet = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))

    # Remove extra simbols
    tweet = re.sub('@\w+', '', str(tweet))
    tweet = re.sub('\n', '', str(tweet))

    return tweet
```

2. Now that we are defining function, we should define our subjectivity, polarity and Sentiment classification functions. For this, we will use Textblob’s predefined functions. For more information on Textblob click here: https://textblob.readthedocs.io/en/dev/
```python
def Subjectivity(tweet: str) -> float:
    return TextBlob(tweet).sentiment.subjectivity

# TextBlob Polarity function
def Polarity(tweet: str) -> float:
    return TextBlob(tweet).sentiment.polarity

# Assign sentiment to elements
def Sentiment(polarityValue: int) -> str:
    if polarityValue < 0:
        return 'Negative'
    elif polarityValue == 0:
        return 'Neutral'
    else:
        return 'Positive'
```

## Subjectivity and polarity calculation and Sentiment classification
Now defined our functions, the next easy step is to calculate the subjectivity and polarity of each tweet, then classify it as positive, negative or neutral. So we add the next code segment to our main function:
```python
    cl_tweets = df1.withColumn('processed_text', clean_tweets_udf(col("text")))
    subjectivity_tw = cl_tweets.withColumn('subjectivity', subjectivity_func_udf(col("processed_text")))
    polarity_tw = subjectivity_tw.withColumn("polarity", polarity_func_udf(col("processed_text")))
    sentiment_tw = polarity_tw.withColumn("sentiment", sentiment_func_udf(col("polarity")))
```

## Data storage
- Finally! Now that we have calculated the polarity and we have a usefull dataframe we need to store it. For tis we will use the parquet format that can save us arroun a 75% of storage space. Really usefull of we are paying for storage. For this we can add the following segment on our main.py.
- To open parquet files and see its insides, I use ParquetViewer, you can download it here.
- NOTE: As you will see in the following code segments, I’ve set a wait time of 60 sec, this is for testing purposes, in production you should adjust this time according to your needs.
```python
    parquets = sentiment_tw.repartition(1)
    query2 = parquets.writeStream.queryName("final_tweets_parquet") \
        .outputMode("append").format("parquet") \
        .option("path", "./parc") \
        .option("checkpointLocation", "./check") \
        .trigger(processingTime='60 seconds').start()
    query2.awaitTermination(60)
```

## Final Consumer file
```python
# Import libraries
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType, StructField, FloatType
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
import re
import logging
from textblob import TextBlob

import findspark
findspark.init()


# Text cleaning function
def cleanTweet(tweet: str) -> str:
    tweet = re.sub(r'http\S+', '', str(tweet))
    tweet = re.sub(r'bit.ly/\S+', '', str(tweet))
    tweet = tweet.strip('[link]')

    # Remove users
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))

    # Remove punctuation
    my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@â'
    tweet = re.sub('[' + my_punctuation + ']+', ' ', str(tweet))

    # Remove numbers
    tweet = re.sub('([0-9]+)', '', str(tweet))

    # Remove hashtags
    tweet = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))

    # Remove extra simbols
    tweet = re.sub('@\w+', '', str(tweet))
    tweet = re.sub('\n', '', str(tweet))

    return tweet

# TextBlob Subjectivity function
def Subjectivity(tweet: str) -> float:
    return TextBlob(tweet).sentiment.subjectivity

# TextBlob Polarity function
def Polarity(tweet: str) -> float:
    return TextBlob(tweet).sentiment.polarity

# Assign sentiment to elements
def Sentiment(polarityValue: int) -> str:
    if polarityValue < 0:
        return 'Negative'
    elif polarityValue == 0:
        return 'Neutral'
    else:
        return 'Positive'

# Main function
if __name__ == "__main__":
    # Create logging file
    logging.basicConfig(filename='spark_tw.log', encoding='UTF-8', level=logging.INFO)

    # Spark object creation
    spark = SparkSession\
            .builder \
            .appName("Sentiment_Analysis_TW") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
            .getOrCreate()

    # Main spark reader in kafka format
    df = spark \
        .readStream \
        .format("kafka") \
        .option("subscribe", "TW_ANALYSIS")\
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .load()

    # Convert df's column value to string so we can manipulate it
    df.selectExpr("CAST(value AS STRING)")

    # Schema creation for new df values
    valSchema = StructType([StructField("text", StringType(), True)])

    # Creation and asignation of tweets text to new df
    values = df.select(from_json(df.value.cast("string"), valSchema).alias("tweets"))
    df1 = values.select("tweets.*")

    # User defined function creation from normal functions
    clean_tweets_udf = F.udf(cleanTweet, StringType())
    subjectivity_func_udf = F.udf(Subjectivity, FloatType())
    polarity_func_udf = F.udf(Polarity, FloatType())
    sentiment_func_udf = F.udf(Sentiment, StringType())

    # Tweet processing
    cl_tweets = df1.withColumn('processed_text', clean_tweets_udf(col("text")))
    subjectivity_tw = cl_tweets.withColumn('subjectivity', subjectivity_func_udf(col("processed_text")))
    polarity_tw = subjectivity_tw.withColumn("polarity", polarity_func_udf(col("processed_text")))
    sentiment_tw = polarity_tw.withColumn("sentiment", sentiment_func_udf(col("polarity")))

    # Final tweet logging
    query = sentiment_tw.writeStream.queryName("final_tweets_reg") \
        .outputMode("append").format("console") \
        .option("truncate", False) \
        .start().awaitTermination(60)

    # Parquet file dumping
    parquets = sentiment_tw.repartition(1)
    query2 = parquets.writeStream.queryName("final_tweets_parquet") \
        .outputMode("append").format("parquet") \
        .option("path", "./parc") \
        .option("checkpointLocation", "./check") \
        .trigger(processingTime='60 seconds').start()
    query2.awaitTermination(60)

    print("Process finished")
```

# TLDR:
- Run our servers in different terminals (Zookeper, Kafka, Spark).
- Run `kafkaProducer.py` on an independent terminal and let it run!
- Run `kafkaConsumer.py` on an independent terminal.
- Run `main.py` and watch your parquet files be generated with our dataframe.