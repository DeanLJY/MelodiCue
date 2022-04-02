import random
from time import sleep
from itertools import count
import json
from kafka import KafkaProducer


sleep(10)
producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

TOPIC_NAME = "test"

for i in count():
    json_data = {"name": f"node{i}"}
    producer.send(TOPIC_NAME, json_data)
    print(f"Sending {json_data}")
    producer.flush()
    sleep(1)
