# Pre-reqs:
#  - A Kafka broker
#  - Confluent Kafka Python library
#      pip3 install confluent_kafka
#
# Usage: 
#
#  python python_kafka_test_client.py [bootstrap server]

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer
from confluent_kafka import Producer
from sys import argv
from datetime import datetime
import json

inputTopic='input-topic'
outputTopic='output-topic'
time_format = '%Y-%m-%dT%H:%M:%S%z'
inputListOfEvents = [
    {"myKey": 1, "myTimestamp": "2022-03-01T09:11:04+01:00"},
    {"myKey": 2, "myTimestamp": "2022-03-01T09:12:08+01:00"},
    {"myKey": 3, "myTimestamp": "2022-03-01T09:13:12+01:00"},
    {"myKey": 4, "myTimestamp": ""},
    {"myKey": 5, "myTimestamp": "2022-03-01T09:14:05+01:00"}
    ]
consumedListOfEvents = []
processedListOfEvents = []
topic_list=[]


def Produce(source_data, produce_to_topic):
    print(f'Producing messages to {produce_to_topic}')
    p = Producer({'bootstrap.servers': bootstrap_server})

    def delivery_status(err, msg):
        if err is not None:
            print(f'Produce failed: {err}')
        else:
            print(f"Message produced: {msg.value().decode('utf-8')} to {msg.topic()}")

    for data in source_data:
        p.poll(0)
        p.produce(produce_to_topic, json.dumps(data).encode('utf-8'), callback=delivery_status)

    r=p.flush(timeout=5)

def Consume(consume_from_topic):
    global consumedListOfEvents
    print(f'Consuming from {consume_from_topic}')
    c = Consumer({
        "bootstrap.servers": bootstrap_server,
        "group.id": 'kafka',
        "auto.offset.reset": 'earliest'
    })

    c.subscribe([consume_from_topic])
    print("Consumer Subscribed")
    try:
        msgs = c.consume(num_messages=10,timeout=30)

        if len(msgs)==0:
            print("No message(s) consumed")
        else:
            for msg in msgs:
                event = json.loads(msg.value().decode("utf-8"))
                myKey = event["myKey"]
                myTimestamp = event["myTimestamp"]
                dictEvent = {"myKey": myKey, "myTimestamp": myTimestamp}
                consumedListOfEvents.append(dictEvent)
                print(f'Message consumed: {msg.value().decode("utf-8")} from topic {msg.topic()}')
    except Exception as e:
        print(f"Consumer error: {e}")
    c.close()


def ProcessConsumed(consumedListOfEvents):
    global processedListOfEvents
    for event in consumedListOfEvents:
        if event['myTimestamp']:
            event["myTimestamp"] = datetime.utcfromtimestamp(datetime.fromisoformat(event["myTimestamp"]).timestamp()).strftime(time_format) + "+00:00"
        processedListOfEvents.append(event)


bootstrap_server=argv[1]
print(f'Connecting to bootstrap server: {bootstrap_server}')

a = AdminClient({'bootstrap.servers': bootstrap_server})
topic_list.append(NewTopic(topic="input-topic", num_partitions=1, replication_factor=1,))
topic_list.append(NewTopic(topic="output-topic", num_partitions=1, replication_factor=1,))
a.create_topics(topic_list)

try:         
    md=a.list_topics(timeout=10)
    print(f'Connected to bootstrap server: {bootstrap_server}')

    try:
        Produce(inputListOfEvents, inputTopic)
        Consume(inputTopic)
        ProcessConsumed(consumedListOfEvents)
        Produce(processedListOfEvents, outputTopic)
    except:
        print(f"(Exception in producer or consumer)")

except Exception as e:
    print(f'Failed to connect to bootstrap server {bootstrap_server}, {e}')
