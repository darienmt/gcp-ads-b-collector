import os
import json

from google.cloud import bigquery

from google.api_core.exceptions import NotFound

from main import get_table_and_bq_client

from main import map_aircraft_to_record

from main import create_records

from main import insert_records

from main import handler

class TestMain(object):

  @classmethod
  def setup_class(cls):
    cls.project_id = os.getenv('PROJECT_ID')
    if cls.project_id == None:
      raise ValueError('The PROJECT_ID environment variable must be configured to run the test')
    
    cls.dataset_id = os.getenv('DATASET_ID')
    if cls.dataset_id == None:
      raise ValueError('The DATASET_ID environment variable must be configured to run the test')

    cls.table_id = os.getenv('TEST_TABLE_ID')
    if cls.table_id == None:
      raise ValueError('The TEST_TABLE_ID environment variable must be configured to run the test')

    cls.table, cls.bq_client = get_table_and_bq_client(cls.dataset_id, cls.table_id)
  
  def test_map_to_record_ok(self):
    now = 1554347065.9
    device_id = 'this_device'

    data = [
          {
            "hex": "c08562", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
          },
        ]

    unique_ids, records = map_aircraft_to_record(data, now, device_id)

    assert unique_ids
    assert records
    assert len(unique_ids) == 1
    assert len(records) == 1

  def test_test_map_to_record_same_values_has_same_unique_id(self):
    now = 1554347065.9
    device_id = 'this_device'

    data = [
          {
            "hex": "c08562", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
          },
          {
            "hex": "c08562", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
          },
        ]

    unique_ids, records = map_aircraft_to_record(data, now, device_id)

    assert unique_ids
    assert records
    assert len(unique_ids) == 2
    assert len(records) == 2
    assert unique_ids[0] == unique_ids[1]

  def test_create_records_ok(self):
    data = {
      'device_id' : 'this_device',
      'aircraft_data' : [
        {
          'now' : 1554347065.9,
          'aircraft' : [
            {
              "hex": "c08562", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            },
            {
              "hex": "c08522", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            }
          ]
        },
        {
          'now' : 1554247065.9,
          'aircraft' : [
            {
              "hex": "c08362", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            },
            {
              "hex": "c08422", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            }
          ]
        }
      ]
    }
    
    unique_ids, records = create_records(data)
    assert len(unique_ids) == 4
    assert len(records) == 4

  def test_insert_records_ok(self):
    data = {
      'device_id' : 'this_device',
      'aircraft_data' : [
        {
          'now' : 1554347065.9,
          'aircraft' : [
            {
              "hex": "c08562", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            },
            {
              "hex": "c08522", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            }
          ]
        },
        {
          'now' : 1554247065.9,
          'aircraft' : [
            {
              "hex": "c08362", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            },
            {
              "hex": "c08422", "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            }
          ]
        }
      ]
    }
    
    total_inserted, errors = insert_records(data, TestMain.table, TestMain.bq_client)
    assert total_inserted == 4
    assert not errors

  def test_insert_records_with_errors(self):
    data = {
      'device_id' : 'this_device',
      'aircraft_data' : [
        {
          'now' : 1554347065.9,
          'aircraft' : [
            {
              "squawk": "4304", "lat": 43.517311, "lon": -79.821494, "nucp": 0, "seen_pos": 6.7, "altitude": 2300, "vert_rate": 0, "track": 144, "speed": 176, "messages": 70, "seen": 0.8, "rssi": -23.2
            }
          ]
        }
      ]
    }
    
    total_inserted, errors = insert_records(data, TestMain.table, TestMain.bq_client)
    assert total_inserted == 0
    assert len(errors) == 1

  # def test_handler_ok(self):
  #   event = { 
  #     'data' : "ewogICAgICAiZGV2aWNlX2lkIiA6ICJ0aGlzX2RldmljZSIsCiAgICAgICJhaXJjcmFmdF9kYXRhIiA6IFsKICAgICAgICB7CiAgICAgICAgICAibm93IiA6IDE1NTQzNDcwNjUuOSwKICAgICAgICAgICJhaXJjcmFmdCIgOiBbCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAiaGV4IjogImNjY2MiLCAic3F1YXdrIjogIjQzMDQiLCAibGF0IjogNDMuNTE3MzExLCAibG9uIjogLTc5LjgyMTQ5NCwgIm51Y3AiOiAwLCAic2Vlbl9wb3MiOiA2LjcsICJhbHRpdHVkZSI6IDIzMDAsICJ2ZXJ0X3JhdGUiOiAwLCAidHJhY2siOiAxNDQsICJzcGVlZCI6IDE3NiwgIm1lc3NhZ2VzIjogNzAsICJzZWVuIjogMC44LCAicnNzaSI6IC0yMy4yCiAgICAgICAgICAgIH0KICAgICAgICAgIF0KICAgICAgICB9CiAgICAgIF0KICAgIH0="
  #   }

  #   context = {}

  #   handler(event, context)

  # def test_handler_with_errors(self):
  #   event = { 
  #     'data' : "ewogICAgICAiZGV2aWNlX2lkIiA6ICJ0aGlzX2RldmljZSIsCiAgICAgICJhaXJjcmFmdF9kYXRhIiA6IFsKICAgICAgICB7CiAgICAgICAgICAibm93IiA6IDE1NTQzNDcwNjUuOSwKICAgICAgICAgICJhaXJjcmFmdCIgOiBbCiAgICAgICAgICAgeyJtbGF0IjpbXSwidGlzYiI6W10sIm1lc3NhZ2VzIjoyMTIwLCJzZWVuIjoxOTMuOSwicnNzaSI6LTI5LjR9CiAgICAgICAgICBdCiAgICAgICAgfQogICAgICBdCiAgICB9"
  #   }

  #   context = {}

  #   handler(event, context)