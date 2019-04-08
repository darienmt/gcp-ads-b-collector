#!/bin/bash 

source ./scripts/env.sh

gcloud beta functions deploy aircraft-json-collector \
 --entry-point handler \
 --runtime python37 \
 --trigger-topic ${INPUT_TOPIC} \
 --update-labels=created-by=${CURRENT_ACCOUNT}, \
 --set-env-vars DATASET_ID=${DATASET_ID} \
 --set-env-vars TABLE_ID=${TABLE_ID}