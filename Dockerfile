FROM python:3

# We'll add netcat cos it's a really useful
# network troubleshooting tool
RUN apt-get update
RUN apt-get install -y netcat

# Install the Confluent Kafka python library
RUN pip install confluent_kafka
RUN pip install --upgrade pip
ADD requirements.txt .
RUN python -m pip install -r requirements.txt
#RUN pip install json

# Add our script
ADD processing_kafka.py /
ENTRYPOINT [ "python", "/processing_kafka.py"]
