#!/bin/bash 

export PROJECT_ID=$(gcloud config get-value project)

CURRENT_ACCOUNT=$(gcloud config list account --format "value(core.account)")

CURRENT_ACCOUNT=${CURRENT_ACCOUNT/@/_}

export CURRENT_ACCOUNT=${CURRENT_ACCOUNT//./_}

export INPUT_TOPIC=adbs

export DATASET_ID=airplane_data

export TABLE_ID=adbs_messages

export TEST_TABLE_ID=adbs_messages_test
