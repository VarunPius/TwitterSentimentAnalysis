import tweepy
import auth_tokens as cred                      # File where creds are kept


auth = tweepy.OAuth1UserHandler(
   cred.consumer_key, cred.consumer_secret, cred.access_token, cred.access_secret
)


api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)



# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

import multiprocessing as mp
import random
import time

def number_generator(queue):
    while True:
        queue.put(random.randint(1,100))
        time.sleep(0.5)

def another_method(queue):
    while True:
        data = queue.get()
        # write data to Kafka topic
        print(data)

if __name__ == '__main__':
    queue = mp.Queue()
    p1 = mp.Process(target=number_generator, args=(queue,))
    p2 = mp.Process(target=another_method, args=(queue,))
    p1.start()
    p2.start()



You can use a multiprocessing queue to share data between two files in Python.
The multiprocessing.Queue class provides a way to share data between processes.
You can create a queue object in one file and pass it to another file as an argument.
Here’s an example of how you can use it:

from multiprocessing import Process, Queue

def writer(q):
    q.put('hello')

def reader(q):
    print(q.get())

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=writer, args=(q,))
    p2 = Process(target=reader, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
In this example, we create a queue object q and pass it as an argument to both the writer and reader functions.
The writer function puts a string 'hello' into the queue using the put() method.
The reader function reads from the queue using the get() method and prints the value.

