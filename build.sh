#!/usr/bin/env bash

# Creating docker network
docker network create Test_kafka

echo "*******************************"
echo "Spinning up zookeeper container"
docker run --network=Test_kafka --rm --detach --name zookeeper -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:5.5.0

echo "*******************************"
echo "Giving zookeeper container a bit of time to start up: 10 seconds"
sleep 10

echo "*******************************"
echo "Spinning up kafka broker container"
docker run --network=Test_kafka --rm --detach --name broker \
           -p 9092:9092 \
           -e KAFKA_BROKER_ID=1 \
           -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
           -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://broker:9092 \
           -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
           -e AUTO_CREATE_TOPICS_ENABLE=false \
           confluentinc/cp-kafka:5.5.0

echo "*******************************"
echo "Building kafka processing image"
docker build -t processing_kafka .

echo "*******************************"
echo "Running kafka processing"
docker run --network=Test_kafka --rm --name processing_kafka \
           --tty processing_kafka broker:9092