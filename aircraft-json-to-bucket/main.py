import sys
import os
import json
import time

import requests

from google.cloud import storage
from google.cloud.storage import Blob

device_id = os.getenv('DEVICE_ID')
if not device_id:
  raise ValueError('DEVICE_ID env variable is not set')

receiver_url = os.getenv('RECEIVER_URL')
if not receiver_url:
  raise ValueError('RECEIVER_URL env variable is not set')

output_bucket = os.getenv('OUTPUT_BUCKET')
if not output_bucket:
  raise ValueError('OUTPUT_BUCKET env variable is not set')

sampling_period_seconds = os.getenv('SAMPLING_PERIOD_SECONDS')
if not sampling_period_seconds:
  raise ValueError('SAMPLING_PERIOD_SECONDS env variable is not set')

sampling_period = int(sampling_period_seconds)

client = storage.Client()

bucket = client.get_bucket(output_bucket)

while True:
  r = requests.get(f'{receiver_url}/data/aircraft.json')

  if r.status_code != 200:
    raise ValueError(f'ERROR: getting aircraft json data :{r.text}')

  aircraft_data = r.json()

  now = aircraft_data['now']
  info_data = {
    'now': now,
    'aircraft_count' : len(aircraft_data['aircraft']),
    'messages': aircraft_data['messages']
  }
  print('INFO: ' + json.dumps(info_data))

  file_name = f'{device_id}/{now}.json'

  blob = Blob(file_name, bucket)
  blob.upload_from_string(json.dumps(aircraft_data), content_type='application/json')

  print(f'INFO: Uploaded : {file_name}')
  
  time.sleep(sampling_period)







