# Import KafkaConsumer, KafkaProducer from Kafka library
from kafka import KafkaConsumer, KafkaProducer

# Import helper modules
import sys, json
from datetime import datetime, timedelta

# Define server with port
bootstrap_servers = ['localhost:9092']

# Define topic names
inputTopicName  = 'input-topic'
outputTopicName = 'output-topic'

# Initialize consumer variable
consumer = KafkaConsumer(
    inputTopicName, 
    bootstrap_servers=bootstrap_servers,
    consumer_timeout_ms=60000,
    group_id='group1',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    api_version=(2, 0, 2)
)

time_format = '%Y-%m-%dT%H:%M:%S%z'
listOfEvents = []

# Read and correct event from consumer
for event in consumer:
    print(event.value)
    myKey = event.value['myKey']
    myTimestamp = event.value['myTimestamp']
    if myTimestamp:
        myTimestamp = datetime.utcfromtimestamp(datetime.fromisoformat(myTimestamp).timestamp()).strftime(time_format) + "+00:00"
    dictEvent = {'myKey': myKey, 'myTimestamp': myTimestamp}
    listOfEvents.append(dictEvent)

print(f"Events processed: {len(listOfEvents)}")

# Initialize producer variable and set parameter for JSON encode
producer = KafkaProducer(bootstrap_servers =bootstrap_servers,value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Send events to output-topic
for event in listOfEvents:
    producer.send(outputTopicName, event)

print("Events submitted")

consumer = KafkaConsumer(
    outputTopicName, 
    bootstrap_servers=bootstrap_servers,
    consumer_timeout_ms=6000,
    group_id='group1',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)
for event in consumer:
    print(event.value)

# Print message
print("Events submitted")

# Terminate the script
sys.exit()