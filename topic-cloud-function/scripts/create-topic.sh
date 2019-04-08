#!/bin/bash 

source ./scripts/env.sh

gcloud alpha pubsub topics create ${INPUT_TOPIC} \
--labels=created-by=${CURRENT_ACCOUNT}