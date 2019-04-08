import sys
import os
import time
import json
import random

from google.cloud import pubsub_v1
import requests

project_id = os.getenv('PROJECT_ID')
if not project_id:
  raise ValueError('PROJECT_ID env variable is not set')

topic = os.getenv('INPUT_TOPIC')
if not topic:
  raise ValueError('INPUT_PUBSUB env variable is not set')

device_id = os.getenv('DEVICE_ID')
if not device_id:
  raise ValueError('DEVICE_ID env variable is not set')

aircraft_json_url = os.getenv('AIRCRAFT_JSON_URL')
if not aircraft_json_url:
  raise ValueError('AIRCRAFT_JSON_URL env variable is not set')

r = requests.get(aircraft_json_url)

if r.status_code != 200:
  raise ValueError(f'Error getting aircraft json data :{r.text}')

aircraft_data = r.json()
aircraft_count = len(aircraft_data['aircraft'])
print(f'Messages: {aircraft_count}')
message = {
      'device_id' : device_id,
      'aircraft_data' : [aircraft_data]
    }


client = pubsub_v1.PublisherClient()

full_topic_name = client.topic_path(project_id, topic)

message_bytes = json.dumps(message).encode('utf-8')

print(f'Message to be sent to {full_topic_name}:')

future_id = client.publish(full_topic_name, message_bytes)

event_id = future_id.result()

print(f'Message sent => Event id: {event_id}')