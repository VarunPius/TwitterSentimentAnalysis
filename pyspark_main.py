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
