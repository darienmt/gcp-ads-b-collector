#!/bin/bash 

source ./scripts/env.sh

bq rm -f -t ${PROJECT_ID}:${DATASET_ID}.${TEST_TABLE_ID}

bq mk --table --description "ADB-S Messages" \
  --label "created-by:${CURRENT_ACCOUNT}" \
  --label "reason:unit-test" \
  --schema ./scripts/schema.json \
  ${PROJECT_ID}:${DATASET_ID}.${TEST_TABLE_ID}