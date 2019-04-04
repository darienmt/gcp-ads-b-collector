#!/bin/bash 

source ./scripts/env.sh

bq mk --description "Airplane data dataset" ${PROJECT_ID}:${DATASET_ID} 

bq update --set_label created-by:${CURRENT_ACCOUNT} ${PROJECT_ID}:${DATASET_ID}

bq mk --table --description "ADB-S Messages" \
  --label "created-by:${CURRENT_ACCOUNT}" \
  --schema ./scripts/schema.json \
  --time_partitioning_field timestamp \
  --time_partitioning_expiration 7776000000 \
  ${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}


