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




