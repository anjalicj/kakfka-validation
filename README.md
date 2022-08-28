# KAFKA Project to exchange & process events - Local
## System Set up (WSL)
### JAVA:
    - `sudo apt-get install openjdk-8-jdk`
    - `sudo echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /etc/environment`

### KAFKA
#### Run the following commands
    - Download the kafka package:
        `wget https://dlcdn.apache.org/kafka/3.2.1/kafka_2.13-3.2.1.tgz`
    - Unzip it:
        `tar -xzf kafka_2.13-3.2.1.tgz`
    - Remove the zip file:
        `sudo rm kafka_2.13-3.2.1.tgz`

## Running the project
### Start up the zookeeper and broker nodes
    - Spin up the nodes and create two kafka topics: input-topic & output-topic:
        `./build.sh`

### Producing - Consuming - Processing events
    - Produce sample events for input-topic:
        `python3 sample-events-to-input-topic.py`
    - In parallel to above, consume-preprocess-produce the events to output-topic:
        `python3 processing-kafka-events.py`
