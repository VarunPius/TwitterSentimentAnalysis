# Import libraries
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType, StructField, FloatType
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
import re
import logging
from textblob import TextBlob
import time

import findspark
findspark.init()

if __name__ == "__main__":
    # Create logging file
    logging.basicConfig(filename='spark_tw.log', encoding='UTF-8', level=logging.INFO)

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

    df1.writeStream.outputMode("append").format("console").start().awaitTermination()


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
