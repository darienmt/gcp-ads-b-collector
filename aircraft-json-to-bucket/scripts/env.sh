#!/bin/bash 

export PROJECT_ID=$(gcloud config get-value project)

CURRENT_ACCOUNT=$(gcloud config list account --format "value(core.account)")

CURRENT_ACCOUNT=${CURRENT_ACCOUNT/@/_}

export CURRENT_ACCOUNT=${CURRENT_ACCOUNT//./_}

export BUCKET_PUBLISHER_ACCOUNT=bucket-publisher

export GOOGLE_APPLICATION_CREDENTIALS=~/GCP_${PROJECT_ID}_${BUCKET_PUBLISHER_ACCOUNT}.json

export DEVICE_ID=local-receiver

export OUTPUT_BUCKET=${PROJECT_ID}-aircraft-json

export SAMPLING_PERIOD_SECONDS=5