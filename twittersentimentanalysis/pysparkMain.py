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
import re
import logging
import time

# External librabries
from textblob import TextBlob

from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType, StructField, FloatType
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col

import findspark


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Configurations goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# Find Spark Path variable
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
findspark.init()

logging.basicConfig(filename='../logs/DEBUG_PySpark.log', filemode='w', encoding='UTF-8', level=logging.INFO)
logging.basicConfig(filename='../logs/DEBUG_TweetParser.log', filemode='w', encoding='UTF-8', level=logging.DEBUG, format='%(levelname)s: %(message)s')
logging.info('Spark Starts here:')


######################################################################################################################################################
# Code starts here
######################################################################################################################################################

def spark_session():
    # Spark object creation
    # Main spark reader in kafka format
    spark = SparkSession\
            .builder \
            .appName("Kafka_Consumer_Main") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
            .getOrCreate()
    
    return spark


def parse_df(ss):
    df = ss \
        .readStream \
        .format("kafka") \
        .option("subscribe", "TW_ANALYSIS")\
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .load()
    
    df1 = df.selectExpr("CAST(value AS STRING)")            # Refer &1

    df1.writeStream.outputMode("append").format("console").start().awaitTermination()


if __name__ == "__main__":
    ss = spark_session()
    parse_df(ss)




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
