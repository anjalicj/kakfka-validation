#!/usr/bin/env bash
cd kafka_2.13-3.2.1/
`bin/zookeeper-server-start.sh config/zookeeper.properties` &
sleep 30
`bin/kafka-server-start.sh config/server.properties`
sleep 30
`bin/kafka-topics.sh --create --topic input-topic --bootstrap-server localhost:9092` &
`bin/kafka-topics.sh --create --topic output-topic --bootstrap-server localhost:9092`

