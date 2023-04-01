# Twitter
- Create Tweepy API.
- Keep 


# Kafka
- We first start the Kafka server using Docker:
    ```
    docker-compose -f DockerCompose_Kafka.yaml up
    ```
- Create the topic:
    ```
    docker exec broker \
    kafka-topics --bootstrap-server broker:9092 \
                --create \
                --topic quickstart
    ```
- Write to topic:
    ```
    docker exec --interactive --tty broker \
    kafka-console-producer --bootstrap-server broker:9092 \
                        --topic quickstart
    ```
    or alternatively:
    ```
    docker exec -it broker kafka-console-producer --bootstrap-server broker:9092 --topic quickstart
    ```
- Read from topic:
    ```
    docker exec --interactive --tty broker \
    kafka-console-consumer --bootstrap-server broker:9092 \
                        --topic quickstart \
                        --from-beginning
    ```
    or alternatively:
    ```
    docker exec --it broker kafka-console-consumer --bootstrap-server broker:9092 --from-beginning --topic quickstart
    ```

# Python 3.10
There is some issue with using Python 3.11. AT the moment, Spark needs v3.4 to run Python 3.11 and it was not realeased at the time of doing this.
This is I kept getting the following error:
```
PicklingError: Could not serialize object: IndexError: tuple index out of range
```

To fix, I moved to version 3.10 in Poetry.

