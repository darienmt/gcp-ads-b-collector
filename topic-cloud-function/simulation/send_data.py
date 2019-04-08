import sys
import os
import time
import json
import random

from google.cloud import pubsub_v1

with open('./sample_data.json') as json_file:
  data = json.load(json_file)

device_id = 'simulated_device'

message = {
      'device_id' : device_id,
      'aircraft_data' : data
    }

project_id = os.getenv('PROJECT_ID')
if not project_id:
  raise ValueError('PROJECT_ID env variable is not set')

topic = os.getenv('INPUT_TOPIC')
if not topic:
  raise ValueError('INPUT_PUBSUB env variable is not set')

client = pubsub_v1.PublisherClient()

full_topic_name = client.topic_path(project_id, topic)

message_bytes = json.dumps(message).encode('utf-8')

print(f'Message to be sent to {full_topic_name}:')

future_id = client.publish(full_topic_name, message_bytes)

event_id = future_id.result()

print(f'Message sent => Event id: {event_id}')