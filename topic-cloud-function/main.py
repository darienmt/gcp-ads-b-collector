import base64
import json
import os
import hashlib

from google.cloud import bigquery

from google.api_core.exceptions import NotFound

from datetime import datetime

def get_table_and_bq_client(dataset_id, table_name):
  """
  Returns the table instance and the BigQuery client `(table, bq_client)`.
  """
  bq_client = bigquery.Client()

  dataset_ref = bq_client.dataset(dataset_id)

  try:
    bq_client.get_dataset(dataset_ref)
  except NotFound:
    raise ValueError(f'The dataset {dataset_id} was not found')
  
  table_ref = dataset_ref.table(table_name)
  try:
    table = bq_client.get_table(table_ref)
  except NotFound:
    raise ValueError(f'The table {table_name} could not be found in the dataset {dataset_id}')
  
  return (table, bq_client)

def map_aircraft_to_record(aircrafts, message_now, device_id):
  """
  Maps the `aircraft` entity to a BigQuery record and its unique id.
  Returns `(unique_ids, records)`
  """
  def copy_data(aircraft):
    result = aircraft.copy()
    result['device_id'] = device_id
    result['timestamp'] = datetime.utcfromtimestamp(float(message_now)).isoformat()

    result_json = json.dumps(result)
    result_hash = hashlib.sha512(result_json.encode('utf-8')).hexdigest()
    unique_id = f'{message_now}_{result_hash}'

    result['created_at'] = datetime.now().isoformat()
    return (unique_id, result)

  return zip( *map( copy_data, aircrafts ) )

def create_records(data):
  """
  Converts the received `data` into `(unique_ids, records)`
  """
  device_id = data['device_id']
  aircraft_data = data['aircraft_data']

  def flattener( aircraft_message ):
    message_now = aircraft_message['now']
    return map_aircraft_to_record( aircraft_message['aircraft'], message_now, device_id )

  unique_ids, records = zip(*map(flattener, aircraft_data))

  flatten = lambda l: [item for sublist in l for item in sublist]
  return (flatten(unique_ids), flatten(records))
      
def insert_records(data, table, bq_client):
  """
  Insert the `data` aircraft messages into `table` with `bq_client`
  """
  unique_ids, records = create_records(data)

  results = bq_client.insert_rows_json(table, records, row_ids=unique_ids, skip_invalid_rows=True)

  def get_error_data(result):
    index = result.get('index')
    record = records[index] if index != None else None
    return (record, result.get('errors'))

  errors = list(map(get_error_data, results)) if results else []  
  
  total_inserted = len(records) - len(errors)
  
  return (total_inserted, errors)

def process_reporter(data_inserter):
  """
  Process device aircraft data
  """
  total_inserted, errors = data_inserter()
  print(f'INFO: Total inserted records: {total_inserted}')
  if error_data:
    for (record, err) in errors:
      record_json = json.dumps(record) if record else 'NotFound'
      joined_errors = ','.join(err)
      print(f'ERROR: Error inserting {record_json}, Errors : {joined_errors}')


global_bq_client = None
global_table = None

def handler(event, context):
  """
  Receives an aircraft device message from a PubSub topic, and inserts it in a BigQuery table
  """
  dataset_id = os.getenv('DATASET_ID')
  if not dataset_id:
    raise ValueError('The DATASET_ID environment variable is not set')

  table_id = os.getenv('TABLE_ID')
  if not table_id:
    raise ValueError('The TABLE_ID environment variable is not set')
  
  global global_bq_client, global_table
  if global_bq_client == None or global_table == None:
    global_table, global_bq_client = get_table_and_bq_client(dataset_id, table_id)
  
  data = event.get('data')
  if not data:
    raise ValueError('No data attribute was found on the event')

  message_raw = base64.b64decode(data).decode('utf-8')

  message_json = json.loads(message_raw)

  process_reporter(lambda : insert_records(message_json, global_table, global_bq_client))
