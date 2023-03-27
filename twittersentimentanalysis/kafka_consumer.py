######################################################################################################################################################
# Code Info                                                                                                                                          #
#                                                                                                                                                    #
# Kafka_consumer.py                                                                                                                                  #
# Author(s): Varun Pius Rodrigues                                                                                                                    #
# About: Reads tweets from Kafka topic; this is a placeholder to process kafka data while Spark implementation was incomplete;                       #
#        Use this to read from Kafka and check it Kafka topic is working or if Spark part is not complete.                                           #
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

# External librabries
from ruamel.yaml import YAML
from kafka import KafkaConsumer


######################################################################################################################################################
# Code starts here
######################################################################################################################################################

# Kafka Consumer
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
def kafka_initializer(env):
    yaml=YAML(typ='safe')                                       # default, if not specfied, is 'rt' (round-trip)
    with open('../resources/config.yml', 'r') as file:
        config = yaml.load(file)

    btstrp_srvr = config[env]['Kafka']['bootstrap_servers']

    # Topic name for Kafka tracing
    topic_name = config[env]['Kafka']['topic_name']             #'TW_ANALYSIS'
    
    print(btstrp_srvr, topic_name)
    
    # Kafka Consumer
    consumer = KafkaConsumer(topics = topic_name, bootstrap_servers=btstrp_srvr,      #['localhost:9092'],   # $Appx1
                            # Deserialize the string from the producer since it comes in hex
                            key_deserializer=lambda x: x.decode('utf-8'),
                            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
                        )
                                                                            
    return consumer


# Main 
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    env = 'Dev'
    consumer = kafka_initializer(env)

    for message in consumer:
        print("Key: ", message.key)
        print("Value: ", json.loads(json.dumps(message.value)))


######################################################################################################################################################
# Notes/Appendix
######################################################################################################################################################

# Appx1 
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
'''
kafkaConsumer takes positional arguments before keyword arguments; 
meaning topics names `*topics` should be placed first, before specifying other arguments using the keyword (key-value pairs using `=`)
'''
