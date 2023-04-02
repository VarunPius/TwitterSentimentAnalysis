# Import libraries
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType, StructField, FloatType
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
import re
import logging
from textblob import TextBlob
import time

import findspark
findspark.init()


def pre_process(text):
    text = text.split(' | Tweet: ')[1]
    # Remove links
    text = re.sub('http://\S+|https://\S+', '', text)
    text = re.sub('http[s]?://\S+', '', text)
    text = re.sub(r"http\S+", "", text)

    # Convert HTML references
    text = re.sub('&amp', 'and', text)
    text = re.sub('&lt', '<', text)
    text = re.sub('&gt', '>', text)
    text = re.sub('\xa0', ' ', text)

    # Remove new line characters
    text = re.sub('[\r\n]+', ' ', text)
    
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)

    # Remove multiple space characters
    text = re.sub('\s+',' ', text)
    
    # Convert to lowercase
    text = text.lower()
    logging.info("Debug: " + text)
    print("Debug:", text)
    return text


if __name__ == "__main__":
    # Create logging file
    logging.basicConfig(filename='../logs/DEBUG_PySpark.log', filemode='w', encoding='UTF-8', level=logging.INFO)
    logging.info("-- PySpark Started!!  --")

    # Spark object creation
    spark = SparkSession\
            .builder \
            .appName("Kafka_Consumer_Test") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
            .getOrCreate()

    # Main spark reader in kafka format
    df = spark \
        .readStream \
        .format("kafka") \
        .option("subscribe", "TW_ANALYSIS")\
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .load()
    
    df1 = df.selectExpr("CAST(value AS STRING)")            # Refer &1    
    #df1 = df1.withColumn('processed_tweet', col('value'))

    convertUDF = udf(lambda z: pre_process(z), StringType())
    df2 = df1.select(convertUDF(col("value")).alias("processed_tweet") )
    df2.writeStream.outputMode("append").format("console").option("truncate", "false").start().awaitTermination()



"""
Appendix:

----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
&1:

Output of df is:
-------------------------------------------                                     
Batch: 0
-------------------------------------------
+---+-----+-----+---------+------+---------+-------------+
|key|value|topic|partition|offset|timestamp|timestampType|
+---+-----+-----+---------+------+---------+-------------+
+---+-----+-----+---------+------+---------+-------------+

-------------------------------------------                                     
Batch: 1
-------------------------------------------
+----+--------------------+-----------+---------+------+--------------------+-------------+
| key|               value|      topic|partition|offset|           timestamp|timestampType|
+----+--------------------+-----------+---------+------+--------------------+-------------+
|null|[7B 22 48 65 6C 6...|TW_ANALYSIS|        0|    87|2022-10-09 13:25:...|            0|
+----+--------------------+-----------+---------+------+--------------------+-------------+

As you can see, the values are coming as ByteStream. The input in the consumer was '{"Hello": "World"}'

This is why we we cast as String to get:
+------------------+
|             value|
+------------------+
|{"Hello": "World"}|
+------------------+
"""

###
'''
https://towardsdatascience.com/sentiment-analysis-on-streaming-twitter-data-using-spark-structured-streaming-python-fc873684bfe3
https://medium.com/analytics-vidhya/congressional-tweets-using-sentiment-analysis-to-cluster-members-of-congress-in-pyspark-10afa4d1556e


'''