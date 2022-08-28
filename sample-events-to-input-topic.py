# Import KafkaProducer from Kafka library
from kafka import KafkaProducer

# Import helper modules
import sys, json, time

# Define server with port
bootstrap_servers = ['localhost:9092']

# Define topic names
inputTopicName  = 'input-topic'

listOfEvents=[
    {"myKey": 1, "myTimestamp": "2022-03-01T09:11:04+01:00"},
    {"myKey": 2, "myTimestamp": "2022-03-01T09:12:08+01:00"},
    {"myKey": 3, "myTimestamp": "2022-03-01T09:13:12+01:00"},
    {"myKey": 4, "myTimestamp": ""},
    {"myKey": 5, "myTimestamp": "2022-03-01T09:14:05+01:00"},
    {"myKey": 1, "myTimestamp": "2022-03-01T09:11:04+01:00"},
    {"myKey": 2, "myTimestamp": "2022-03-01T09:12:08+01:00"},
    {"myKey": 3, "myTimestamp": "2022-03-01T09:13:12+01:00"},
    {"myKey": 4, "myTimestamp": ""},
    {"myKey": 5, "myTimestamp": "2022-03-01T09:14:05+01:00"},
]
# Initialize producer variable and set parameter for JSON encode
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Send events to output-topic
for event in listOfEvents:
    producer.send(inputTopicName, event)
    time.sleep(2)

# Print message
print("Events submitted")

# Terminate the script
sys.exit()