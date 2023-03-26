# Twitter Sentiment Analysis
The primary scope of this project is to identify sentiments on twitter based on the selected search word.

However, to make things interesting and learn some things in the process, I integrated more technologies into creating a pipeline.

The pipeline consists of the following stages:
- **Parser**: Will contain the code to grab tweets. We use **Tweepy** APIs from Twitter to grab the tweets.
- **Kafka**: The parser will write data to a Kafka topic. One single broker will give us capabilities to to spawn multiple parsers and write to single parser, thus ensuring scalability
- **Docker**: Kafka and Zookeeper servers will be spun on Docker containers
- **Spark**: Spark streaming will be used for data analysis. Machine learning libraries in Spark will enable easy sentiment enelysis.

# Installation
To successfully run this project, you would need certain tools pre-installed in the system:
- **Poetry**
- **Spark**: Spark needs the follow to successfully install:
    - **Java**
    - **Scala**
- **Docker**

After the installation of the above tools, do the following:
- Clone this project using `git clone`
- Run `poetry install`
- Spin up Kafka Docker: `docker-compose -f DockerCompose_Kafka.yaml up`

