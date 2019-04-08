#!/bin/bash 

export PROJECT_ID=$(gcloud config get-value project)

CURRENT_ACCOUNT=$(gcloud config list account --format "value(core.account)")

CURRENT_ACCOUNT=${CURRENT_ACCOUNT/@/_}

export CURRENT_ACCOUNT=${CURRENT_ACCOUNT//./_}

export TEST_RUNNER_ACCOUNT=test-runner

export GOOGLE_APPLICATION_CREDENTIALS=~/GCP_${PROJECT_ID}_${TEST_RUNNER_ACCOUNT}.json

export INPUT_TOPIC=aircraft-json

export DATASET_ID=aircraft_data

export TABLE_ID=aircraft_json

export TEST_TABLE_ID=aircraft_json_test
